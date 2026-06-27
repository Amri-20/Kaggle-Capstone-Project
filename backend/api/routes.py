import os
import uuid
import json
import asyncio
import re
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

# Database & Security Imports
from backend.database.models import SessionLocal, User, BoardSession, Message, AuditLog, ApprovalRequest, MemoryItem, ExecutionLog
from backend.security.auth import (
    get_password_hash, verify_password, create_access_token, decode_access_token,
    check_prompt_injection, sanitize_input, verify_role
)
from backend.memory.store import MemoryService

# ADK Imports
from google.adk.runners import InMemoryRunner
from backend.app.agent import ceo_agent

# Utils Imports
from backend.utils.parser import parse_file
from backend.utils.reports import generate_markdown_report, generate_pdf_report, generate_pptx_report, compile_report_data
from backend.app.skills import generate_financial_chart, summarize_text

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper to log execution steps
def log_step_helper(session_id: str, agent_name: str, message: str, step_name: str = None):
    try:
        db = SessionLocal()
        try:
            log = ExecutionLog(
                session_id=session_id,
                agent_name=agent_name,
                step_name=step_name,
                message=message
            )
            db.add(log)
            db.commit()
        finally:
            db.close()
    except Exception as e:
        print(f"Failed to log execution step: {e}")

# Pydantic Schemas
class UserRegister(BaseModel):
    username: str
    password: str
    role: Optional[str] = "viewer"

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    role: str

class BoardRunRequest(BaseModel):
    name: str
    proposal: str
    context_document_id: Optional[str] = None

class MemoryAddRequest(BaseModel):
    key: str
    value: str
    category: str

class ApprovalResolveRequest(BaseModel):
    status: str # approved or rejected
    resolver_username: str

# Helper to verify token from header
def get_current_user(token: str, db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ================= AUTH ENDPOINTS =================

@router.post("/auth/register")
def register_user(req: UserRegister, db: Session = Depends(get_db)):
    # Check if username exists
    existing = db.query(User).filter(User.username == req.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    pwd_hash = get_password_hash(req.password)
    user = User(username=req.username, password_hash=pwd_hash, role=req.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    MemoryService.log_audit(db, user.id, user.username, "register", f"User registered with role: {req.role}")
    return {"status": "success", "username": user.username, "role": user.role}

@router.post("/auth/login", response_model=TokenResponse)
def login_user(req: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
        
    token = create_access_token({"sub": user.username, "role": user.role})
    MemoryService.log_audit(db, user.id, user.username, "login", "User logged in successfully")
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role
    }

# ================= BOARDRUN BACKGROUND TASK =================

async def run_boardroom_adk_runner(session_id: str, proposal: str, context_text: str):
    """Asynchronous background task that executes the ADK runner and stores results."""
    db = SessionLocal()
    try:
        # Load long-term memory (past decisions)
        memories = MemoryService.search_memories(db, proposal, limit=3)
        memory_context = "\n".join([f"- {m['key']}: {m['value']}" for m in memories])
        
        # Load user preferences and strategic constraints
        prefs = MemoryService.get_memories_by_category(db, "preference")
        pref_context = "\n".join([f"- {p.key}: {p.value}" for p in prefs])
        
        full_prompt = f"Business Proposal: {proposal}\n"
        if context_text:
            full_prompt += f"\nUploaded Reference Document Content:\n{context_text}\n"
        if memory_context:
            full_prompt += f"\nRelevant Past Decision Memory Context:\n{memory_context}\n"
        if pref_context:
            full_prompt += f"\nUser Preferences & Strategic Constraints:\n{pref_context}\n"
            
        runner = InMemoryRunner(agent=ceo_agent, app_name="boardroom_app")
        
        # Initialize ADK state variables
        runner.state["session_id"] = session_id
        runner.state["current_agent"] = "CEO"
        
        log_step_helper(session_id, "CEO", "CEO Agent initialized the Boardroom.", "init")
        
        # Run ADK orchestrator
        async for event in runner.run_async(user_id="user", session_id=session_id, input_text=full_prompt):
            # Parse events and save dialogue to DB
            if event.author:
                author_name = event.author
                content = event.content or ""
                
                # Check for agent switch
                if "agent" in author_name.lower():
                    runner.state["current_agent"] = author_name
                
                if content:
                    msg = Message(
                        session_id=session_id,
                        sender=author_name,
                        content=content
                    )
                    db.add(msg)
                    db.commit()
                    log_step_helper(session_id, author_name, f"Said: {content[:100]}...", "dialogue")
                    
        # Collect debate outcome and generate files using real Gemini extractor
        msgs = db.query(Message).filter(Message.session_id == session_id).all()
        full_debate_text = "\n".join([f"{m.sender}: {m.content}" for m in msgs])
        
        # Run real structured extraction
        log_step_helper(session_id, "Report Agent", "Parsing debate transcript and compiling structured strategic review...", "parsing_debate")
        report_data = compile_report_data(full_debate_text, proposal)
        
        # Create final reports
        md_filepath = f"backend/static/reports/{session_id}_report.md"
        pdf_filepath = f"backend/static/reports/{session_id}_report.pdf"
        pptx_filepath = f"backend/static/reports/{session_id}_report.pptx"
        chart_filepath = f"backend/static/charts/{session_id}_chart.png"
        
        # Write Markdown report
        md_content = generate_markdown_report(report_data)
        with open(md_filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        # Generate chart
        generate_financial_chart(120000, 180000, 240000, 150000, chart_filepath)
        
        # Generate PDF & PPTX
        generate_pdf_report(report_data, pdf_filepath)
        generate_pptx_report(report_data, pptx_filepath)
        
        # Log completion
        log_step_helper(session_id, "Report Agent", "Generated MD, PDF, and PPTX reports successfully.", "reports_done")
        
        # Update Session Status to completed
        sess = db.query(BoardSession).filter(BoardSession.id == session_id).first()
        if sess:
            sess.status = "completed"
            db.commit()
            
        # Add to long term memory for future searches
        MemoryService.add_memory(
            db=db,
            key=f"Decision for {proposal[:40]}",
            value=f"Recommendation: {report_data['recommendation']}. Decision Score: {report_data['decision_score']}.",
            category="decision",
            session_id=session_id
        )
        
    except Exception as e:
        log_step_helper(session_id, "System", f"Execution failed with error: {str(e)}", "error")
        sess = db.query(BoardSession).filter(BoardSession.id == session_id).first()
        if sess:
            sess.status = "failed"
            db.commit()
    finally:
        db.close()

# ================= BOARDROOM ENDPOINTS =================

@router.post("/board/start")
def start_board_evaluation(
    req: BoardRunRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    session_id = str(uuid.uuid4())
    
    # Prompt injection check
    if check_prompt_injection(req.proposal):
        MemoryService.log_audit(db, None, "system", "injection_prevented", f"Prompt injection block: {req.proposal[:50]}")
        raise HTTPException(status_code=400, detail="Security Warning: Prompt contains unauthorized instructions.")
        
    # Get parsed context text if document is provided
    context_text = ""
    if req.context_document_id:
        doc = db.query(MemoryItem).filter(MemoryItem.id == int(req.context_document_id)).first()
        if doc:
            context_text = doc.value
            
    # Create Board Session record
    sess = BoardSession(id=session_id, name=req.name, user_id=1, status="running")
    db.add(sess)
    db.commit()
    
    # Launch debate in background task
    background_tasks.add_task(run_boardroom_adk_runner, session_id, req.proposal, context_text)
    
    return {
        "status": "started",
        "session_id": session_id,
        "message": "Boardroom debate initiated in the background."
    }

@router.get("/board/sessions")
def get_all_sessions(db: Session = Depends(get_db)):
    return db.query(BoardSession).order_by(BoardSession.created_at.desc()).all()

@router.get("/board/session/{session_id}/timeline")
def get_session_timeline(session_id: str, db: Session = Depends(get_db)):
    return MemoryService.get_execution_timeline(db, session_id)

@router.get("/board/session/{session_id}/messages")
def get_session_messages(session_id: str, db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp.asc()).all()

# ================= HUMAN APPROVALS =================

@router.get("/board/approvals")
def get_approvals(db: Session = Depends(get_db)):
    return MemoryService.get_pending_approvals(db)

@router.post("/board/approve/{approval_id}")
def resolve_approval(approval_id: str, req: ApprovalResolveRequest, db: Session = Depends(get_db)):
    req_obj = MemoryService.resolve_approval_request(db, approval_id, req.status, req.resolver_username)
    if not req_obj:
        raise HTTPException(status_code=404, detail="Approval request not found")
    
    MemoryService.log_audit(db, None, req.resolver_username, f"approval_{req.status}", f"Approval {approval_id} resolved: {req.status}")
    return {"status": "success", "message": f"Approval request {req.status} successfully."}

# ================= FILE PROCESSING =================

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".csv", ".xlsx", ".xls", ".txt", ".md"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/board/upload")
async def upload_file_for_analysis(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Validate file extension
    filename = file.filename or "unknown"
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}"
        )
        
    # 2. Validate file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds limit of 10MB. Got {len(contents) / (1024 * 1024):.1f}MB."
        )
        
    # 3. Sanitize filename and construct path
    clean_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    file_id = str(uuid.uuid4())
    save_path = f"backend/static/uploads/{file_id}_{clean_filename}"
    
    try:
        with open(save_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
        
    # Parse file contents
    parsed_text = parse_file(save_path)
    
    # Store parsed text in database as document context memory
    mem = MemoryService.add_memory(
        db=db,
        key=f"Uploaded Document: {filename}",
        value=parsed_text,
        category="context"
    )
    
    return {
        "status": "success",
        "document_id": mem.id,
        "filename": filename,
        "parsed_preview": parsed_text[:200] + "..."
    }

# ================= MEMORY ENDPOINTS =================

@router.get("/memory/search")
def search_memories(query: str, db: Session = Depends(get_db)):
    return MemoryService.search_memories(db, query, limit=5)

@router.post("/memory/add")
def add_memory_item(req: MemoryAddRequest, db: Session = Depends(get_db)):
    item = MemoryService.add_memory(db, req.key, req.value, req.category)
    return {"status": "success", "memory": {"id": item.id, "key": item.key, "category": item.category}}

@router.get("/memory/all")
def get_all_memories(db: Session = Depends(get_db)):
    return db.query(MemoryItem).order_by(MemoryItem.created_at.desc()).all()

@router.delete("/memory/delete/{memory_id}")
def delete_memory_item(memory_id: int, db: Session = Depends(get_db)):
    success = MemoryService.delete_memory(db, memory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Memory item not found")
    return {"status": "success", "message": "Memory item deleted successfully."}

# ================= REPORTS =================

@router.get("/reports/download/{session_id}/{format}")
def download_report(session_id: str, format: str):
    format = format.lower().strip()
    if format not in ["pdf", "pptx", "md"]:
        raise HTTPException(status_code=400, detail="Invalid format")
        
    filepath = f"backend/static/reports/{session_id}_report.{format}"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Report not generated yet or session failed.")
        
    media_types = {
        "pdf": "application/pdf",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "md": "text/markdown"
    }
    
    return FileResponse(filepath, media_type=media_types[format], filename=f"BoardRoom_AI_Report_{session_id[:8]}.{format}")

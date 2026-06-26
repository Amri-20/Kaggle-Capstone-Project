from datetime import datetime
import json
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.database.models import MemoryItem, AuditLog, ExecutionLog, ApprovalRequest, BoardSession, Message

class MemoryService:
    @staticmethod
    def add_memory(db: Session, key: str, value: str, category: str = "context", session_id: Optional[str] = None) -> MemoryItem:
        """Add a new memory item to the SQLite store."""
        item = MemoryItem(
            session_id=session_id,
            key=key,
            value=value,
            category=category
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def search_memories(db: Session, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Perform a keyword-matching semantic search over stored memory items."""
        if not query:
            return []
            
        # Split query into words, normalize
        query_words = [w.lower() for w in query.split() if len(w) > 2]
        
        # Load all memories
        memories = db.query(MemoryItem).all()
        scored_memories = []
        
        for mem in memories:
            score = 0
            mem_text = f"{mem.key} {mem.value} {mem.category}".lower()
            
            # Simple keyword matching score
            for word in query_words:
                if word in mem_text:
                    score += 1.0
                    # Give extra weight to exact word match
                    if f" {word} " in f" {mem_text} ":
                        score += 0.5
            
            if score > 0:
                scored_memories.append({
                    "id": mem.id,
                    "key": mem.key,
                    "value": mem.value,
                    "category": mem.category,
                    "created_at": mem.created_at.isoformat(),
                    "score": score
                })
                
        # Sort by score descending
        scored_memories.sort(key=lambda x: x["score"], reverse=True)
        return scored_memories[:limit]

    @staticmethod
    def get_memories_by_category(db: Session, category: str) -> List[MemoryItem]:
        """Fetch all memories in a given category."""
        return db.query(MemoryItem).filter(MemoryItem.category == category).all()

    @staticmethod
    def delete_memory(db: Session, memory_id: int) -> bool:
        """Delete a memory item."""
        item = db.query(MemoryItem).filter(MemoryItem.id == memory_id).first()
        if item:
            db.delete(item)
            db.commit()
            return True
        return False

    @staticmethod
    def log_audit(db: Session, user_id: Optional[int], username: Optional[str], action: str, details: Optional[str] = None):
        """Create an audit log entry."""
        log = AuditLog(
            user_id=user_id,
            username=username,
            action=action,
            details=details
        )
        db.add(log)
        db.commit()

    @staticmethod
    def log_execution(db: Session, session_id: str, agent_name: str, step_name: Optional[str], message: str):
        """Create an agent execution log entry."""
        log = ExecutionLog(
            session_id=session_id,
            agent_name=agent_name,
            step_name=step_name,
            message=message
        )
        db.add(log)
        db.commit()

    @staticmethod
    def get_execution_timeline(db: Session, session_id: str) -> List[Dict[str, Any]]:
        """Fetch a chronological timeline of steps executed for a session."""
        logs = db.query(ExecutionLog).filter(ExecutionLog.session_id == session_id).order_by(ExecutionLog.timestamp.asc()).all()
        return [
            {
                "id": log.id,
                "agent_name": log.agent_name,
                "step_name": log.step_name,
                "message": log.message,
                "timestamp": log.timestamp.isoformat()
            }
            for log in logs
        ]

    @staticmethod
    def add_approval_request(db: Session, request_id: str, session_id: str, tool_name: str, arguments: dict) -> ApprovalRequest:
        """Log a tool execution requiring human approval."""
        req = ApprovalRequest(
            id=request_id,
            session_id=session_id,
            tool_name=tool_name,
            arguments=json.dumps(arguments),
            status="pending"
        )
        db.add(req)
        db.commit()
        db.refresh(req)
        return req

    @staticmethod
    def get_pending_approvals(db: Session) -> List[ApprovalRequest]:
        """Fetch all pending tool execution approvals."""
        return db.query(ApprovalRequest).filter(ApprovalRequest.status == "pending").all()

    @staticmethod
    def resolve_approval_request(db: Session, request_id: str, status: str, resolver_username: str) -> Optional[ApprovalRequest]:
        """Resolve (Approve or Reject) a tool approval request."""
        req = db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
        if req:
            req.status = status
            req.resolved_at = datetime.utcnow()
            req.resolved_by = resolver_username
            db.commit()
            db.refresh(req)
            return req
        return None

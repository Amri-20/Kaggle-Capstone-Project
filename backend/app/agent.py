import os
import uuid
import datetime
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import FunctionTool
from google.genai import types

# Import tools
from backend.app.tools import (
    list_directory, read_file, write_file,
    execute_sqlite_query, browse_web,
    github_mcp_operation, google_drive_mcp_operation,
    execute_sensitive_transaction
)

# Import skills
from backend.app.skills import (
    market_research, calculate_financial_kpis,
    generate_financial_chart, summarize_text, extract_citations
)

# Use API Key authentication for prototype
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key
    os.environ["GOOGLE_API_KEY"] = api_key

# We use gemini-1.5-flash as the standard robust model
model_instance = Gemini(
    model="gemini-1.5-flash",
    retry_options=types.HttpRetryOptions(attempts=3),
)

# Create database logger callback helpers
def log_step_helper(session_id: str, agent_name: str, message: str, step_name: str = None):
    """Write execution logs to the database."""
    try:
        from backend.database.models import SessionLocal, ExecutionLog
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

# Callbacks to log agent lifecycle events
async def before_agent(callback_context) -> None:
    session_id = callback_context.session.id
    agent_name = callback_context.agent_name
    log_step_helper(session_id, agent_name, f"Starting analysis cycle...", "agent_start")

async def after_agent(callback_context) -> None:
    session_id = callback_context.session.id
    agent_name = callback_context.agent_name
    log_step_helper(session_id, agent_name, f"Completed analysis cycle.", "agent_end")

# Create agents
cfo_agent = Agent(
    name="cfo_agent",
    model=model_instance,
    description="Chief Financial Officer. Analyzes budgets, costs, ROI, and financial feasibility.",
    instruction="""You are the Chief Financial Officer (CFO) of the board.
Your job is to analyze the financial viability of the proposal.
You must:
1. Estimate initial budget, annual revenues, and ROI over 3 years.
2. Use the calculate_financial_kpis tool to calculate precise financial KPIs.
3. Use the generate_financial_chart tool to save a visualization of the projections to 'backend/static/charts/{session_id}_chart.png'.
4. Identify financial risks and propose cost mitigations.
5. Present a clear financial summary.
6. When executing sensitive transactions (like releasing budget), use the execute_sensitive_transaction tool.
Always state your findings clearly and transfer control back to the CEO agent when done.""",
    tools=[
        FunctionTool(calculate_financial_kpis),
        FunctionTool(generate_financial_chart),
        FunctionTool(execute_sensitive_transaction, require_confirmation=True)
    ],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent
)

cto_agent = Agent(
    name="cto_agent",
    model=model_instance,
    description="Chief Technology Officer. Evaluates technical feasibility, software stacks, engineering effort, and scalability.",
    instruction="""You are the Chief Technology Officer (CTO) of the board.
Your job is to review the technical implementation details of the project.
You must:
1. Recommend a modern, secure, and scalable technology stack.
2. Estimate engineering effort (in terms of team size and months).
3. Evaluate feasibility (High, Medium, Low) and identify technical risks.
4. Read existing files if necessary using read_file or list_directory.
5. Present a comprehensive technology review.
Always state your findings clearly and transfer control back to the CEO agent when done.""",
    tools=[
        FunctionTool(list_directory),
        FunctionTool(read_file)
    ],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent
)

cmo_agent = Agent(
    name="cmo_agent",
    model=model_instance,
    description="Chief Marketing Officer. Conducts market research, competitor analysis, customer segment trends, and SWOT.",
    instruction="""You are the Chief Marketing Officer (CMO) of the board.
Your job is to analyze the market positioning and customer demand.
You must:
1. Conduct market research using the market_research tool.
2. Identify at least 3 direct competitors and map out market trends.
3. Create a comprehensive SWOT analysis list (Strengths, Weaknesses, Opportunities, Threats).
4. Browse external sites if needed using the browse_web tool.
5. Present your market research report.
Always transfer control back to the CEO agent when done.""",
    tools=[
        FunctionTool(market_research),
        FunctionTool(browse_web)
    ],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent
)

coo_agent = Agent(
    name="coo_agent",
    model=model_instance,
    description="Chief Operating Officer. Develops project timelines, operational planning, resource allocation, and identifies execution bottlenecks.",
    instruction="""You are the Chief Operating Officer (COO) of the board.
Your job is to plan the operational execution.
You must:
1. Define a step-by-step project timeline/action plan (Phases 1, 2, and 3).
2. Detail resource allocation (human, operational tools, equipment).
3. Identify operational bottlenecks and regulatory hurdles.
4. Write operational timeline guidelines using the write_file tool if needed.
5. Present a structured execution plan.
Always transfer control back to the CEO agent when done.""",
    tools=[
        FunctionTool(write_file)
    ],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent
)

legal_agent = Agent(
    name="legal_agent",
    model=model_instance,
    description="Legal and Compliance Officer. Validates security policies, regulatory compliance, and business liability.",
    instruction="""You are the Legal & Compliance Officer of the board.
Your job is to validate business risks, data privacy (GDPR, CCPA), and security concerns.
You must:
1. Identify compliance issues and legal risks (intellectual property, data storage).
2. Recommend security controls (encryption, access management).
3. Browse the web for regulatory standards if needed.
4. Present a legal clearance report.
Always transfer control back to the CEO agent when done.""",
    tools=[
        FunctionTool(browse_web)
    ],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent
)

report_agent = Agent(
    name="report_agent",
    model=model_instance,
    description="Report Compiler. Merges board outputs and generates Markdown, PDF, and PPTX files.",
    instruction="""You are the Report Agent of the board.
Your job is to gather all debate notes and compile them into formal business reports.
You must:
1. Write the final report in Markdown to 'backend/static/reports/{session_id}_report.md'.
2. The report must contain: Title, Executive Summary, Decision Score, SWOT table, Risk table, Financial details, Tech stack, and Action Plan.
3. Make sure to call write_file to save the report.
Always confirm once the files are saved and return control to the CEO.""",
    tools=[
        FunctionTool(write_file)
    ],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent
)

# Root orchestrator: CEO Agent
ceo_agent = Agent(
    name="ceo_agent",
    model=model_instance,
    instruction="""You are the Chief Executive Officer (CEO) and orchestrator of BoardRoom AI.
Your goal is to guide the board to evaluate a business proposal.
Your workflow:
1. Introduce yourself and explain the evaluation plan.
2. Break down the user's business proposal.
3. Coordinate the debate by calling the sub-agents (cfo_agent, cto_agent, cmo_agent, coo_agent, legal_agent) to analyze.
4. Call each agent and wait for their report. Make sure you get input from CFO (finances), CTO (tech), CMO (market/SWOT), COO (operations/timeline), and Legal (risk/compliance).
5. Resolve any conflicts or gaps in their assessments (e.g. if the CTO proposes an expensive stack, make sure the CFO adjusts the budget).
6. Give a final Decision Score (1-100) and Recommendation.
7. Delegate to the report_agent to compile and save the reports.
8. Present the final executive summary to the user, including the filenames of the generated reports.
Always act professionally and logically.""",
    sub_agents=[cfo_agent, cto_agent, cmo_agent, coo_agent, legal_agent, report_agent],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent
)

app = App(
    root_agent=ceo_agent,
    name="boardroom_app",
)

import os
import uuid
import datetime
from typing import AsyncGenerator
from google.adk.agents import Agent, BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
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
    session_id = callback_context.state.get("session_id", "default")
    agent_name = callback_context.state.get("current_agent", "CEO")
    log_step_helper(session_id, agent_name, f"Starting analysis cycle...", "agent_start")

async def after_agent(callback_context) -> None:
    session_id = callback_context.state.get("session_id", "default")
    agent_name = callback_context.state.get("current_agent", "CEO")
    log_step_helper(session_id, agent_name, f"Completed analysis cycle.", "agent_end")

# Create specialist agents with structured output instructions
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

Your output must be structured, starting with a clear table or list of:
- Budget Required
- Estimated Revenue
- ROI (3-Year)
- Payback Period
- Financial Risks & Mitigations
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

Your output must be structured, starting with:
- Feasibility Rating (High, Medium, Low)
- Recommended Technology Stack
- Estimated Engineering Effort
- Technical Risks & Scalability Plan
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

Your output must be structured, starting with:
- Market Trends
- Competitor Landscape (at least 3 competitors)
- SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)
- Go-To-Market (GTM) Strategy
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

Your output must be structured, starting with:
- Step-by-Step Implementation Phases (Phase 1, Phase 2, Phase 3)
- Resource Allocation (roles, tools, etc.)
- Operational Bottlenecks & Execution Risks
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

Your output must be structured, starting with:
- Compliance Risks (GDPR, CCPA)
- Regulatory Concerns & Data Storage Issues
- Recommended Security Controls & Clearance Rating
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

class BoardroomOrchestrator(BaseAgent):
    """Custom BaseAgent that orchestrates a real collaborative board meeting debate."""
    def __init__(self, name: str, model, sub_agents: list, **kwargs):
        super().__init__(name=name, **kwargs)
        object.__setattr__(self, 'model', model)
        object.__setattr__(self, 'sub_agents', sub_agents)
        
        object.__setattr__(self, 'cfo', next(a for a in sub_agents if a.name == "cfo_agent"))
        object.__setattr__(self, 'cto', next(a for a in sub_agents if a.name == "cto_agent"))
        object.__setattr__(self, 'cmo', next(a for a in sub_agents if a.name == "cmo_agent"))
        object.__setattr__(self, 'coo', next(a for a in sub_agents if a.name == "coo_agent"))
        object.__setattr__(self, 'legal', next(a for a in sub_agents if a.name == "legal_agent"))
        object.__setattr__(self, 'report_agent', next(a for a in sub_agents if a.name == "report_agent"))
        
        # CEO inner LLM agent to handle dialogs
        ceo_inner_agent = Agent(
            name="ceo_orchestrator",
            model=model,
            instruction="""You are the Chief Executive Officer (CEO) and orchestrator of BoardRoom AI.
Your goal is to guide the board to evaluate a business proposal.
Decompose the proposal into specific specialist briefs, coordinate the agenda, resolve conflicts, synthesize final votes, and output recommendations.""",
            before_agent_callback=before_agent,
            after_agent_callback=after_agent
        )
        object.__setattr__(self, 'ceo_inner', ceo_inner_agent)

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        session_id = ctx.state.get("session_id", "default")
        
        # 1. CEO Briefing & Decomposition
        ctx.state["current_agent"] = "CEO"
        log_step_helper(session_id, "CEO", "CEO decomposing proposal and briefing board specialists...", "ceo_briefing_start")
        ctx.session.history.append(types.Content(
            role="user",
            parts=[types.Part.from_text("CEO, please introduce the boardroom agenda and decompose the user's business proposal. Highlight the core goal and assign initial review targets to each specialist.")]
        ))
        async for event in self.ceo_inner.run_async(ctx):
            yield event
        log_step_helper(session_id, "CEO", "CEO completed initial briefing.", "ceo_briefing_done")

        # 2. Specialist Round
        specialists = [
            (self.cmo, "CMO", "CMO, please analyze the market opportunity, map competitor landscape, outline SWOT, and GTM strategy."),
            (self.cto, "CTO", "CTO, please evaluate the technical feasibility, stack scalability, effort estimation, and tech risks."),
            (self.cfo, "CFO", "CFO, please calculate financial KPIs (ROI, payback period) using tools, generate the visualization chart, and identify budget risks."),
            (self.coo, "COO", "COO, please outline step-by-step implementation phases, resource allocation, and operational bottlenecks."),
            (self.legal, "Legal", "Legal, please evaluate regulatory compliance (GDPR/CCPA), data privacy hazards, and recommend safety controls.")
        ]
        
        for agent, name, prompt in specialists:
            ctx.state["current_agent"] = name
            log_step_helper(session_id, name, f"{name} starts analysis...", "specialist_start")
            ctx.session.history.append(types.Content(
                role="user",
                parts=[types.Part.from_text(prompt)]
            ))
            async for event in agent.run_async(ctx):
                yield event
            log_step_helper(session_id, name, f"{name} submitted structured report.", "specialist_done")

        # 3. Cross-Critique Round
        critiques = [
            (self.cfo, "CFO", "CFO, please review the CTO's stack cost and COO's resource plans. Critique whether they are financially realistic or if budget shifts are needed."),
            (self.cto, "CTO", "CTO, please review the COO's timeline. Critique whether it is technically feasible and identify bottlenecks."),
            (self.legal, "Legal", "Legal, please review the CMO's GTM model and COO's execution risks. Critique them for data privacy and compliance liabilities.")
        ]
        
        for agent, name, prompt in critiques:
            ctx.state["current_agent"] = name
            log_step_helper(session_id, name, f"{name} preparing cross-critique...", "critique_start")
            ctx.session.history.append(types.Content(
                role="user",
                parts=[types.Part.from_text(prompt)]
            ))
            async for event in agent.run_async(ctx):
                yield event
            log_step_helper(session_id, name, f"{name} submitted critique.", "critique_done")

        # 4. Voting Round
        log_step_helper(session_id, "CEO", "CEO calling for final specialist votes...", "voting_start")
        for agent, name in [(self.cfo, "CFO"), (self.cto, "CTO"), (self.cmo, "CMO"), (self.coo, "COO"), (self.legal, "Legal")]:
            ctx.state["current_agent"] = f"{name} (Vote)"
            ctx.session.history.append(types.Content(
                role="user",
                parts=[types.Part.from_text(f"{name}, state your final vote (Approve, Approve with Conditions, or Reject) with a 1-sentence business justification.")]
            ))
            async for event in agent.run_async(ctx):
                yield event

        # 5. CEO Final Synthesis
        ctx.state["current_agent"] = "CEO"
        log_step_helper(session_id, "CEO", "CEO synthesizing board consensus and final score...", "synthesis_start")
        ctx.session.history.append(types.Content(
            role="user",
            parts=[types.Part.from_text("CEO, please synthesize the board debate, summarize the votes, and output the final board recommendation, including a decision score from 1-100.")]
        ))
        async for event in self.ceo_inner.run_async(ctx):
            yield event
        log_step_helper(session_id, "CEO", "CEO completed final synthesis.", "synthesis_done")

        # 6. Report Compiler Execution
        ctx.state["current_agent"] = "Report Compiler"
        log_step_helper(session_id, "Report Compiler", "Compiling final MD report...", "report_compilation_start")
        ctx.session.history.append(types.Content(
            role="user",
            parts=[types.Part.from_text(f"Report Compiler, write the final debate summary to the Markdown file 'backend/static/reports/{session_id}_report.md' using write_file. Include Title, Executive Summary, Score, SWOT table, Risk table, Financials, Tech Stack, and Action Plan.")]
        ))
        async for event in self.report_agent.run_async(ctx):
            yield event
        log_step_helper(session_id, "Report Compiler", "Report files successfully generated.", "report_compilation_done")

# Instantiate root orchestrator CEO agent
ceo_agent = BoardroomOrchestrator(
    name="ceo_agent",
    model=model_instance,
    sub_agents=[cfo_agent, cto_agent, cmo_agent, coo_agent, legal_agent, report_agent]
)

app = App(
    root_agent=ceo_agent,
    name="boardroom_app",
)

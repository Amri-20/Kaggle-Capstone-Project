import streamlit as st

def render_landing():
    """Render the landing page for BoardRoom AI."""
    st.markdown("""
    <div class="title-banner">
        <h1>BoardRoom AI</h1>
        <p>"The AI Executive Board That Thinks Before Your Business Acts."</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write(" ")
    st.write(" ")
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### The Problem with Single-Agent AI")
        st.write("""
        When businesses evaluate new strategies, relying on a single AI chat prompt often results in biased, generic, or incomplete answers. 
        In the real corporate world, critical proposals are debated, scrutinized, and reviewed by a board of specialists before any decisions are made.
        """)
        
        st.markdown("### The BoardRoom AI Solution")
        st.write("""
        **BoardRoom AI** replicates this corporate vetting process. It deploys a team of specialized AI agents running on the **Google Agent Development Kit (ADK)**. 
        Each agent represents a specific executive role, debating your business ideas from distinct perspectives to produce a vetted, balanced recommendation.
        """)
        
        if st.button("🚀 Enter BoardRoom Dashboard", type="primary"):
            st.session_state["page"] = "auth"
            st.rerun()
            
    with col2:
        st.markdown("#### The AI Executive Board Members")
        
        st.markdown("""
        <div class="board-card">
            <span style="color:#6366F1; font-weight:bold;">👔 CEO Agent (Orchestrator)</span><br/>
            Decomposes tasks, delegates analysis, resolves specialist disagreements, and makes the final decision.
        </div>
        <div class="board-card">
            <span style="color:#10B981; font-weight:bold;">📈 CFO Agent (Finance)</span><br/>
            Evaluates initial budget requirements, projects revenues, calculates ROI, and creates financial charts.
        </div>
        <div class="board-card">
            <span style="color:#F59E0B; font-weight:bold;">💻 CTO Agent (Technology)</span><br/>
            Reviews architecture, proposes modern tech stacks, estimates effort, and scores technical feasibility.
        </div>
        <div class="board-card">
            <span style="color:#EC4899; font-weight:bold;">📢 CMO Agent (Marketing)</span><br/>
            Conducts market research, maps out competitor landscapes, and designs SWOT analysis.
        </div>
        <div class="board-card">
            <span style="color:#EF4444; font-weight:bold;">⚖️ Legal & Compliance</span><br/>
            Evaluates compliance risks, reviews data privacy laws (GDPR/CCPA), and proposes security guardrails.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("### Platform Key Features")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("🤖 **Google ADK**")
        st.write("Built on Google's new Agent Development Kit with custom multi-agent collaboration pipelines.")
    with c2:
        st.markdown("🛡️ **Enterprise Security**")
        st.write("SQLite-backed JWT authentication, strict Role-Based Access Control, and prompt injection protection.")
    with c3:
        st.markdown("🧠 **Decision Memory**")
        st.write("Long-term business context memory retrieval and audit log logging for full system accountability.")
    with c4:
        st.markdown("📄 **Vetted Reports**")
        st.write("Automatically compiles executive-ready reports in Markdown, PowerPoint (PPTX), and ReportLab PDF.")
        
    st.markdown("""
    <div class="dashboard-footer">
        BoardRoom AI - Kaggle AI Agents Capstone Project submission. Powered by Google ADK & FastAPI.
    </div>
    """, unsafe_allow_html=True)


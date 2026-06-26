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
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### 👔 Vetting Business Proposals with Multi-Agent AI")
        st.write("""
        When businesses evaluate new strategies, relying on a single AI chat prompt often results in biased, generic, or incomplete answers. 
        In the real corporate world, critical proposals are debated, scrutinized, and reviewed by a board of specialists before any decisions are made.
        """)
        st.write("""
        **BoardRoom AI** replicates this corporate vetting process. It deploys a team of specialized AI agents running on the **Google Agent Development Kit (ADK)**. 
        Each agent represents a specific executive role, debating your business ideas from distinct perspectives to produce a vetted, balanced recommendation.
        """)
        
        st.write(" ")
        
        # Onboarding Quick Start Scenarios
        st.markdown("### 🚀 One-Click Boardroom Demo Scenarios")
        st.write("Select a preset scenario below to pre-populate and enter the Boardroom immediately:")
        
        sc_col1, sc_col2 = st.columns(2)
        with sc_col1:
            if st.button("🌿 Green SaaS (Munich)", use_container_width=True, help="Carbon tracking SaaS for retail brands in Germany"):
                st.session_state["preset_scenario"] = {
                    "name": "Green Retail Delivery SaaS",
                    "proposal": "We want to launch a carbon tracking SaaS software for retail brands in Germany. The initial budget is $150k. We expect $180k year 1, $240k year 2, and $300k year 3 revenue. Review tech stack scalability and GDPR legal compliance."
                }
                st.session_state["page"] = "auth"
                st.rerun()
                
            if st.button("🩺 AI Medical IoT (Boston)", use_container_width=True, help="AI-powered medical device monitoring platform"):
                st.session_state["preset_scenario"] = {
                    "name": "AI Medical IoT Platform",
                    "proposal": "Launch a remote AI patient monitoring system for hospitals in Massachusetts. Hardware + cloud SaaS model. Initial budget is $400k. Expecting Year 1 $300k, Year 2 $600k, Year 3 $1M revenue. Analyze FDA compliance, HIPAA encryption, and backend scalability."
                }
                st.session_state["page"] = "auth"
                st.rerun()
                
        with sc_col2:
            if st.button("👗 D2C E-commerce (Tokyo)", use_container_width=True, help="Sustainable fashion direct-to-consumer store"):
                st.session_state["preset_scenario"] = {
                    "name": "D2C Sustainable Fashion Store",
                    "proposal": "Launch a direct-to-consumer sustainable apparel brand online in Japan. Budget required is $80k. Expecting $100k Year 1, $150k Year 2, and $220k Year 3 revenue. Review supplier audit requirements, marketing strategies, and Shopify integration feasibility."
                }
                st.session_state["page"] = "auth"
                st.rerun()
                
            if st.button("⚡ EV Charging Network (Austin)", use_container_width=True, help="Electric vehicle charging station logistics"):
                st.session_state["preset_scenario"] = {
                    "name": "EV Fleet Charge Grid",
                    "proposal": "Build a network of electric vehicle charging hubs for commercial delivery fleets in Texas. Initial hardware budget: $600k. Expected revenues: $250k Y1, $550k Y2, $900k Y3. Review logistics optimization, technical installation effort, and legal land leases."
                }
                st.session_state["page"] = "auth"
                st.rerun()
                
        st.write(" ")
        if st.button("🔑 Enter with Custom Proposal", type="primary", use_container_width=True):
            st.session_state["preset_scenario"] = None
            st.session_state["page"] = "auth"
            st.rerun()
            
    with col2:
        st.markdown("#### 👥 Meet The AI Executive Board")
        
        st.markdown("""
        <div class="executive-card" style="border-left-color: #6366F1;">
            <div class="executive-avatar avatar-ceo">
                <i class="fa-solid fa-user-tie"></i>
            </div>
            <div class="executive-info">
                <div class="executive-title" style="color: #818CF8;">CEO Agent</div>
                <div class="executive-role">Chief Executive Officer</div>
                <div class="executive-desc">Task planner and orchestrator. Decomposes the business goals, assigns sub-tasks to specialists, and resolves conflicting board recommendations.</div>
            </div>
        </div>
        
        <div class="executive-card" style="border-left-color: #10B981;">
            <div class="executive-avatar avatar-cfo">
                <i class="fa-solid fa-coins"></i>
            </div>
            <div class="executive-info">
                <div class="executive-title" style="color: #34D399;">CFO Agent</div>
                <div class="executive-role">Chief Financial Officer</div>
                <div class="executive-desc">Financial models and KPIs. Reviews the budget, projects 3-year revenues, calculates ROI, and estimates payback timelines.</div>
            </div>
        </div>
        
        <div class="executive-card" style="border-left-color: #F59E0B;">
            <div class="executive-avatar avatar-cto">
                <i class="fa-solid fa-laptop-code"></i>
            </div>
            <div class="executive-info">
                <div class="executive-title" style="color: #FBBF24;">CTO Agent</div>
                <div class="executive-role">Chief Technology Officer</div>
                <div class="executive-desc">Technical implementation review. Proposes modern, scalable technology stacks and estimates engineering timeline effort.</div>
            </div>
        </div>
        
        <div class="executive-card" style="border-left-color: #EC4899;">
            <div class="executive-avatar avatar-cmo">
                <i class="fa-solid fa-bullhorn"></i>
            </div>
            <div class="executive-info">
                <div class="executive-title" style="color: #F472B6;">CMO Agent</div>
                <div class="executive-role">Chief Marketing Officer</div>
                <div class="executive-desc">Market analysis and customer demand. Researches the competitor landscape and drafts the SWOT grid.</div>
            </div>
        </div>
        
        <div class="executive-card" style="border-left-color: #EF4444;">
            <div class="executive-avatar avatar-legal">
                <i class="fa-solid fa-scale-balanced"></i>
            </div>
            <div class="executive-info">
                <div class="executive-title" style="color: #F87171;">Legal Agent</div>
                <div class="executive-role">General Counsel</div>
                <div class="executive-desc">Compliance risk assessment. Reviews data privacy regulation frameworks (GDPR/HIPAA) and advises on business liability.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("### Platform Key Features")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("🧩 **Google ADK Core**")
        st.write("Leverages Vertex AI Gemini models and asynchronous coordination runners.")
    with c2:
        st.markdown("🛡️ **Enterprise Security**")
        st.write("JWT-secured sessions, strict Role-Based Access Controls, and injection filters.")
    with c3:
        st.markdown("🧠 **Memory Bank**")
        st.write("Saves past strategic decisions and audits for full platform compliance.")
    with c4:
        st.markdown("📈 **Automated Reports**")
        st.write("Compiles executive-ready PowerPoint decks and ReportLab PDF documents.")
        
    st.markdown("""
    <div class="dashboard-footer">
        BoardRoom AI - Kaggle AI Agents Capstone Project. Powered by Google ADK & FastAPI.
    </div>
    """, unsafe_allow_html=True)

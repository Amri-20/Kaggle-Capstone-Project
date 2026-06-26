import streamlit as st
import requests
import time
import os
import sqlite3

API_URL = "http://localhost:8000/api"
STATIC_URL = "http://localhost:8000/static"

def render_dashboard():
    """Render the primary BoardRoom AI Decision Dashboard."""
    # Check if authenticated
    token = st.session_state.get("token")
    username = st.session_state.get("username", "Guest")
    role = st.session_state.get("role", "viewer")
    
    if not token:
        st.error("Access denied. Please log in.")
        st.session_state["page"] = "auth"
        st.rerun()
        return

    # Header section
    col_header, col_logout = st.columns([4, 1])
    with col_header:
        st.markdown(f"<h2>Executive Decision Room</h2>", unsafe_allow_html=True)
        st.write(f"Logged in as: **{username}** | Role: **{role.upper()}**")
    with col_logout:
        if st.button("?? Log Out", use_container_width=True):
            st.session_state["token"] = None
            st.session_state["username"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "landing"
            st.session_state["active_session_id"] = None
            st.rerun()
            
    st.write(" ")
    
    # Sidebar navigation tabs
    menu_selection = st.sidebar.radio("Navigation", [
        "?? Start Evaluation",
        "?? Session History",
        "?? Pending Approvals",
        "?? Memory Bank",
        "?? Platform Audit Logs"
    ])
    
    # ================= 1. START EVALUATION =================
    if menu_selection == "?? Start Evaluation":
        st.markdown("### Evaluate New Business Idea")
        st.write("Submit a proposal to initiate an executive debate among your AI board members.")
        
        proj_name = st.text_input("Project Name", placeholder="e.g., Green SaaS Expansion 2026")
        proposal_text = st.text_area("Business Idea Details", height=150, 
                                     placeholder="e.g., We want to launch a carbon tracking SaaS software for retail brands in Germany. The initial budget is $150k. We expect $180k year 1, $240k year 2, and $300k year 3 revenue. Review tech stack scalability and GDPR legal compliance.")
        
        uploaded_file = st.file_uploader("Attach Reference Documents (PDF, DOCX, CSV, Excel, TXT)", type=["pdf", "docx", "csv", "xlsx", "txt"])
        
        doc_id = None
        if uploaded_file:
            # Upload file to FastAPI
            if st.session_state.get("uploaded_file_name") != uploaded_file.name:
                with st.spinner("Analyzing uploaded document..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                        res = requests.post(f"{API_URL}/board/upload", files=files)
                        if res.status_code == 200:
                            data = res.json()
                            doc_id = data["document_id"]
                            st.session_state["uploaded_doc_id"] = doc_id
                            st.session_state["uploaded_file_name"] = uploaded_file.name
                            st.success(f"Analyzed {uploaded_file.name} successfully!")
                        else:
                            st.error("Failed to parse file.")
                    except Exception as e:
                        st.error(f"Upload error: {str(e)}")
            else:
                doc_id = st.session_state.get("uploaded_doc_id")
        
        if st.button("?? Initiate Board Debate", type="primary", use_container_width=True):
            if not proj_name or not proposal_text:
                st.error("Please provide both Project Name and Proposal Details.")
            else:
                with st.spinner("Conceiving agenda and waking board members..."):
                    try:
                        headers = {"Authorization": f"Bearer {token}"}
                        payload = {
                            "name": proj_name,
                            "proposal": proposal_text,
                            "context_document_id": doc_id
                        }
                        res = requests.post(f"{API_URL}/board/start", json=payload, headers=headers)
                        if res.status_code == 200:
                            session_id = res.json()["session_id"]
                            st.session_state["active_session_id"] = session_id
                            st.success("Board meeting started! Redirecting to monitor...")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(res.json().get("detail", "Failed to start board run."))
                    except Exception as e:
                        st.error(f"Error starting board: {str(e)}")
                        
        # Active session monitoring
        active_sess_id = st.session_state.get("active_session_id")
        if active_sess_id:
            st.markdown("---")
            st.markdown(f"### Current Active Session: `{active_sess_id[:8]}`")
            
            # Fetch timeline and logs
            try:
                timeline_res = requests.get(f"{API_URL}/board/session/{active_sess_id}/timeline")
                msg_res = requests.get(f"{API_URL}/board/session/{active_sess_id}/messages")
                
                t_list = timeline_res.json() if timeline_res.status_code == 200 else []
                m_list = msg_res.json() if msg_res.status_code == 200 else []
                
                col_tl, col_msgs = st.columns([1, 2.2])
                
                with col_tl:
                    st.markdown("#### Execution Timeline")
                    if not t_list:
                        st.info("Starting up...")
                    for item in t_list:
                        st.markdown(f"""
                        <div class="timeline-item">
                            <div class="timeline-timestamp">{item['timestamp'][11:19]}</div>
                            <b>{item['agent_name']}</b>: {item['message']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                with col_msgs:
                    st.markdown("#### Agent Dialogue & Arguments")
                    if not m_list:
                        st.info("Waiting for board debate transcripts...")
                    for m in m_list:
                        cls = ""
                        author = m["sender"].lower()
                        if "ceo" in author: cls = "agent-ceo"
                        elif "cfo" in author: cls = "agent-cfo"
                        elif "cto" in author: cls = "agent-cto"
                        elif "cmo" in author: cls = "agent-cmo"
                        elif "coo" in author: cls = "agent-coo"
                        elif "legal" in author: cls = "agent-legal"
                        elif "report" in author: cls = "agent-report"
                        
                        st.markdown(f"""
                        <div class="message-container">
                            <div class="agent-header {cls}">{m['sender']}</div>
                            <div class="message-bubble">{m['content']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                # Check session status
                history_res = requests.get(f"{API_URL}/board/sessions")
                if history_res.status_code == 200:
                    for s in history_res.json():
                        if s["id"] == active_sess_id:
                            if s["status"] == "completed":
                                st.balloons()
                                st.success("Evaluation completed! Report files are ready below.")
                                # Render downloads
                                c1, c2, c3 = st.columns(3)
                                with c1:
                                    st.link_button("?? Download PDF", f"{API_URL}/reports/download/{active_sess_id}/pdf", use_container_width=True)
                                with c2:
                                    st.link_button("?? Download PPTX", f"{API_URL}/reports/download/{active_sess_id}/pptx", use_container_width=True)
                                with c3:
                                    st.link_button("?? Download Markdown", f"{API_URL}/reports/download/{active_sess_id}/md", use_container_width=True)
                                    
                                # Show chart
                                st.markdown("#### Projections Visualizer")
                                st.image(f"{STATIC_URL}/charts/{active_sess_id}_chart.png", caption="BoardRoom AI Projected Projections", use_container_width=True)
                                st.session_state["active_session_id"] = None
                            elif s["status"] == "failed":
                                st.error("Board session execution failed. Please verify credentials or logs.")
                                st.session_state["active_session_id"] = None
                                
            except Exception as e:
                st.error(f"Error reading timeline: {e}")
                
            # Quick Refresh Button
            st.button("?? Refresh Timeline & Dialogs")

    # ================= 2. SESSION HISTORY =================
    elif menu_selection == "?? Session History":
        st.markdown("### Past Board Evaluations")
        st.write("Browse all past executive reviews and download their completed strategy packages.")
        
        try:
            res = requests.get(f"{API_URL}/board/sessions")
            if res.status_code == 200:
                sessions = res.json()
                if not sessions:
                    st.info("No evaluations run yet.")
                for s in sessions:
                    status_cls = "status-active" if s['status'] == "completed" else ("status-pending" if s['status'] == "running" else "status-failed")
                    st.markdown(f"""
                    <div class="board-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h4>?? {s['name']}</h4>
                            <span class="status-badge {status_cls}">{s['status'].upper()}</span>
                        </div>
                        <p style="font-size:0.85rem; color:#94A3B8; margin-top:2px;">Session ID: {s['id']} | Created: {s['created_at'][:19]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # If completed, show downloads
                    if s['status'] == "completed":
                        c1, c2, c3, c4 = st.columns([1, 1, 1, 1.2])
                        with c1:
                            st.link_button("PDF Report", f"{API_URL}/reports/download/{s['id']}/pdf", use_container_width=True)
                        with c2:
                            st.link_button("PPTX Slides", f"{API_URL}/reports/download/{s['id']}/pptx", use_container_width=True)
                        with c3:
                            st.link_button("Markdown", f"{API_URL}/reports/download/{s['id']}/md", use_container_width=True)
                        with c4:
                            if st.button("?? View Dialogs", key=f"v_{s['id']}", use_container_width=True):
                                st.session_state["active_session_id"] = s["id"]
                                st.session_state["page"] = "dashboard"
                                st.rerun()
                        st.write(" ")
            else:
                st.error("Failed to load history.")
        except Exception as e:
            st.error(f"Connection error: {e}")

    # ================= 3. PENDING APPROVALS =================
    elif menu_selection == "?? Pending Approvals":
        st.markdown("### Human Approval Workflows")
        st.write("Manager and Admin roles can audit and release budget contracts or sensitive transaction operations requested by board agents.")
        
        if role not in ["admin", "manager"]:
            st.warning("?? Insufficient Permissions. Your role must be MANAGER or ADMIN to resolve action approvals.")
        else:
            try:
                res = requests.get(f"{API_URL}/board/approvals")
                if res.status_code == 200:
                    approvals = res.json()
                    if not approvals:
                        st.success("?? All actions approved! No pending requests.")
                    for app in approvals:
                        st.markdown(f"""
                        <div class="board-card">
                            <h4>?? sensitive action: {app['tool_name']}</h4>
                            <p><b>Session ID:</b> {app['session_id']}</p>
                            <p><b>Request ID:</b> {app['id']}</p>
                            <p><b>Arguments:</b> <code style='color:#38BDF8;'>{app['arguments']}</code></p>
                            <p><b>Requested At:</b> {app['requested_at'][:19]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        c_app, c_rej = st.columns(2)
                        with c_app:
                            if st.button("? Approve Action", key=f"app_{app['id']}", use_container_width=True):
                                resolve_res = requests.post(f"{API_URL}/board/approve/{app['id']}", json={
                                    "status": "approved",
                                    "resolver_username": username
                                })
                                if resolve_res.status_code == 200:
                                    st.success("Action Approved successfully!")
                                    st.rerun()
                        with c_rej:
                            if st.button("? Reject Action", key=f"rej_{app['id']}", use_container_width=True):
                                resolve_res = requests.post(f"{API_URL}/board/approve/{app['id']}", json={
                                    "status": "rejected",
                                    "resolver_username": username
                                })
                                if resolve_res.status_code == 200:
                                    st.warning("Action Rejected.")
                                    st.rerun()
                else:
                    st.error("Failed to load approvals.")
            except Exception as e:
                st.error(f"Error: {e}")

    # ================= 4. MEMORY BANK =================
    elif menu_selection == "?? Memory Bank":
        st.markdown("### Business & Decision Memory")
        st.write("Browse structured facts, user preferences, and strategic decision outcomes remembered across board sessions.")
        
        search_q = st.text_input("?? Search Memory Bank", placeholder="e.g., retail expansion GDPR")
        if search_q:
            try:
                res = requests.get(f"{API_URL}/memory/search", params={"query": search_q})
                if res.status_code == 200:
                    items = res.json()
                    st.write(f"Found **{len(items)}** matching memories:")
                    for it in items:
                        st.markdown(f"""
                        <div class="board-card" style="border-left: 4px solid #0284C7;">
                            <div style="display:flex; justify-content:space-between;">
                                <b>?? {it['key']}</b>
                                <span style="font-size:0.8rem; color:#64748B;">Score: {it['score']:.2f}</span>
                            </div>
                            <p style="margin-top:6px; color:#E2E8F0;">{it['value']}</p>
                            <p style="font-size:0.75rem; color:#64748B; margin-top:2px;">Category: {it['category'].upper()} | Saved: {it['created_at'][:19]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Search failed.")
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            try:
                res = requests.get(f"{API_URL}/memory/all")
                if res.status_code == 200:
                    items = res.json()
                    if not items:
                        st.info("No memories stored yet.")
                    for it in items:
                        st.markdown(f"""
                        <div class="board-card" style="border-left: 4px solid #0284C7;">
                            <b>?? {it['key']}</b>
                            <p style="margin-top:6px; color:#E2E8F0;">{it['value']}</p>
                            <p style="font-size:0.75rem; color:#64748B; margin-top:2px;">Category: {it['category'].upper()} | Saved: {it['created_at'][:19]}</p>
                        </div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Connection error: {e}")

    # ================= 5. PLATFORM AUDIT LOGS =================
    elif menu_selection == "?? Platform Audit Logs":
        st.markdown("### Security Compliance Audit Logs")
        st.write("Full accountability record of user sign-ins, prompt injection triggers, database initializations, and approvals.")
        
        if role != "admin":
            st.warning("?? Access Blocked. Platform audit logs are reserved for the Admin role only.")
        else:
            try:
                db_path = "boardroom.db"
                if os.path.exists(db_path):
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, username, action, details, timestamp FROM audit_logs ORDER BY timestamp DESC LIMIT 50")
                    logs = cursor.fetchall()
                    conn.close()
                    
                    if not logs:
                        st.info("No security events logged.")
                    for log in logs:
                        l_id, l_usr, l_act, l_det, l_ts = log
                        st.markdown(f"""
                        <div style="font-family:monospace; padding:8px; border-bottom:1px solid rgba(255,255,255,0.05); font-size:0.85rem;">
                            <span style="color:#64748B;">[{l_ts[:19]}]</span> 
                            <span style="color:#10B981; font-weight:bold;">{l_usr}</span> - 
                            <span style="color:#E2E8F0; font-weight:bold;">{l_act.upper()}</span>: 
                            <span style="color:#94A3B8;">{l_det}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No audit logs database found.")
            except Exception as e:
                st.error(f"Failed to query audit logs: {e}")

    st.markdown("""
    <div class="dashboard-footer">
        BoardRoom AI - Kaggle AI Agents Capstone Project. Premium UI Theme.
    </div>
    """, unsafe_allow_html=True)

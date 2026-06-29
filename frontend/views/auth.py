import streamlit as st
import requests

API_URL = "http://localhost:8000/api"

def render_auth():
    """Render Login and Register page."""
    st.markdown("<h2 style='text-align: center;'>Platform Authentication</h2>", unsafe_allow_html=True)
    st.write(" ")
    
    tab1, tab2 = st.tabs(["🔑 Log In", "📝 Register"])
    
    with tab1:
        st.markdown("### Sign In to BoardRoom AI")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_pwd")
        
        if st.button("Log In", type="primary", key="btn_login"):
            if not username or not password:
                st.error("Please fill in all fields.")
            else:
                try:
                    res = requests.post(f"{API_URL}/auth/login", json={
                        "username": username,
                        "password": password
                    })
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state["token"] = data["access_token"]
                        st.session_state["username"] = data["username"]
                        st.session_state["role"] = data["role"]
                        st.session_state["page"] = "dashboard"
                        st.success("Successfully logged in!")
                        st.rerun()
                    else:
                        st.error(res.json().get("detail", "Invalid credentials."))
                except Exception as e:
                    st.error(f"Cannot connect to backend: {str(e)}")
                    
    with tab2:
        st.markdown("### Create New Account")
        reg_username = st.text_input("Choose Username", key="reg_username")
        reg_pwd = st.text_input("Choose Password", type="password", key="reg_pwd")
        reg_role = st.selectbox("Role", ["viewer", "manager", "admin"], key="reg_role")
        
        if st.button("Register", key="btn_register"):
            if not reg_username or not reg_pwd:
                st.error("Please fill in all fields.")
            else:
                try:
                    res = requests.post(f"{API_URL}/auth/register", json={
                        "username": reg_username,
                        "password": reg_pwd,
                        "role": reg_role
                    })
                    if res.status_code == 200:
                        st.success("Registration successful! Please log in.")
                    else:
                        st.error(res.json().get("detail", "Registration failed."))
                except Exception as e:
                    st.error(f"Cannot connect to backend: {str(e)}")
                    
    if st.button("⬅️ Back to Landing Page"):
        st.session_state["page"] = "landing"
        st.rerun()


import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Configure page layout and style
st.set_page_config(
    page_title="BoardRoom AI - Decision Dashboard",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Styling
from frontend.components.styles import apply_custom_css
apply_custom_css()

# Import Page Renderers
from frontend.pages.landing import render_landing
from frontend.pages.auth import render_auth
from frontend.pages.dashboard import render_dashboard

# Initialize Session State Variables
if "page" not in st.session_state:
    st.session_state["page"] = "landing"
if "token" not in st.session_state:
    st.session_state["token"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
if "active_session_id" not in st.session_state:
    st.session_state["active_session_id"] = None

# Routing Logic
current_page = st.session_state["page"]

if current_page == "landing":
    render_landing()
elif current_page == "auth":
    render_auth()
elif current_page == "dashboard":
    render_dashboard()

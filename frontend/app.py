import streamlit as st

# Configure page layout and style
st.set_page_config(
    page_title="BoardRoom AI - Decision Dashboard",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Styling
from components.styles import apply_custom_css
apply_custom_css()

# Import Page Renderers
from views.landing import render_landing
from views.auth import render_auth
from views.dashboard import render_dashboard

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


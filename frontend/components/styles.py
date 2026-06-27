import streamlit as st

def apply_custom_css():
    """Inject premium CSS styling into Streamlit for BoardRoom AI."""
    css = """<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
    /* Main App Config */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    /* Heading Fonts */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.02em;
    }
    /* Custom Title Banner */
    .title-banner {
        background: linear-gradient(135deg, #0369A1 0%, #2563EB 50%, #4F46E5 100%);
        padding: 35px;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.2);
        margin-bottom: 30px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .title-banner h1 {
        margin: 0;
        font-size: 3rem !important;
        letter-spacing: -0.05em;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    .title-banner p {
        margin: 10px 0 0 0;
        font-size: 1.2rem;
        color: #E2E8F0;
        opacity: 0.95;
    }
    /* Premium Dashboard Cards */
    .board-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18);
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .board-card:hover {
        transform: translateY(-3px);
        border-color: rgba(37, 99, 235, 0.45);
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.15);
    }
    /* Status Badge styling */
    .status-badge {
        padding: 5px 12px;
        border-radius: 24px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .status-active, .status-completed {
        background-color: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .status-pending, .status-running {
        background-color: rgba(245, 158, 11, 0.12);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.25);
    }
    .status-failed {
        background-color: rgba(239, 68, 68, 0.12);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.25);
    }
    /* Agent Message Bubbles */
    .message-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 16px;
    }
    .agent-header {
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 6px;
        padding-left: 4px;
        letter-spacing: 0.02em;
    }
    .message-bubble {
        background: rgba(30, 41, 59, 0.4);
        border-left: 4px solid #38BDF8;
        border-radius: 0 12px 12px 12px;
        padding: 15px 20px;
        color: #E2E8F0;
        font-size: 0.98rem;
        line-height: 1.6;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border-right: 1px solid rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }
    /* Colors per Agent */
    .agent-ceo { color: #818CF8 !important; border-color: #818CF8 !important; }
    .agent-cfo { color: #34D399 !important; border-color: #34D399 !important; }
    .agent-cto { color: #FBBF24 !important; border-color: #FBBF24 !important; }
    .agent-cmo { color: #F472B6 !important; border-color: #F472B6 !important; }
    .agent-coo { color: #A78BFA !important; border-color: #A78BFA !important; }
    .agent-legal { color: #F87171 !important; border-color: #F87171 !important; }
    .agent-report { color: #22D3EE !important; border-color: #22D3EE !important; }
    
    /* Timeline styles */
    .timeline-item {
        border-left: 2px solid #2563EB;
        padding-left: 22px;
        position: relative;
        margin-bottom: 18px;
        font-size: 0.92rem;
    }
    .timeline-item::before {
        content: '';
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #2563EB;
        position: absolute;
        left: -7px;
        top: 4px;
        box-shadow: 0 0 10px #2563EB;
    }
    .timeline-timestamp {
        color: #64748B;
        font-size: 0.78rem;
        margin-bottom: 3px;
        font-weight: 500;
    }
    /* Footer */
    .dashboard-footer {
        text-align: center;
        padding: 30px;
        margin-top: 60px;
        font-size: 0.85rem;
        color: #475569;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>"""
    st.markdown(css, unsafe_allow_html=True)

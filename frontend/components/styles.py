import streamlit as st

def apply_custom_css():
    """Inject premium CSS styling into Streamlit for BoardRoom AI."""
    css = """
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
    /* Main App Config */
    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Heading Fonts */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }
    
    /* Custom Title Banner */
    .title-banner {
        background: linear-gradient(135deg, #0284C7 0%, #3B82F6 50%, #6366F1 100%);
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.25);
        margin-bottom: 25px;
        text-align: center;
    }
    .title-banner h1 {
        margin: 0;
        font-size: 2.8rem !important;
        letter-spacing: -0.05em;
    }
    .title-banner p {
        margin: 8px 0 0 0;
        font-size: 1.1rem;
        color: #E2E8F0;
        opacity: 0.9;
    }
    
    /* Premium Dashboard Cards */
    .board-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .board-card:hover {
        transform: translateY(-2px);
        border-color: rgba(59, 130, 246, 0.4);
    }
    
    /* Status Badge styling */
    .status-badge {
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    .status-active {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .status-pending {
        background-color: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .status-failed {
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Agent Message Bubbles */
    .message-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 12px;
    }
    .agent-header {
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 4px;
        color: #38BDF8;
    }
    .message-bubble {
        background: #1E293B;
        border-left: 4px solid #38BDF8;
        border-radius: 0 8px 8px 8px;
        padding: 12px 16px;
        color: #E2E8F0;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Colors per Agent */
    .agent-ceo { color: #6366F1; border-color: #6366F1 !important; }
    .agent-cfo { color: #10B981; border-color: #10B981 !important; }
    .agent-cto { color: #F59E0B; border-color: #F59E0B !important; }
    .agent-cmo { color: #EC4899; border-color: #EC4899 !important; }
    .agent-coo { color: #8B5CF6; border-color: #8B5CF6 !important; }
    .agent-legal { color: #EF4444; border-color: #EF4444 !important; }
    .agent-report { color: #06B6D4; border-color: #06B6D4 !important; }
    
    /* Timeline styles */
    .timeline-item {
        border-left: 2px solid #3B82F6;
        padding-left: 20px;
        position: relative;
        margin-bottom: 15px;
        font-size: 0.9rem;
    }
    .timeline-item::before {
        content: '';
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #3B82F6;
        position: absolute;
        left: -6px;
        top: 4px;
        box-shadow: 0 0 8px #3B82F6;
    }
    .timeline-timestamp {
        color: #94A3B8;
        font-size: 0.75rem;
        margin-bottom: 2px;
    }
    
    /* Footer */
    .dashboard-footer {
        text-align: center;
        padding: 25px;
        margin-top: 50px;
        font-size: 0.8rem;
        color: #64748B;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

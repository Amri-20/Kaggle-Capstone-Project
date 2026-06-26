import streamlit as st

def apply_custom_css():
    """Inject premium CSS styling into Streamlit for BoardRoom AI."""
    css = """
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
    /* Main App Config */
    .stApp {
        background-color: #080B11;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
            radial-gradient(at 50% 0%, rgba(59, 130, 246, 0.05) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.05) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.03) 0px, transparent 50%);
        color: #F8FAFC;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Heading Fonts */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.02em !important;
    }
    
    /* Custom Title Banner */
    .title-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-bottom: 2px solid #3B82F6;
        padding: 35px 25px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        margin-bottom: 30px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .title-banner::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.6), transparent);
    }
    .title-banner h1 {
        margin: 0;
        font-size: 3.2rem !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .title-banner p {
        margin: 10px 0 0 0;
        font-size: 1.25rem;
        color: #38BDF8;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    /* Premium Dashboard Cards */
    .board-card {
        background: rgba(17, 24, 39, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .board-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 16px;
        border: 1px solid transparent;
        background: linear-gradient(135deg, rgba(255,255,255,0.08), transparent) border-box;
        -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: destination-out;
        mask-composite: exclude;
        pointer-events: none;
    }
    .board-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.15);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    /* Executive Agent Cards */
    .executive-card {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        background: rgba(22, 28, 45, 0.65);
        border-left: 4px solid #64748B;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: transform 0.2s ease;
    }
    .executive-card:hover {
        transform: scale(1.02);
    }
    .executive-avatar {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50%;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        flex-shrink: 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .executive-info {
        flex-grow: 1;
    }
    .executive-title {
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 2px;
    }
    .executive-role {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .executive-desc {
        font-size: 0.85rem;
        color: #CBD5E1;
        line-height: 1.4;
    }
    
    /* Agent Message Bubbles */
    .message-container {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        animation: fadeIn 0.4s ease-out;
    }
    .message-avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.15rem;
        flex-shrink: 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .message-body {
        flex-grow: 1;
    }
    .agent-header {
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .message-bubble {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 0 16px 16px 16px;
        padding: 16px;
        color: #E2E8F0;
        font-size: 0.95rem;
        line-height: 1.5;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    /* Specific bubble left borders per agent */
    .bubble-ceo { border-left: 4px solid #6366F1 !important; }
    .bubble-cfo { border-left: 4px solid #10B981 !important; }
    .bubble-cto { border-left: 4px solid #F59E0B !important; }
    .bubble-cmo { border-left: 4px solid #EC4899 !important; }
    .bubble-coo { border-left: 4px solid #8B5CF6 !important; }
    .bubble-legal { border-left: 4px solid #EF4444 !important; }
    .bubble-report { border-left: 4px solid #06B6D4 !important; }
    
    .avatar-ceo { background: rgba(99, 102, 241, 0.15); color: #818CF8; border: 1px solid rgba(99, 102, 241, 0.3); }
    .avatar-cfo { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .avatar-cto { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .avatar-cmo { background: rgba(236, 72, 153, 0.15); color: #F472B6; border: 1px solid rgba(236, 72, 153, 0.3); }
    .avatar-coo { background: rgba(139, 92, 246, 0.15); color: #A78BFA; border: 1px solid rgba(139, 92, 246, 0.3); }
    .avatar-legal { background: rgba(239, 68, 68, 0.15); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .avatar-report { background: rgba(6, 182, 212, 0.15); color: #22D3EE; border: 1px solid rgba(6, 182, 212, 0.3); }
    
    /* Interactive Timeline */
    .timeline-item {
        border-left: 2px solid rgba(59, 130, 246, 0.3);
        padding-left: 20px;
        position: relative;
        margin-bottom: 20px;
        animation: slideIn 0.3s ease-out;
    }
    .timeline-item::before {
        content: '';
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #080B11;
        border: 2px solid #3B82F6;
        position: absolute;
        left: -8px;
        top: 3px;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.8);
        transition: all 0.3s ease;
    }
    .timeline-item.active::before {
        background: #3B82F6;
        animation: pulse 1.5s infinite;
    }
    .timeline-item.complete::before {
        background: #10B981;
        border-color: #10B981;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.8);
    }
    .timeline-timestamp {
        color: #64748B;
        font-size: 0.75rem;
        margin-bottom: 2px;
        font-family: monospace;
    }
    
    /* Metrics grid badges */
    .metric-badge-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin-bottom: 25px;
    }
    .metric-badge-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .metric-badge-val {
        font-family: 'Outfit', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 4px;
    }
    .metric-badge-lbl {
        font-size: 0.8rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Status Badges */
    .status-badge {
        padding: 6px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .status-badge.completed {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .status-badge.running {
        background: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.3);
        animation: pulse 2s infinite;
    }
    .status-badge.failed {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Quick Start Demo Scenario Cards */
    .scenario-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 16px;
        margin-bottom: 25px;
    }
    .scenario-card {
        background: rgba(30, 41, 59, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 16px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .scenario-card:hover {
        background: rgba(59, 130, 246, 0.1);
        border-color: rgba(59, 130, 246, 0.3);
        transform: translateY(-2px);
    }
    .scenario-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #FFFFFF;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .scenario-desc {
        font-size: 0.8rem;
        color: #94A3B8;
        line-height: 1.4;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0% { opacity: 0.6; box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
        70% { opacity: 1; box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
        100% { opacity: 0.6; box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
    }
    
    /* Footer */
    .dashboard-footer {
        text-align: center;
        padding: 30px;
        margin-top: 60px;
        font-size: 0.8rem;
        color: #475569;
        border-top: 1px solid rgba(255, 255, 255, 0.04);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

import streamlit as st

def apply_custom_css() -> None:
    """Injects custom CSS to style the Streamlit app with premium glassmorphism and dark mode elements."""
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <style>
            /* Apply custom typography */
            html, body, [class*="css"], .stApp {
                font-family: 'Outfit', sans-serif;
            }
            
            /* Custom dark theme colors & glassmorphism backgrounds */
            .stApp {
                background: radial-gradient(circle at top right, #1a2238 0%, #0d111d 100%);
                color: #e2e8f0;
            }
            
            /* Clean Sidebar styling */
            section[data-testid="stSidebar"] {
                background-color: rgba(17, 24, 39, 0.85);
                backdrop-filter: blur(12px);
                border-right: 1px solid rgba(255, 255, 255, 0.05);
            }
            
            section[data-testid="stSidebar"] .stMarkdown {
                color: #e2e8f0;
            }
            
            /* Custom styled login container */
            .login-container {
                max-width: 420px;
                margin: 80px auto;
                padding: 40px;
                background: rgba(30, 41, 59, 0.45);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.08);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                text-align: center;
                animation: fadeIn 0.8s ease-in-out;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(15px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .login-header h2 {
                color: #f1f5f9;
                font-weight: 700;
                margin-bottom: 8px;
                background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .login-header p {
                color: #94a3b8;
                font-size: 14px;
                margin-bottom: 24px;
            }
            
            /* Custom input styling */
            .stTextInput>div>div>input {
                background-color: rgba(15, 23, 42, 0.6) !important;
                color: #f8fafc !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 10px !important;
                padding: 12px 16px !important;
                transition: all 0.3s ease !important;
            }
            
            .stTextInput>div>div>input:focus {
                border-color: #6366f1 !important;
                box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
            }
            
            /* Buttons styling */
            .stButton>button {
                background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 10px 24px !important;
                font-weight: 600 !important;
                width: 100%;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
            }
            
            .stButton>button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
                background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
            }
            
            .stButton>button:active {
                transform: translateY(1px) !important;
            }
            
            /* Citation container styling */
            .citation-container {
                margin-top: 12px;
                padding: 10px 14px;
                background: rgba(30, 41, 59, 0.4);
                border-left: 3px solid #6366f1;
                border-radius: 4px 8px 8px 4px;
                font-size: 13px;
                color: #cbd5e1;
            }
            
            .citation-title {
                font-weight: 600;
                color: #818cf8;
                margin-bottom: 4px;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            
            .citation-item {
                display: inline-flex;
                align-items: center;
                background: rgba(99, 102, 241, 0.15);
                border: 1px solid rgba(99, 102, 241, 0.3);
                border-radius: 4px;
                padding: 2px 6px;
                margin: 2px 4px 2px 0;
                font-family: monospace;
                color: #a5b4fc;
            }
            
            /* Custom chatbot messages decoration */
            div[data-testid="stChatMessage"] {
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 12px;
                border: 1px solid rgba(255, 255, 255, 0.03);
            }
            
            div[data-testid="stChatMessage"]:nth-child(even) {
                background-color: rgba(30, 41, 59, 0.35);
                backdrop-filter: blur(4px);
            }
            
            div[data-testid="stChatMessage"]:nth-child(odd) {
                background-color: rgba(15, 23, 42, 0.45);
            }
            
            /* App title banner style */
            .app-title-banner {
                background: linear-gradient(90deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.05) 100%);
                border: 1px solid rgba(255, 255, 255, 0.05);
                padding: 20px;
                border-radius: 16px;
                margin-bottom: 25px;
            }
            
            .app-title-banner h1 {
                margin: 0;
                font-size: 28px;
                font-weight: 800;
                background: linear-gradient(135deg, #a5b4fc 0%, #cbd5e1 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .app-title-banner p {
                margin: 5px 0 0 0;
                color: #94a3b8;
                font-size: 14px;
            }
            
            /* Style Streamlit headers */
            h1, h2, h3 {
                font-weight: 700 !important;
                color: #f1f5f9 !important;
            }
            
            /* Custom scrollbars */
            ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }
            ::-webkit-scrollbar-track {
                background: rgba(15, 23, 42, 0.1);
            }
            ::-webkit-scrollbar-thumb {
                background: rgba(99, 102, 241, 0.3);
                border-radius: 3px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: rgba(99, 102, 241, 0.5);
            }
        </style>
        """,
        unsafe_allow_html=True
    )

import streamlit as st
from utils.helpers import get_app_credentials

def check_credentials(username_input: str, password_input: str) -> bool:
    """Verifies user input against configured credentials."""
    correct_username, correct_password = get_app_credentials()
    return username_input == correct_username and password_input == correct_password

def show_login_page() -> bool:
    """Renders the login UI. Returns True if authenticated, False otherwise."""
    # Custom HTML container to wrapper elements
    st.markdown(
        """
        <div class="login-container">
            <div class="login-header">
                <h2>Real Estate AI Assistant</h2>
                <p>Please log in using your secure agent credentials to access the RAG system.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # We position the login form beneath the HTML header.
    # Note: Streamlit's native input elements can be nested but to align with the CSS container, 
    # we render them cleanly.
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="e.g. admin", key="user_input_val")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="pwd_input_val")
            submit_btn = st.form_submit_button("Log In")
            
            if submit_btn:
                if check_credentials(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Authentication successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid username or password. Please try again.")
                    
    return st.session_state.get("authenticated", False)

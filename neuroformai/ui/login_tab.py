import gradio as gr
from auth import AuthManager


def create_login_tab():
    """Build the Login / Signup tab."""

    with gr.Tab("Login / Signup") as tab:
        gr.Markdown("## Welcome to NeuroFormAI")
        gr.Markdown("Login or create an account to start tracking your workouts.")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Login")
                login_username = gr.Textbox(label="Username", placeholder="Enter username")
                login_password = gr.Textbox(label="Password", type="password", placeholder="Enter password")
                login_btn = gr.Button("Login", variant="primary")
                login_msg = gr.Markdown("")

            with gr.Column(scale=1):
                gr.Markdown("### Sign Up")
                signup_fullname = gr.Textbox(label="Full Name", placeholder="Enter your full name")
                signup_username = gr.Textbox(label="Username", placeholder="Choose a username (min 3 chars)")
                signup_password = gr.Textbox(label="Password", type="password", placeholder="Choose a password (min 6 chars)")
                signup_btn = gr.Button("Create Account", variant="secondary")
                signup_msg = gr.Markdown("")

        with gr.Row():
            user_status = gr.Markdown("**Status:** Not logged in")

    return {
        "tab": tab,
        "login_username": login_username,
        "login_password": login_password,
        "login_btn": login_btn,
        "login_msg": login_msg,
        "signup_fullname": signup_fullname,
        "signup_username": signup_username,
        "signup_password": signup_password,
        "signup_btn": signup_btn,
        "signup_msg": signup_msg,
        "user_status": user_status,
    }


def handle_login(username, password, session_state, browser_state):
    """Process login attempt. Saves to BrowserState on success."""
    success, message, user_data = AuthManager.login(username, password)
    if success:
        session_state = user_data
        browser_state = {"username": username, "password": password}
        status = f"**Status:** Logged in as **{user_data['full_name']}**"
        return f"✓ {message}", status, session_state, browser_state
    return f"✗ {message}", "**Status:** Not logged in", session_state, browser_state


def handle_signup(full_name, username, password, session_state, browser_state):
    """Process signup attempt. Saves to BrowserState on success."""
    success, message, user_id = AuthManager.signup(username, password, full_name)
    if success:
        session_state = {
            "user_id": user_id,
            "username": username,
            "full_name": full_name or username,
        }
        browser_state = {"username": username, "password": password}
        status = f"**Status:** Logged in as **{full_name or username}**"
        return f"✓ {message}", status, session_state, browser_state
    return f"✗ {message}", "**Status:** Not logged in", session_state, browser_state


def handle_auto_login(browser_state, session_state):
    """Auto-login from saved browser credentials on page load."""
    if not browser_state or not isinstance(browser_state, dict):
        return "**Status:** Not logged in", session_state

    username = browser_state.get("username", "")
    password = browser_state.get("password", "")

    if not username or not password:
        return "**Status:** Not logged in", session_state

    success, message, user_data = AuthManager.login(username, password)
    if success:
        session_state = user_data
        return f"**Status:** Logged in as **{user_data['full_name']}**", session_state

    return "**Status:** Not logged in", session_state

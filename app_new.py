import streamlit as st
import streamlit.components.v1 as components

# ---------------------------
# Simple in-memory user database (for demo)
# ---------------------------
if "users" not in st.session_state:
    st.session_state.users = {}  # {"username": {"password": ..., "feedback": ...}}

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None


# ---------------------------
# Navigation
# ---------------------------
def show_home():
    st.title("🏠 Home")
    st.markdown("Welcome! Use the sidebar to navigate between pages.")


def show_signup():
    st.title("📝 Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if username in st.session_state.users:
            st.error("Username already exists!")
        elif username == "" or password == "":
            st.error("Username and password cannot be empty.")
        else:
            st.session_state.users[username] = {"password": password, "feedback": ""}
            st.success("Sign up successful! Please log in.")


def show_login():
    st.title("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = st.session_state.users.get(username)
        if user and user["password"] == password:
            st.session_state.logged_in_user = username
            st.success(f"Logged in as {username}")
        else:
            st.error("Invalid username or password")


def show_dashboard():
    st.title("📊 Power BI Dashboard")
    st.markdown("Embedded dashboard below:")

    # Slider to adjust height
    iframe_height = st.slider(
        "Select iframe height (px):", min_value=400, max_value=1200, value=600, step=50
    )

    # Power BI embed (use Publish to Web link for local testing)
    power_bi_embed_code = f"""
    <iframe title="Power BI Dashboard"
        width="100%" height="{iframe_height}"
        src="https://app.powerbi.com/reportEmbed?reportId=6f8d9545-9ee6-4910-b7f5-ae4a906a11f9&autoAuth=true&ctid=4ce8fa72-23e2-4b0c-b5e0-847fff441edd"
        frameborder="0" allowFullScreen="true">
    </iframe>
    """
    components.html(power_bi_embed_code, height=iframe_height + 20)


def show_feedback():
    st.title("📝 Feedback")
    feedback = st.text_area("Write your feedback here:")
    if st.button("Submit Feedback"):
        if st.session_state.logged_in_user:
            st.session_state.users[st.session_state.logged_in_user][
                "feedback"
            ] = feedback
            st.success("Feedback submitted! Thank you.")
        else:
            st.error("You must be logged in to submit feedback.")


def show_profile():
    st.title("👤 Profile")
    if st.session_state.logged_in_user:
        username = st.session_state.logged_in_user
        st.write(f"**Username:** {username}")
        user_feedback = st.session_state.users[username]["feedback"]
        st.write(
            f"**Feedback:** {user_feedback if user_feedback else 'No feedback submitted yet.'}"
        )
    else:
        st.warning("Please log in to view your profile.")


# ---------------------------
# Sidebar Navigation
# ---------------------------
page = st.sidebar.selectbox(
    "Navigate", ["Home", "Sign Up", "Login", "Dashboard", "Feedback", "Profile"]
)

# ---------------------------
# Show page
# ---------------------------
if page == "Home":
    show_home()
elif page == "Sign Up":
    show_signup()
elif page == "Login":
    show_login()
elif page == "Dashboard":
    if st.session_state.logged_in_user:
        show_dashboard()
    else:
        st.warning("Please log in to access the dashboard.")
elif page == "Feedback":
    if st.session_state.logged_in_user:
        show_feedback()
    else:
        st.warning("Please log in to submit feedback.")
elif page == "Profile":
    show_profile()

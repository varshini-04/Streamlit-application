import streamlit as st
import streamlit.components.v1 as components
import json
import requests
from streamlit_lottie import st_lottie

# ---------------------------
# Simple in-memory user database (for demo)
# ---------------------------
if "users" not in st.session_state:
    st.session_state.users = {}  # {"username": {"password": ..., "feedback": ""}}

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None


# ---------------------------
# Load Lottie Animation (from URL)
# ---------------------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Load a simple globe animation for the homepage
lottie_globe = load_lottieurl(
    "https://assets9.lottiefiles.com/packages/lf20_gyn1w9v9.json"
)

# ---------------------------
# Page functions with improved aesthetics
# ---------------------------


def show_home():
    st.markdown(
        "<h1 style='text-align: center; color: #FF4B4B;'>🏠 Welcome!</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center;'>Your journey to data insights starts here. Use the sidebar to navigate.</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st_lottie(lottie_globe, height=200, key="globe_animation")


def show_signup():
    st.title("📝 Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Create Account"):
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
    st.markdown(
        "<h1 style='text-align: center;'>📊 Power BI Dashboard</h1>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown(
        """
        <style>
        .page-link {
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            background-color: #f0f2f6;
            color: #31333F;
            text-decoration: none;
            transition: background-color 0.3s, transform 0.3s;
        }
        .page-link:hover {
            background-color: #e0e0e4;
            transform: scale(1.05);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    dashboard_page = st.radio(
        "Select Dashboard View:",
        ["Global Holiday Data", "Economic Impact", "Destination Insights"],
        horizontal=True,
    )

    embed_codes = {
        "Global Holiday Data": "https://app.powerbi.com/reportEmbed?reportId=6f8d9545-9ee6-4910-b7f5-ae4a906a11f9&autoAuth=true&ctid=4ce8fa72-23e2-4b0c-b5e0-847fff441edd&pageName=ReportSection",
        "Economic Impact": "https://app.powerbi.com/reportEmbed?reportId=6f8d9545-9ee6-4910-b7f5-ae4a906a11f9&autoAuth=true&ctid=4ce8fa72-23e2-4b0c-b5e0-847fff441edd&pageName=ReportSection_b11d9426f04f26b52a82bec2b8377a7e",
        "Destination Insights": "https://app.powerbi.com/reportEmbed?reportId=6f8d9545-9ee6-4910-b7f5-ae4a906a11f9&autoAuth=true&ctid=4ce8fa72-23e2-4b0c-b5e0-847fff441edd&pageName=ReportSection_b11d9426f04f26b52a82bec2b8377a7e",
    }

    iframe_height = st.slider(
        "Select iframe height (px):", min_value=400, max_value=1200, value=750, step=50
    )

    components.html(
        f"""
        <iframe title="{dashboard_page}"
            width="100%" height="{iframe_height}"
            src="{embed_codes[dashboard_page]}"
            frameborder="0" allowFullScreen="true">
        </iframe>
        """,
        height=iframe_height + 20,
    )


def show_feedback():
    st.title("📝 Feedback")
    feedback = st.text_area("Share your feedback with us:", height=150)
    if st.button("Submit Feedback"):
        if st.session_state.logged_in_user:
            st.session_state.users[st.session_state.logged_in_user][
                "feedback"
            ] = feedback
            st.success("Feedback submitted! Thank you.")
        else:
            st.error("You must be logged in to submit feedback.")


def show_profile():
    st.title("👤 User Profile")
    if st.session_state.logged_in_user:
        username = st.session_state.logged_in_user
        st.info(f"Welcome, **{username}**!")

        with st.expander("My Submitted Feedback"):
            user_feedback = st.session_state.users[username]["feedback"]
            if user_feedback:
                st.write(user_feedback)
            else:
                st.write("No feedback submitted yet.")
    else:
        st.warning("Please log in to view your profile.")


def get_chatbot_response(prompt):
    prompt = prompt.lower()

    if "holiday" in prompt or "travel data" in prompt or "global data" in prompt:
        return "The **Global Holiday and Travel Data** dashboard provides insights on **domestic and international passengers**, flight years, best seasons for travel, and average flight rating."
    elif (
        "economic" in prompt
        or "gdp" in prompt
        or "expenditure" in prompt
        or "impact" in prompt
    ):
        return "The **Economic Impact** dashboard shows **Total GDP**, **Total Expenditures**, **Total Receipts**, and **tourism arrivals** by year. It gives a financial overview of the industry."
    elif (
        "destination" in prompt
        or "insights" in prompt
        or "type" in prompt
        or "cost" in prompt
    ):
        return "The **Destination Insights** dashboard focuses on traveler data, including **average daily cost**, **sum of average rating**, and a breakdown of destinations by **type** (e.g., Religious, Historical, Adventure)."
    elif "hello" in prompt or "hi" in prompt or "hey" in prompt:
        return "Hello! I am your dashboard assistant. What would you like to know about the dashboards?"
    elif "pages" in prompt or "dashboards" in prompt:
        return "The dashboards are: **Global Holiday Data**, **Economic Impact**, and **Destination Insights**. I can tell you about each one."
    else:
        return "I'm sorry, I can only answer questions about the content of the three dashboards. Please ask about the data on 'Global Holiday Data', 'Economic Impact', or 'Destination Insights'."


def show_chatbot():
    st.title("💬 Dashboard Chatbot")
    st.info(
        "I'm a simple assistant. Ask me questions about the dashboards! (e.g., 'What's on the economic dashboard?')"
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the dashboard..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_chatbot_response(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


def show_insights():
    st.title("💡 Key Insights")
    st.markdown("Here are some key takeaways from the Power BI dashboards.")
    st.markdown("---")

    st.subheader("🌍 Global Holiday and Travel Data")
    st.info(
        """
    - **Passenger Flow:** The dashboard highlights a significant number of domestic and international passengers, indicating a robust global travel market.
    - **Seasonal Trends:** Data on "Best Season" reveals clear seasonal patterns in travel, with certain times of the year being more popular for specific destinations.
    - **Rating & Popularity:** Insights into the average rating of destinations can help travelers and businesses understand popular trends and sentiment.
    """
    )
    st.markdown("---")

    st.subheader("💰 Economic Impact")
    st.info(
        """
    - **Tourism as a GDP Driver:** The data shows the substantial contribution of tourism to the Total GDP, with a clear breakdown of expenditures and receipts.
    - **Growth Trajectory:** The trends in "tourism arrivals by year" demonstrate the growth and stability of the global travel and tourism sector.
    - **Financial Health:** The visualizations on total expenditures and receipts offer a quick overview of the economic health and profitability of the industry.
    """
    )
    st.markdown("---")

    st.subheader("🗺️ Destination Insights")
    st.info(
        """
    - **Cost vs. Value:** The scatter plot comparing "Avg Cost" and "Sum of Avg Rating" provides a crucial insight into traveler perceived value for money across different destinations.
    - **Popularity by Type:** The pie chart on "Count of Destination Name by Type" reveals which types of travel are most popular, such as Adventure, Religious, or Historical.
    - **Visitor Behavior:** Analysis of annual visitors by country and expenditure helps to identify key source markets and their spending habits.
    """
    )


# ---------------------------
# NEW: Logout Page Function
# ---------------------------
def show_logout():
    st.title("🚪 Logout")
    st.session_state.logged_in_user = None
    st.success("You have been successfully logged out.")
    st.info("You can now navigate to the 'Login' page to log back in.")


# ---------------------------
# Sidebar Navigation with custom names
# ---------------------------
page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Sign Up",
        "Login",
        "Dashboard",
        "Feedback",
        "Profile",
        "Chatbot",
        "Insights",
        "Logout",
    ],
)

# ---------------------------
# Show page based on selection
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
elif page == "Chatbot":
    if st.session_state.logged_in_user:
        show_chatbot()
    else:
        st.warning("Please log in to use the chatbot.")
elif page == "Insights":
    if st.session_state.logged_in_user:
        show_insights()
    else:
        st.warning("Please log in to view the insights.")
elif page == "Logout":
    show_logout()

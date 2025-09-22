import streamlit as st
import streamlit.components.v1 as components

# Set page config
st.set_page_config(page_title="Power BI Dashboard Demo", layout="wide")

# Title & Description
st.title("📊 Power BI Dashboard")
st.markdown("This is a live Power BI dashboard embedded in a Streamlit web app.")

# Power BI Embed Code (make sure link is correct)
power_bi_embed_code = """
<iframe title="My Power BI Dashboard"
    width="1000" height="600"
    src="https://app.powerbi.com/reportEmbed?reportId=6f8d9545-9ee6-4910-b7f5-ae4a906a11f9&autoAuth=true&ctid=4ce8fa72-23e2-4b0c-b5e0-847fff441edd"
    frameborder="0" allowFullScreen="true">
</iframe>
"""

# Embed in Streamlit
components.html(power_bi_embed_code, height=620)

st.info("✅ Dashboard loaded successfully! You can interact with it directly above.")

import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ANTARCTIC AI",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# COMMAND CENTER THEME
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #050b14;
    color: #e8f1f8;
}

.block-container {
    padding-top: 1.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
}

.command-header {
    background: linear-gradient(90deg, #071321, #0b1c2d);
    border: 1px solid #1c354a;
    border-radius: 12px;
    padding: 18px 24px;
    margin-bottom: 18px;
}

.command-title {
    font-size: 30px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #eaf6ff;
    margin: 0;
}

.command-subtitle {
    font-size: 13px;
    color: #7fa6bf;
    letter-spacing: 1.5px;
    margin-top: 5px;
}

.status {
    color: #57d6a3;
    font-size: 13px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="command-header">

    <div class="command-title">
        ❄️ ANTARCTIC AI
    </div>

    <div class="command-subtitle">
        RESEARCH VESSEL COMMAND CENTER
    </div>

    <div class="status">
        ● SYSTEM ONLINE
    </div>

</div>
""", unsafe_allow_html=True)
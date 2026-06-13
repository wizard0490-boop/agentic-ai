import streamlit as st

st.set_page_config(
    page_title="Swastha AI – Indian Health Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #f0fdf4; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #16a34a;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        margin-bottom: 0.5rem;
    }
    .alert-red { border-left-color: #dc2626 !important; }
    .alert-yellow { border-left-color: #d97706 !important; }
    h1, h2, h3 { color: #14532d; }
    .stButton>button {
        background-color: #16a34a;
        color: white;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover { background-color: #15803d; }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/caduceus.png", width=60)
    st.title("Swastha AI")
    st.caption("आपका स्वास्थ्य सहायक")
    st.divider()
    page = st.radio(
        "Navigate",
        [" Dashboard", " Medication Tracker", " Fitness & Diet",
         "🤖 Health Chatbot", " Health Reports", "⚙️ My Profile"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("⚠️ For informational purposes only. Always consult a doctor.")

# Route pages
if page == " Dashboard":
    from pages import dashboard; dashboard.show()
elif page == " Medication Tracker":
    from pages import medication; medication.show()
elif page == " Fitness & Diet":
    from pages import fitness; fitness.show()
elif page == "🤖 Health Chatbot":
    from pages import chatbot; chatbot.show()
elif page == " Health Reports":
    from pages import reports; reports.show()
elif page == "⚙️ My Profile":
    from pages import profile; profile.show()


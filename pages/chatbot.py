import streamlit as st
import google.generativeai as genai

def show():
    st.title("🤖 Swastha AI Health Chatbot")

    api_key = st.secrets.get("GEMINI_API_KEY", "AQ.Ab8RN6JiEYj2bmxPMgvR57BB-UC5e8oajNUBzwZVmFNYk3Kc7Q")

    if not api_key:
        st.error("Gemini API key not configured.")
        return

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
    model = genai.GenerativeModel("gemini-2.5-flash")
    except:
    model = genai.GenerativeModel("gemini-2.0-flash")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask a health question...")

    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.write(prompt)

        try:
            response = model.generate_content(
                f"""
                You are Swastha AI, a healthcare assistant.
                Give educational health information.
                Do not diagnose diseases.
                Encourage users to consult healthcare professionals.

                User: {prompt}
                """
            )

            answer = response.text

        except Exception as e:
            answer = f"Error: {str(e)}"

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.write(answer)

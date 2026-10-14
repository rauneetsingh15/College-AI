
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="College AI Assistant",
    page_icon="🎓"
)

st.title("🎓 College AI Assistant")
st.caption("Your study and college companion")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Ask about studies, exams or college life..."
)

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=(
                        "You are a helpful College AI Assistant. "
                        "Explain topics in simple English. "
                        "Help with study plans, concepts and revision. "
                        "Do not invent official college information. "
                        "If college details are not provided, "
                        "tell the student to verify with their college. "
                        f"\nStudent question: {question}"
                    ),
                )

                answer = response.text or (
                    "Sorry, I could not generate an answer."
                )

            st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as error:
            st.error(
                "Something went wrong. Check your API key, "
                "internet connection and API usage limits."
            )
            st.caption(str(error))

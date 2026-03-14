import streamlit as st

import os
import sys

# Ensure project root (parent of this file's directory) is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    
from chatbot.rag_chain import ask_question


st.set_page_config(
    page_title="UHC Policy Chatbot",
    page_icon="💬",
)

st.title("UHC Insurance Policy Assistant")

st.write(
    "Ask questions about UnitedHealthcare (UHC) policy guidelines."
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask your question about UHC policies"):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Searching policies..."):

            answer = ask_question(prompt)

        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
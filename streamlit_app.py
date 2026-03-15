import streamlit as st
from chatbot.rag_chain import ask_question

st.set_page_config(
    page_title="UHC Insurance Policy Chatbot",
    page_icon="🏢",
    layout="centered"
)

st.title("🏢 UHC Insurance Policy Chatbot")
st.markdown("Ask questions about UnitedHealthcare policies. I'm here to help you understand your coverage and answer any questions you might have.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is the copay for a specialist visit?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Searching UHC policies..."):
            response = ask_question(prompt)
            st.markdown(response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Optional: Add a sidebar with example questions
with st.sidebar:
    st.header("💡 Example Questions")
    if st.button("What does my insurance cover?"):
        st.info("Type this question into the chat box below!")
    if st.button("How do I claim my insurance?"):
        st.info("Type this question into the chat box below!")
    if st.button("What is the copay for a specialist visit?"):
        st.info("Type this question into the chat box below!")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

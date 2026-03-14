import gradio as gr
from chatbot.rag_chain import ask_question

def chat(message, history):
    return ask_question(message)

demo = gr.ChatInterface(
    fn=chat,
    title="UHC Insurance Policy Chatbot",
    description="Ask questions about UnitedHealthcare policies"
)

demo.launch(server_name="0.0.0.0", server_port=7860)
import gradio as gr
import os
from chatbot.rag_chain import ask_question

def chat(message, history):
    return ask_question(message)

demo = gr.ChatInterface(
    fn=chat,
    title="UHC Insurance Policy Chatbot",
    description="Ask questions about UnitedHealthcare policies"
)
port = int(os.environ.get("PORT", 8862))
demo.launch(server_name="0.0.0.0", server_port=port)
import gradio as gr
from chatbot.rag_chain import ask_question

def chat(query):
    return ask_question(query)

demo = gr.Interface(
    fn=chat,
    inputs="text",
    outputs="text",
    title="UHC Insurance Policy Chatbot",
    description="Ask questions about UnitedHealthcare policies"
)

demo.launch()
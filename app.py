import gradio as gr
from chatbot.rag_chain import ask_question

def chat(message, history):
    """
    Chat function for the Gradio ChatInterface.
    message: The current user message.
    history: The conversation history (not used here, but available if ask_question supports it).
    """
    return ask_question(message)

demo = gr.ChatInterface(
    fn=chat,
    title="🏢 UHC Insurance Policy Chatbot",
    description="Ask questions about UnitedHealthcare policies. I'm here to help you understand your coverage and answer any questions you might have.",
    # theme=gr.themes.Soft(),
    examples=[
        "Amvuttra (vutrisiran) is medically necessary for the treatment of what?",
        "When is bariatric surgery required",
        "When did India win the World Cup?",
    ],
    # retry_btn="🔄 Retry",
    # undo_btn="↩️ Undo",
    # clear_btn="🗑️ Clear",
)

if __name__ == "__main__":
    demo.launch()

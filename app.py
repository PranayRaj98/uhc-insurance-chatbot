import gradio as gr
import os
from chatbot.rag_chain import ask_question

CSS = """
/* ── Global ── */
body, .gradio-container {
    background: #e8f1fb !important;
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}

/* ── Header ── */
.app-header {
    text-align: center;
    padding: 28px 20px 10px;
}
.app-header h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1a3a6b;
    margin-bottom: 6px;
}
.app-header p {
    color: #2563a8;
    font-size: 0.95rem;
    margin: 0;
}

/* ── Chat window ── */
#chatbox {
    background: #f0f7ff !important;
    border: 1px solid #b3cff5 !important;
    border-radius: 16px !important;
}

/* ── User & Bot bubbles — identical style ── */
.message.user,
.message.bot {
    background: #dbeafe !important;
    border: 1px solid #93c5fd !important;
    border-radius: 16px !important;
    color: #1a2f5e !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07) !important;
}

/* ── Input textbox ── */
#msg-box textarea {
    background: #fff !important;
    border: 1.5px solid #93c5fd !important;
    border-radius: 10px !important;
    color: #1a3a6b !important;
    font-size: 0.95rem !important;
}
#msg-box textarea::placeholder { color: #93c5fd !important; }

/* ── Send button ── */
#send-btn {
    background: #2563eb !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-weight: 600 !important;
    box-shadow: 0 3px 10px rgba(37,99,235,0.3) !important;
    transition: background 0.2s !important;
    min-width: 90px !important;
}
#send-btn:hover { background: #1d4ed8 !important; }

/* ── Examples ── */
.examples .example-btn {
    background: #dbeafe !important;
    border: 1px solid #93c5fd !important;
    color: #1a3a6b !important;
    border-radius: 10px !important;
}
.examples .example-btn:hover { background: #bfdbfe !important; }

/* ── Footer ── */
.status-bar {
    text-align: center;
    color: #3b82f6;
    font-size: 0.78rem;
    padding-top: 4px;
}
"""

EXAMPLES = [
    "Is Daxxify included in the coverage?",
    "When is bariatric surgery covered?",
    "What date did India win a world cup?",
    "What is cell free fetal DNA testing?",
    "What are the criteria when Evenity is proven for the treatment of osteoporosis in postmenopausal patients at high risk for fracture?",
]

def respond(message, chat_history):
    if not message.strip():
        return "", chat_history
    reply = ask_question(message)
    chat_history = chat_history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]
    return "", chat_history

def use_example(example, chat_history):
    reply = ask_question(example)
    chat_history.append((example, reply))
    return chat_history

with gr.Blocks(css=CSS, theme=gr.themes.Base(), title="UHC Insurance Policy Chatbot") as demo:

    # ── Header ──────────────────────────────────────────
    gr.HTML("""
    <div class="app-header">
        <h1>🏥 UHC Insurance Policy Chatbot</h1>
        <p>Powered by RAG · Ask any question about UnitedHealthcare policies</p>
    </div>
    """)

    # ── Chat window ─────────────────────────────────────
    chatbot = gr.Chatbot(
        elem_id="chatbox",
        height=440,
        show_label=False,
        avatar_images=(None, "https://img.icons8.com/fluency/48/bot.png"),
    )

    # ── Input row: textbox + button side by side ─────────
    with gr.Row(equal_height=True):
        msg = gr.Textbox(
            placeholder="Ask a question about UHC policies…",
            container=False,
            show_label=False,
            elem_id="msg-box",
            scale=9,
            lines=1,
            max_lines=4,
            autofocus=True,
        )
        send_btn = gr.Button("Send ➤", elem_id="send-btn", variant="primary", scale=1)

    # ── Example questions ────────────────────────────────
    gr.Examples(
        examples=[[e] for e in EXAMPLES],
        inputs=[msg],
        label="💡 Example questions",
        examples_per_page=5,
    )

    # ── Footer ───────────────────────────────────────────
    gr.HTML('<p class="status-bar">🔒 Answers are based solely on provided UHC policy documents.</p>')

    # ── Wire up events ───────────────────────────────────
    send_btn.click(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])
    msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])

port = int(os.environ.get("PORT", 8862))
demo.launch(server_name="0.0.0.0", server_port=port)
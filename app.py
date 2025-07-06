import gradio as gr
import google.generativeai as genai

# ✅ Gemini API Key
api_key = "AIzaSyDRAdhYBIijeYgQlFE11qmJTJtsnD6fP70"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Chat logic
def therapy_chat(user_input, history):
    history = history or []
    history.append(("user", user_input))

    prompt = """
You are MindBloom, an AI emotional support therapist.
1. Detect the user's emotional tone (e.g. anxiety, sadness, loneliness, etc.).
2. Respond using compassionate language (CBT/validation style).
3. End with exactly 4 wellness tips in bullet format.

Respond like this:

**Detected Emotion:** <emotion>

**🧠 THERAPEUTIC RESPONSE:**
<supportive response>

**💡 WELLNESS TIPS:**
• Tip 1  
• Tip 2  
• Tip 3  
• Tip 4
"""

    response = model.generate_content([prompt, user_input]).text
    history.append(("ai", response.replace("**", "")))
    return format_history(history), history

# ✅ Format chat history
def format_history(history):
    formatted = ""
    for sender, msg in history:
        if sender == "user":
            formatted += f"<div class='bubble user'><b>You:</b><br>{msg}</div>\n"
        else:
            if "WELLNESS TIPS:" in msg:
                parts = msg.split("WELLNESS TIPS:")
                therapy = parts[0]
                tips = "WELLNESS TIPS:" + parts[1]
                formatted += f"<div class='bubble ai'><b>MindBloom 🧠:</b><br>{therapy}</div>"
                formatted += f"<div class='tips-box'>{tips}</div>"
            else:
                formatted += f"<div class='bubble ai'><b>MindBloom 🧠:</b><br>{msg}</div>"
    return formatted

# ✅ Gradio App
with gr.Blocks(
    title="MindBloom: AI Therapist",
    css="""
/* ✅ Bubble Styles (rounded and multiline safe) */
.bubble {
    padding: 16px 22px;
    margin: 12px;
    border-radius: 30px;
    font-size: 1rem;
    max-width: 75%;
    font-family: 'Segoe UI', sans-serif;
    line-height: 1.6;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: pre-wrap;
    box-shadow: 0 6px 14px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.08);
}
.user {
    background-color: #22c55e33;
    color: #bbf7d0;
    margin-left: auto;
    text-align: right;
}
.ai {
    background-color: #3b82f633;
    color: #bfdbfe;
    margin-right: auto;
    text-align: left;
}

/* ✅ Tips Box */
.tips-box {
    background: linear-gradient(to right, #f9a8d4, #fef3c7);
    color: #1e293b;
    padding: 18px;
    margin: 10px;
    border-radius: 24px;
    font-size: 1rem;
    font-family: 'Segoe UI', sans-serif;
    max-width: 75%;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    margin-right: auto;
    white-space: pre-wrap;
}

/* ✅ Layout Styles */
body, .gradio-container {
    background: linear-gradient(to bottom right, #0f172a, #1e3a8a);
    font-family: 'Segoe UI', sans-serif;
    color: white;
}
#chatbox {
    max-height: 560px;
    overflow-y: auto;
    padding: 20px;
    background: #0f172a;
    border-radius: 16px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}
textarea {
    border-radius: 16px;
    padding: 14px;
    font-size: 1rem;
    background-color: #1e293b;
    color: white;
    border: none;
}
textarea::placeholder {
    color: #94a3b8;
    font-style: italic;
}
.gr-button {
    background: linear-gradient(to right, #34d399, #10b981);
    color: white;
    border-radius: 14px;
    font-size: 1rem;
    padding: 12px 24px;
    font-weight: bold;
}
.gr-button:hover {
    background: linear-gradient(to right, #059669, #047857);
}
"""
) as app:

    # ✅ Stylish White Glowing Heading
    gr.Markdown("""
<h1 style='
    color: white;
    font-size: 2.2rem;
    font-weight: 700;
    text-align: center;
    font-family: "Segoe UI", sans-serif;
    letter-spacing: 1px;
    text-shadow: 1px 1px 8px rgba(255, 255, 255, 0.3);'
>
🧠 MindBloom: Emotional AI Companion 🌙
</h1>
""")

    chat_output = gr.HTML(elem_id="chatbox", value="")
    chat_state = gr.State([])

    with gr.Row():
        user_input = gr.Textbox(placeholder="Type something on your mind...", label=None, lines=3)
        send_btn = gr.Button("Send 💬")

    send_btn.click(fn=therapy_chat, inputs=[user_input, chat_state], outputs=[chat_output, chat_state])

app.launch()

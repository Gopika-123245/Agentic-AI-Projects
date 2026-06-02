import os
import gradio as gr
from PyPDF2 import PdfReader
from groq import Groq

# — Set your Groq API key —
os.environ["GROQ_API_KEY"] = ""
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# — Load manual text —
def load_manual(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            ptext = page.extract_text() or ""
            text += ptext + "\n"
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    return text

manual_text = load_manual("/content/IISU_internship170925.pdf")  # <-- Replace with your manual path

# — Chat function using a Groq‑supported model —
def chat_with_manual(question):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # Supported Groq model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Answer based only on the given manual."},
                {"role": "user", "content": f"Manual:\n{manual_text}\n\nQuestion: {question}"}
            ],
            max_tokens=512
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# — Gradio UI —
iface = gr.Interface(
    fn=chat_with_manual,
    inputs=gr.Textbox(lines=2, placeholder="Ask something about the manual..."),
    outputs="text",
    title="Manual‑Based Groq Chatbot",
    description="Ask questions from your manuawl using Groq API."
)

iface.launch()

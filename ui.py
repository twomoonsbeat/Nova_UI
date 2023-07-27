from test import *
import gradio as gr
from test import *
import pyttsx3

 
def respond(message, history):
    if message:
        response = ask_ai(message).response
        return response

gr.ChatInterface(
    respond,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Ask me a question", container=False, scale=10),
    title="Nova",
    description="I am Nova your personal Assistant",
    theme="soft",
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
).launch()
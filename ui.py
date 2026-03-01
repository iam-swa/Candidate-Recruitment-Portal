"""
Beautiful Gradio web interface for the Candidate Recruitment Portal.
"""

import os
import gradio as gr
from dotenv import load_dotenv
import speech_recognition as sr

load_dotenv()

from main import create_app
from app.utils.tts import speak
from app.utils.db import init_db, create_or_update_user, save_application, get_application_status, get_user

init_db()

def transcribe_audio(audio_path):
    """Convert audio file to text"""
    if not audio_path:
        return ""
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            return ""

def chat(audio_path, text_input, history, workflow):
    """Process voice or text input and return response"""
    if not audio_path and not text_input:
        return history, None, None, "", workflow
    
    user_text = ""
    if audio_path:
        user_text = transcribe_audio(audio_path)
    elif text_input:
        user_text = text_input

    if not user_text:
        return history, None, None, "", workflow
    
    response = workflow.chat(user_text)
    
    audio_file = speak(response, play=False)
    
    history = history + [
        {"role": "user", "content": user_text},
        {"role": "assistant", "content": response}
    ]
    
    return history, audio_file, None, "", workflow

def init_session():
    """Initialize new session with greeting"""
    workflow = create_app()
    greeting = workflow.get_greeting()
    if not greeting:
        greeting = "Welcome to the Candidate Recruitment Portal! How can I help you today?"
        
    greeting_audio = speak(greeting, play=False)
    initial_history = [{"role": "assistant", "content": greeting}]
    return initial_history, greeting_audio, workflow

# Custom CSS for modern interface
custom_css = """
body {
    background-color: #0f172a !important;
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    color: #f1f5f9;
}
.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
}
h1 {
    text-align: center;
    font-weight: 800;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}
.chatbot {
    border-radius: 1rem !important;
    border: 1px solid #1e293b !important;
    background-color: #1e293b !important;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5) !important;
    padding: 1rem !important;
}
.login-nav-btn {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    border: none !important;
    color: white !important;
    padding: 0.5rem 1rem !important;
    border-radius: 0.5rem !important;
    font-weight: 600 !important;
}
.user-row .message-wrap {
    background-color: #3b82f6 !important;
    color: white !important;
    border-radius: 1rem 1rem 0 1rem !important;
}
.bot-row .message-wrap {
    background-color: #334155 !important;
    color: #f8fafc !important;
    border-radius: 1rem 1rem 1rem 0 !important;
}
"""

def process_login(email, fname, lname):
    if not email or not fname or not lname:
        return (
            gr.update(visible=True), 
            gr.update(visible=False), 
            "Please enter email, first name, and last name.", 
            email,
            gr.update(value=""),
            gr.update(visible=True),
            gr.update(visible=False),
            get_tracker_html(applied=False), 
            None
        )
        
    create_or_update_user(email, fname, lname)
    status = get_application_status(email)
    applied = (status == "Applied")
        
    full_name = f"{fname.capitalize()} {lname.capitalize()}"
    initial = fname[0].upper() if fname else "U"

    user_html = f"""
        <div class="user-account">
            <span>{full_name}</span>
            <div class="avatar-circle">{initial}</div>
        </div>
    """
    
    return (
        gr.update(visible=False),
        gr.update(visible=True),
        "",
        email,
        gr.update(value=full_name),
        gr.update(visible=False),
        gr.update(value=user_html, visible=True),
        get_tracker_html(applied=applied),
        email
    )

def get_tracker_html(applied=False):
    applied_class = "completed" if applied else ""
    return f"""
        <div class="tracker-container">
            <h3>Your Application Progress</h3>
            <div class="tracker-steps">
                <div class="step {applied_class}">
                    <div class="step-circle"></div>
                    <div class="step-label">Applied</div>
                </div>
                <div class="step">
                    <div class="step-circle"></div>
                    <div class="step-label">Tech Interview</div>
                </div>
                <div class="step">
                    <div class="step-circle"></div>
                    <div class="step-label">HR Round</div>
                </div>
                <div class="step">
                    <div class="step-circle"></div>
                    <div class="step-label">Offer</div>
                </div>
            </div>
        </div>
    """

def handle_submit(email, cover_letter, resume_path):
    if not email:
        return gr.update(visible=True), gr.update(visible=False), get_tracker_html(False), gr.update(value="<div style='color:red'>Please login first.</div>", visible=True)
    
    save_application(email, resume_path, cover_letter)
    return gr.update(visible=False), gr.update(visible=True), get_tracker_html(True), gr.update(visible=False)

def show_login_page():
    return gr.update(visible=True), gr.update(visible=False)

with gr.Blocks(
    css=custom_css,
    theme=gr.themes.Default(primary_hue="blue", secondary_hue="indigo")
) as demo:

    user_state = gr.State(None)

    # LOGIN PAGE
    with gr.Column(visible=False) as login_page:
        gr.Markdown("<h2>Login to Candidate Portal</h2>")
        login_error = gr.Markdown("", visible=False)
        login_email = gr.Textbox(label="Email")
        login_fname = gr.Textbox(label="First Name")
        login_lname = gr.Textbox(label="Last Name")
        with gr.Row():
            login_submit_btn = gr.Button("Login")
            login_cancel_btn = gr.Button("Cancel")

    # MAIN APP
    with gr.Column(visible=True) as main_app:
        with gr.Row():
            gr.HTML("<h2 class='brand-name'>Xobin</h2>")
            nav_login_btn = gr.Button("Login", elem_classes=["login-nav-btn"])
            nav_user_info = gr.HTML("", visible=False)

        gr.Markdown("# Candidate Recruitment Portal")
        tracker = gr.HTML(get_tracker_html(applied=False))

        workflow = gr.State()

        with gr.Tabs():
            with gr.TabItem("AI Assistant"):
                chatbot = gr.Chatbot(height=500, elem_classes=["chatbot"])
                audio_output = gr.Audio(autoplay=True)
                audio_input = gr.Audio(sources=["microphone"], type="filepath")
                text_input = gr.Textbox()
                send_btn = gr.Button("Send")

                demo.load(fn=init_session, outputs=[chatbot, audio_output, workflow])

                audio_input.stop_recording(fn=chat, inputs=[audio_input, text_input, chatbot, workflow],
                                           outputs=[chatbot, audio_output, audio_input, text_input, workflow])

                text_input.submit(fn=chat, inputs=[audio_input, text_input, chatbot, workflow],
                                  outputs=[chatbot, audio_output, audio_input, text_input, workflow])

                send_btn.click(fn=chat, inputs=[audio_input, text_input, chatbot, workflow],
                               outputs=[chatbot, audio_output, audio_input, text_input, workflow])

            with gr.TabItem("Apply Now"):
                app_error = gr.HTML("", visible=False)
                with gr.Column(visible=True) as application_view:
                    app_name = gr.Textbox(label="Full Name")
                    app_email = gr.Textbox(label="Email", interactive=False)
                    app_resume = gr.File(label="Resume")
                    app_cover_letter = gr.Textbox(label="Cover Letter")
                    submit_btn = gr.Button("Submit")

                with gr.Column(visible=False) as success_view:
                    gr.Markdown("Application received!")

    nav_login_btn.click(fn=show_login_page, outputs=[login_page, main_app])

    login_cancel_btn.click(fn=lambda: (gr.update(visible=False), gr.update(visible=True)),
                           outputs=[login_page, main_app])

    login_submit_btn.click(
        fn=process_login,
        inputs=[login_email, login_fname, login_lname],
        outputs=[login_page, main_app, login_error, app_email, app_name, nav_login_btn, nav_user_info, tracker, user_state]
    )

    submit_btn.click(
        fn=handle_submit,
        inputs=[user_state, app_cover_letter, app_resume],
        outputs=[application_view, success_view, tracker, app_error]
    )

if __name__ == "__main__":
    demo.launch(share=True)
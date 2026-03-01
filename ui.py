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
    # Ensure there's a default generic greeting if not generated
    if not greeting:
        greeting = "Welcome to the Candidate Recruitment Portal! How can I help you today?"
        
    greeting_audio = speak(greeting, play=False)
    initial_history = [{"role": "assistant", "content": greeting}]
    return initial_history, greeting_audio, workflow

# Custom CSS for a modern, sleek interface
custom_css = """
/* Body and Overall Container styling */
body {
    background-color: #0f172a !important; /* Tailwind slate-900 */
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    color: #f1f5f9; /* Tailwind slate-100 */
}
.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* Header styling */
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
    color: #94a3b8; /* Tailwind slate-400 */
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

/* Chatbot Area */
.chatbot {
    border-radius: 1rem !important;
    border: 1px solid #1e293b !important;
    background-color: #1e293b !important;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5) !important;
    padding: 1rem !important;
}

/* Login Button */
.login-nav-btn {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    border: none !important;
    color: white !important;
    padding: 0.5rem 1rem !important;
    border-radius: 0.5rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
.login-nav-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2) !important;
}

/* User Message Bubble */
.user-row .message-wrap {
    background-color: #3b82f6 !important;
    color: white !important;
    border-radius: 1rem 1rem 0 1rem !important;
    border: none !important;
    padding: 1rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2) !important;
}

/* Assistant Message Bubble */
.bot-row .message-wrap {
    background-color: #334155 !important;
    color: #f8fafc !important;
    border-radius: 1rem 1rem 1rem 0 !important;
    border: 1px solid #475569 !important;
    padding: 1rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

/* Audio Player */
audio {
    border-radius: 2rem !important;
    background-color: #1e293b !important;
    border: 1px solid #3b82f6 !important;
}

/* Text Input & Buttons */
.textbox textarea {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #475569 !important;
    border-radius: 0.75rem !important;
}
.textbox textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
}
.primary-button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 0.75rem !important;
    transition: all 0.2s ease !important;
}
.primary-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3) !important;
}

/* General cleanups */
.border-none { border: none !important; }

/* Top Navbar */
.top-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #1e293b;
    padding: 1rem 2rem;
    border-radius: 0.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.brand-name {
    font-size: 1.5rem;
    font-weight: 800;
    color: #3b82f6;
    margin: 0;
}
.user-account {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #cbd5e1;
    font-weight: 500;
}
.avatar-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: #3b82f6;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.2s ease;
}
.avatar-circle:hover {
    transform: scale(1.1);
}

/* Modal styling for basic profile */
.profile-modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #1e293b;
    padding: 2rem;
    border-radius: 1rem;
    border: 1px solid #475569;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    z-index: 1000;
    width: 300px;
    display: none;
}
.profile-modal.show {
    display: block;
}
.overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
    display: none;
}
.overlay.show {
    display: block;
}

/* Tracker styling */
.tracker-container {
    background-color: #1e293b;
    padding: 1.5rem;
    border-radius: 1rem;
    margin-bottom: 2rem;
    border: 1px solid #334155;
}
.tracker-steps {
    display: flex;
    justify-content: space-between;
    margin-top: 1rem;
    position: relative;
}
.tracker-steps::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 2px;
    background-color: #334155;
    z-index: 1;
}
.step {
    position: relative;
    z-index: 2;
    background-color: #1e293b;
    padding: 0 10px;
    text-align: center;
}
.step-circle {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background-color: #334155;
    margin: 0 auto 0.5rem;
    border: 2px solid #1e293b;
}
.step.active .step-circle {
    background-color: #3b82f6;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}
.step.completed .step-circle {
    background-color: #10b981;
}
.step-label {
    font-size: 0.8rem;
    color: #94a3b8;
}
.step.active .step-label {
    color: #f1f5f9;
    font-weight: 600;
}

/* Fix chat overlaps */
.message {
    padding-left: 0 !important;
}
.message-wrap {
    overflow-wrap: break-word !important;
    word-break: break-word !important;
}
"""

def process_login(email, fname, lname):
    """Save user login to DB and switch to main app"""
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
        <div class="user-account" onclick="document.getElementById('profile-overlay').classList.toggle('show'); document.getElementById('profile-modal').classList.toggle('show');">
            <span>{full_name}</span>
            <div class="avatar-circle">{initial}</div>
        </div>
        
        <div id="profile-overlay" class="overlay" onclick="document.getElementById('profile-overlay').classList.remove('show'); document.getElementById('profile-modal').classList.remove('show');"></div>
        <div id="profile-modal" class="profile-modal">
            <h3 style="margin-top:0; color: #f8fafc">Profile Details</h3>
            <p><strong>Name:</strong> {full_name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Status:</strong> {status}</p>
            <button class="primary-button" style="width: 100%; margin-top: 1rem; padding: 0.5rem;" onclick="document.getElementById('profile-overlay').classList.remove('show'); document.getElementById('profile-modal').classList.remove('show');">Close</button>
        </div>
    """
    
    return gr.update(visible=False), gr.update(visible=True), "", email, gr.update(value=full_name), gr.update(visible=False), gr.update(value=user_html, visible=True), get_tracker_html(applied=applied), email

def get_tracker_html(applied=False):
    applied_class = "completed" if applied else ""
    return f"""
        <div class="tracker-container">
            <h3 style="margin-top: 0; color: #f1f5f9;">Your Application Progress</h3>
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
        return gr.update(visible=True), gr.update(visible=False), get_tracker_html(False), gr.update(value="<div style='color:red'>Please login via the top right corner first.</div>", visible=True)
    
    save_application(email, resume_path, cover_letter)
    return gr.update(visible=False), gr.update(visible=True), get_tracker_html(True), gr.update(visible=False)

def show_login_page():
    return gr.update(visible=True), gr.update(visible=False)

with gr.Blocks() as demo:
    user_state = gr.State(None)
    
    # LOGIN PAGE
    with gr.Column(visible=False) as login_page:
        gr.Markdown("<br><br>")
        with gr.Row():
            gr.Column(scale=1)
            with gr.Column(scale=2, elem_classes=["modal-centered"]):
                gr.Markdown("<h2 style='text-align: center;'>Login to Candidate Portal</h2>")
                login_error = gr.Markdown("", visible=False)
                login_email = gr.Textbox(label="Email Address", placeholder="user@example.com")
                login_fname = gr.Textbox(label="First Name", placeholder="e.g. John")
                login_lname = gr.Textbox(label="Last Name", placeholder="e.g. Doe")
                with gr.Row():
                    login_submit_btn = gr.Button("Login", elem_classes=["primary-button"])
                    login_cancel_btn = gr.Button("Cancel")
            gr.Column(scale=1)

    # MAIN APP
    with gr.Column(visible=True) as main_app:
        # Top Navbar (Dynamic, Native Gradio to avoid HTML injection stripping)
        with gr.Row(elem_classes=["top-navbar"]):
            gr.HTML("<h2 class='brand-name'>Xobin</h2>")
            nav_login_btn = gr.Button("Login", elem_classes=["login-nav-btn"])
            nav_user_info = gr.HTML("", visible=False)
        
        with gr.Column():
            gr.Markdown("# 🚀 Candidate Recruitment Portal")
            gr.Markdown("<div class='subtitle'>AI-driven interview prep, resume analysis, and career guidance.</div>")
            
        # Application Tracker
        tracker = gr.HTML(get_tracker_html(applied=False))

        workflow = gr.State()
        
        with gr.Tabs():
            with gr.TabItem("💬 AI Assistant"):
                with gr.Row():
                    with gr.Column(scale=3):
                        chatbot = gr.Chatbot(
                            height=500,
                            elem_classes=["chatbot"],
                            avatar_images=(None, "https://cdn-icons-png.flaticon.com/512/4712/4712038.png"),
                            show_label=False # Removes the overlapping 'Chatbot' label symbol on some Gradio versions
                        )
                        
                    with gr.Column(scale=1):
                        gr.Markdown("### 🎛️ Controls")
                        
                        audio_output = gr.Audio(
                            autoplay=True,
                            label="🔊 Assistant Voice",
                            container=True
                        )
                        
                        gr.Markdown("---")
                        gr.Markdown("#### Use Microphone:")
                        audio_input = gr.Audio(
                            sources=["microphone"], 
                            type="filepath",
                            label="🎤 Speak your message",
                            container=True,
                            waveform_options={"waveform_color": "#3b82f6"}
                        )
                        
                        text_input = gr.Textbox(
                            placeholder="Or type your message here and hit Enter...",
                            label="",
                            container=False,
                            elem_classes=["textbox"]
                        )
                        send_btn = gr.Button("Send Message", elem_classes=["primary-button"])

                # Setup initial app state load
                demo.load(
                    fn=init_session,
                    outputs=[chatbot, audio_output, workflow]
                )
                
                # Handle voice recordings stopping
                audio_input.stop_recording(
                    fn=chat,
                    inputs=[audio_input, text_input, chatbot, workflow],
                    outputs=[chatbot, audio_output, audio_input, text_input, workflow],
                )
                
                # Handle Text input submitting
                text_input.submit(
                    fn=chat,
                    inputs=[audio_input, text_input, chatbot, workflow],
                    outputs=[chatbot, audio_output, audio_input, text_input, workflow],
                )
                send_btn.click(
                    fn=chat,
                    inputs=[audio_input, text_input, chatbot, workflow],
                    outputs=[chatbot, audio_output, audio_input, text_input, workflow],
                )

            with gr.TabItem("📋 Apply Now"):
                app_error = gr.HTML("", visible=False)
                with gr.Column(visible=True) as application_view:
                    gr.Markdown("### Application Form")
                    gr.Markdown("Please verify your details below:")
                    app_name = gr.Textbox(label="Full Name", interactive=True)
                    app_email = gr.Textbox(label="Email Address", interactive=False)
                    app_resume = gr.File(label="Upload Resume (PDF/DOCX)", type="filepath")
                    app_cover_letter = gr.Textbox(label="Cover Letter", lines=4)
                    submit_btn = gr.Button("Submit Application", elem_classes=["primary-button"], variant="primary")
                
                with gr.Column(visible=False) as success_view:
                    gr.Markdown("### 🎉 Success!")
                    gr.Markdown("We have received your application and we will let you know the details by further intimations.")
                    gr.Markdown("You can go back to the AI Assistant tab to continue practicing your interview skills.")

    nav_login_btn.click(
        fn=show_login_page,
        inputs=[],
        outputs=[login_page, main_app]
    )

    login_cancel_btn.click(
        fn=lambda: (gr.update(visible=False), gr.update(visible=True)),
        inputs=[],
        outputs=[login_page, main_app]
    )

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
    demo.launch(css=custom_css, theme=gr.themes.Default(primary_hue="blue", secondary_hue="indigo"))

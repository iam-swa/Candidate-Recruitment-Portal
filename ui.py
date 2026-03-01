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

/* User Message Bubble */
.user-row .message-wrap {
    background: linear-gradient(135deg, #2563eb, #4f46e5) !important;
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

def mock_login(email, fname, lname):
    """Simulate a login and switch to application tab"""
    if not email or not fname or not lname:
        return (
            gr.update(visible=True), 
            gr.update(visible=False), 
            "Please enter email, first name, and last name.", 
            gr.update(value=""),
            # Top navbar fallback
            """
            <div class="top-navbar">
                <h2 class="brand-name">Xobin</h2>
                <div class="user-account">
                    <span>Login to Apply</span>
                    <div class="avatar-circle">?</div>
                </div>
            </div>
            """
        )
        
    full_name = f"{fname.capitalize()} {lname.capitalize()}"
    initial = fname[0].upper() if fname else "U"
    
    new_navbar = f"""
        <div class="top-navbar">
            <h2 class="brand-name">Xobin</h2>
            <div class="user-account">
                <span>{full_name}</span>
                <div class="avatar-circle">{initial}</div>
            </div>
        </div>
    """
    
    return gr.update(visible=False), gr.update(visible=True), "", gr.update(value=full_name), new_navbar

def mock_submit():
    """Simulate form submission"""
    return gr.update(visible=False), gr.update(visible=True)

with gr.Blocks() as demo:
    # Top Navbar (Dynamic)
    top_nav = gr.HTML("""
        <div class="top-navbar">
            <h2 class="brand-name">Xobin</h2>
            <div class="user-account">
                <span>Login to Apply</span>
                <div class="avatar-circle">?</div>
            </div>
        </div>
    """)
    
    with gr.Column():
        gr.Markdown("# 🚀 Candidate Recruitment Portal")
        gr.Markdown("<div class='subtitle'>AI-driven interview prep, resume analysis, and career guidance.</div>")
        
    # Application Tracker
    gr.HTML("""
        <div class="tracker-container">
            <h3 style="margin-top: 0; color: #f1f5f9;">Your Application Progress</h3>
            <div class="tracker-steps">
                <div class="step completed">
                    <div class="step-circle"></div>
                    <div class="step-label">Applied</div>
                </div>
                <div class="step active">
                    <div class="step-circle"></div>
                    <div class="step-label">AI Screening</div>
                </div>
                <div class="step">
                    <div class="step-circle"></div>
                    <div class="step-label">Tech Inteview</div>
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
    """)

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
            with gr.Column() as login_view:
                gr.Markdown("### Login to Apply")
                login_error = gr.Markdown("", visible=False)
                login_email = gr.Textbox(label="Email Address", placeholder="user@example.com")
                login_fname = gr.Textbox(label="First Name", placeholder="e.g. John")
                login_lname = gr.Textbox(label="Last Name", placeholder="e.g. Doe")
                login_btn = gr.Button("Login to Continue", elem_classes=["primary-button"])
                
            with gr.Column(visible=False) as application_view:
                gr.Markdown("### Application Form")
                gr.Markdown("Please verify your details below:")
                app_name = gr.Textbox(label="Full Name", interactive=True)
                app_email = gr.Textbox(label="Email Address", interactive=False)
                app_resume = gr.File(label="Upload Resume (PDF/DOCX)")
                app_cover_letter = gr.Textbox(label="Cover Letter", lines=4)
                submit_btn = gr.Button("Submit Application", elem_classes=["primary-button"], variant="primary")
            
            with gr.Column(visible=False) as success_view:
                gr.Markdown("### 🎉 Success!")
                gr.Markdown("We have received your application and we will let you know the details by further intimations.")
                gr.Markdown("You can go back to the AI Assistant tab to continue practicing your interview skills.")

            login_btn.click(
                fn=mock_login,
                inputs=[login_email, login_fname, login_lname],
                outputs=[login_view, application_view, login_error, app_name, top_nav]
            ).then(
                fn=lambda email: email,
                inputs=[login_email],
                outputs=[app_email]
            )
            
            submit_btn.click(
                fn=mock_submit,
                inputs=[],
                outputs=[application_view, success_view]
            )

if __name__ == "__main__":
    demo.launch(server_port=7870, css=custom_css, theme=gr.themes.Default(primary_hue="blue", secondary_hue="indigo"))

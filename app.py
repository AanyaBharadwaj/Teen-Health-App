"""
TeenMind Companion - Phase 2: Text + Voice Chat
An empathetic AI peer support companion for teens (13-19).
"""

import streamlit as st
import google.generativeai as genai
from datetime import datetime
from config import (
    GEMINI_API_KEY, TEXT_MODEL, GENERATION_CONFIG,
    SAFETY_SETTINGS, MAX_SESSION_TIME, THEME, RESOURCES
)
from safety import (
    SafetyMonitor, validate_age, get_parental_consent_text,
    get_app_disclaimer
)
from prompts import SYSTEM_INSTRUCTION
from voice import (
    VoiceProcessor, render_voice_mode, process_voice_input,
    play_voice_response, get_audio_waveform_viz
)
from realtime_voice import render_realtime_voice_ui, stop_realtime_session

# Page Configuration
st.set_page_config(
    page_title="TeenMind Companion 🧠✨",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Enhanced Neon Dark Theme
st.markdown(f"""
<style>
    /* Main background gradient */
    .stApp {{
        background: {THEME['background_gradient']};
        color: {THEME['text_color']};
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}

    /* Headers with glow effect */
    h1 {{
        color: {THEME['primary_color']};
        text-shadow: 0 0 20px {THEME['primary_color']}, 0 0 40px {THEME['primary_color']}40;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }}

    h2, h3 {{
        color: {THEME['primary_color']};
        text-shadow: 0 0 10px {THEME['primary_color']}80;
        font-weight: 600;
    }}

    /* Enhanced chat messages with smooth animations */
    .stChatMessage {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.08));
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(0, 255, 136, 0.15);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 0.4s ease-out;
        transition: all 0.3s ease;
    }}

    .stChatMessage:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 255, 136, 0.2);
        border-color: rgba(0, 255, 136, 0.3);
    }}

    /* User message - Cyan theme */
    .stChatMessage[data-testid="user-message"] {{
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.08), rgba(0, 212, 255, 0.15));
        border-left: 4px solid {THEME['accent_color']};
        margin-left: 10%;
    }}

    /* Assistant message - Green theme */
    .stChatMessage[data-testid="assistant-message"] {{
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.08), rgba(0, 255, 136, 0.15));
        border-left: 4px solid {THEME['primary_color']};
        margin-right: 10%;
    }}

    /* Message avatars with glow */
    .stChatMessage img {{
        border-radius: 50%;
        box-shadow: 0 0 15px {THEME['primary_color']}60;
    }}

    /* Enhanced input box */
    .stChatInputContainer {{
        border-top: 2px solid {THEME['primary_color']};
        padding-top: 15px;
        background: rgba(15, 15, 35, 0.5);
        backdrop-filter: blur(10px);
    }}

    .stChatInput > div {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 25px;
        transition: all 0.3s;
    }}

    .stChatInput > div:focus-within {{
        border-color: {THEME['primary_color']};
        box-shadow: 0 0 20px {THEME['primary_color']}40;
    }}

    /* Buttons with gradient and glow */
    .stButton > button {{
        background: linear-gradient(90deg, {THEME['primary_color']}, {THEME['accent_color']});
        color: #0f0f23;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 700;
        font-size: 15px;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
    }}

    .stButton > button:hover {{
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 25px {THEME['primary_color']}60, 0 0 30px {THEME['primary_color']}40;
    }}

    .stButton > button:active {{
        transform: translateY(0) scale(0.98);
    }}

    /* Primary button variant */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(90deg, {THEME['primary_color']}, #00cc70);
        box-shadow: 0 4px 20px {THEME['primary_color']}50;
    }}

    /* Sidebar with enhanced styling */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(15, 15, 35, 0.95), rgba(26, 0, 51, 0.95));
        border-right: 1px solid rgba(0, 255, 136, 0.2);
        backdrop-filter: blur(10px);
    }}

    /* Metrics cards with animation */
    .metric-card {{
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.08), rgba(0, 255, 136, 0.15));
        border: 1px solid {THEME['primary_color']}60;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s;
    }}

    .metric-card:hover {{
        transform: translateY(-3px);
        border-color: {THEME['primary_color']};
        box-shadow: 0 6px 20px {THEME['primary_color']}30;
    }}

    /* Crisis box with pulsing animation */
    .crisis-box {{
        background: linear-gradient(135deg, rgba(255, 0, 100, 0.15), rgba(255, 0, 100, 0.25));
        border: 2px solid #ff0066;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(255, 0, 100, 0.3);
        animation: pulse 2s ease-in-out infinite;
    }}

    /* Success/Info boxes */
    .success-box {{
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(0, 255, 136, 0.25));
        border: 2px solid {THEME['primary_color']};
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 20px {THEME['primary_color']}30;
    }}

    /* Voice mode indicator */
    .voice-active {{
        background: linear-gradient(90deg, {THEME['primary_color']}40, {THEME['accent_color']}40);
        border: 2px dashed {THEME['primary_color']};
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        animation: borderPulse 2s ease-in-out infinite;
    }}

    /* Scrollbar styling */
    ::-webkit-scrollbar {{
        width: 10px;
    }}

    ::-webkit-scrollbar-track {{
        background: rgba(15, 15, 35, 0.5);
    }}

    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, {THEME['primary_color']}, {THEME['accent_color']});
        border-radius: 5px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {THEME['primary_color']};
    }}

    /* Animations */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    @keyframes pulse {{
        0%, 100% {{
            box-shadow: 0 0 20px rgba(255, 0, 100, 0.3);
        }}
        50% {{
            box-shadow: 0 0 40px rgba(255, 0, 100, 0.6);
        }}
    }}

    @keyframes borderPulse {{
        0%, 100% {{
            border-color: {THEME['primary_color']}80;
        }}
        50% {{
            border-color: {THEME['primary_color']};
        }}
    }}

    /* Loading spinner */
    .stSpinner > div {{
        border-color: {THEME['primary_color']} transparent transparent transparent !important;
    }}

    /* Success/Error/Warning/Info messages */
    .stSuccess, .stError, .stWarning, .stInfo {{
        border-radius: 12px;
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.3s ease-out;
    }}

    /* Divider */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {THEME['primary_color']}40, transparent);
        margin: 30px 0;
    }}

    /* Select boxes and inputs */
    .stSelectbox > div > div, .stTextInput > div > div {{
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(0, 255, 136, 0.3);
        border-radius: 12px;
    }}

    /* Audio player */
    audio {{
        filter: hue-rotate(90deg) saturate(1.5);
    }}
</style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize all session state variables."""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.age_verified = False
        st.session_state.consent_given = False
        st.session_state.user_age = None
        st.session_state.user_name = "Friend"
        st.session_state.messages = []
        st.session_state.session_start = None
        st.session_state.safety_monitor = SafetyMonitor()
        st.session_state.voice_processor = VoiceProcessor()
        st.session_state.crisis_count = 0
        st.session_state.message_count = 0
        st.session_state.voice_mode_enabled = False
        st.session_state.voice_mode_type = "text"  # "text", "turn-based", "realtime"


def initialize_gemini():
    """Initialize Gemini API."""
    if not GEMINI_API_KEY:
        st.error("❌ Gemini API key not found. Please add GEMINI_API_KEY to your .env file.")
        st.stop()

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return genai.GenerativeModel(
            model_name=TEXT_MODEL,
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS,
            system_instruction=SYSTEM_INSTRUCTION
        )
    except Exception as e:
        st.error(f"❌ Failed to initialize Gemini: {str(e)}")
        st.stop()


def show_age_gate():
    """Display age verification screen."""
    st.title("🧠✨ TeenMind Companion")

    st.markdown("""
    <div class="success-box">
    <h3>Welcome! Before we start...</h3>
    <p>This AI companion is designed for teenagers (ages 13-19) to practice coping skills and receive empathetic support.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("age_verification"):
        st.subheader("Age Verification")
        age = st.number_input("How old are you?", min_value=1, max_value=100, value=15)
        name = st.text_input("What should I call you? (Optional)", value="Friend")

        submitted = st.form_submit_button("Continue")

        if submitted:
            is_valid, error_msg = validate_age(age)
            if not is_valid:
                st.error(error_msg)
            else:
                st.session_state.user_age = age
                st.session_state.user_name = name if name else "Friend"
                st.session_state.age_verified = True
                st.rerun()


def show_consent_screen():
    """Display parental consent and disclaimer."""
    st.title("🧠✨ TeenMind Companion")

    st.markdown(get_parental_consent_text())

    st.markdown(get_app_disclaimer())

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ I Understand & Agree", use_container_width=True):
            st.session_state.consent_given = True
            st.session_state.session_start = datetime.now()
            st.rerun()

    with col2:
        if st.button("❌ Exit", use_container_width=True):
            st.session_state.age_verified = False
            st.rerun()


def show_sidebar():
    """Display sidebar with resources and session info."""
    with st.sidebar:
        st.title("🆘 Quick Help")

        # Session metrics
        if st.session_state.session_start:
            elapsed = (datetime.now() - st.session_state.session_start).seconds
            remaining = MAX_SESSION_TIME - elapsed

            st.markdown(f"""
            <div class="metric-card">
                <h4>Session Time</h4>
                <p style="font-size: 24px; color: {THEME['primary_color']};">
                    {remaining // 60}:{remaining % 60:02d}
                </p>
            </div>
            """, unsafe_allow_html=True)

            if remaining <= 0:
                st.warning("⏰ Session time limit reached. Please take a break!")

        st.markdown(f"""
        <div class="metric-card">
            <h4>Messages</h4>
            <p style="font-size: 24px; color: {THEME['accent_color']};">
                {st.session_state.message_count}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Crisis Resources
        st.markdown("---")
        st.subheader("🆘 Crisis Resources")

        for hotline in RESOURCES["crisis_hotlines"]:
            st.markdown(f"""
            **{hotline['name']}**
            📞 {hotline['number']}
            🕐 {hotline['available']}
            """)

        st.markdown("---")

        # Teen Resources
        st.subheader("📱 Teen Resources")
        for resource in RESOURCES["teen_resources"]:
            if "url" in resource:
                st.markdown(f"[{resource['name']}]({resource['url']}) - {resource['description']}")
            else:
                st.markdown(f"**{resource['name']}** - {resource['number']}  \n{resource['description']}")

        st.markdown("---")

        # Actions
        if st.button("🔄 New Session", use_container_width=True):
            # Clear chat history
            st.session_state.messages = []
            st.session_state.session_start = datetime.now()
            st.session_state.message_count = 0
            st.rerun()

        if st.button("🚪 Exit App", use_container_width=True):
            st.session_state.clear()
            st.rerun()


def display_chat_history():
    """Display chat message history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar", None)):
            st.markdown(message["content"])


def handle_user_input(model):
    """Handle user input and generate AI response."""
    if prompt := st.chat_input(f"Message TeenMind... (Hi {st.session_state.user_name}! 👋)"):
        # Check session time
        if st.session_state.session_start:
            elapsed = (datetime.now() - st.session_state.session_start).seconds
            if elapsed >= MAX_SESSION_TIME:
                st.warning("⏰ Session time limit reached. Starting a new session...")
                st.session_state.messages = []
                st.session_state.session_start = datetime.now()
                st.session_state.message_count = 0
                return

        # Display user message
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "🧑"})
        st.session_state.message_count += 1

        # Safety check
        is_crisis, category, crisis_response = st.session_state.safety_monitor.check_input(prompt)

        if is_crisis:
            # Crisis detected - show crisis response
            with st.chat_message("assistant", avatar="🧠"):
                st.markdown(crisis_response)

            st.session_state.messages.append({
                "role": "assistant",
                "content": crisis_response,
                "avatar": "🧠",
                "crisis": True
            })
            st.session_state.crisis_count += 1

            # Log crisis for monitoring
            st.warning(f"⚠️ Crisis keyword detected: {category}")

        else:
            # Normal response - generate with Gemini
            with st.chat_message("assistant", avatar="🧠"):
                with st.spinner("Thinking..."):
                    try:
                        # Build chat history for context (convert Streamlit roles to Gemini roles)
                        chat = model.start_chat(history=[
                            {
                                "role": "model" if msg["role"] == "assistant" else msg["role"],
                                "parts": [msg["content"]]
                            }
                            for msg in st.session_state.messages[:-1]  # Exclude current message
                            if not msg.get("crisis", False)  # Exclude crisis responses
                        ])

                        # Generate response
                        response = chat.send_message(prompt)

                        # Validate response safety
                        if not st.session_state.safety_monitor.check_response(response.text):
                            response_text = ("I want to be careful with my response here. "
                                           "This sounds like something really important to discuss with a "
                                           "trusted adult or counselor who can give you proper support. "
                                           "Would you like help finding resources?")
                        else:
                            response_text = response.text

                        st.markdown(response_text)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_text,
                            "avatar": "🧠"
                        })

                    except Exception as e:
                        error_msg = f"I'm having trouble responding right now. Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "I'm having some technical difficulties. Please try again, or reach out to a trusted adult if you need immediate support.",
                            "avatar": "🧠"
                        })


def handle_voice_input(model):
    """Handle voice input: record, transcribe, respond with TTS."""

    # Initialize processing flag
    if 'processing_voice' not in st.session_state:
        st.session_state.processing_voice = False

    # Audio input widget
    audio_bytes = st.audio_input(
        "🎤 Click to record your message",
        key="voice_input"
    )

    if audio_bytes:
        # Show waveform visualization
        waveform_html = get_audio_waveform_viz(audio_bytes.getvalue())
        st.components.v1.html(waveform_html, height=80)

        # Process button
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🗣️ Send Voice", use_container_width=True, type="primary"):
                # Store audio in session state and set processing flag
                st.session_state.audio_to_process = audio_bytes.getvalue()
                st.session_state.processing_voice = True
                st.rerun()

    # Process audio if flagged
    if st.session_state.processing_voice and hasattr(st.session_state, 'audio_to_process'):
        st.session_state.processing_voice = False
        audio_data = st.session_state.audio_to_process
        delattr(st.session_state, 'audio_to_process')

        # Process the message (this will add to session state)
        process_voice_message(audio_data, model)

        # Don't rerun - let the message appear naturally


def process_voice_message(audio_bytes: bytes, model):
    """Process voice message: transcribe, check safety, generate response with TTS."""

    # Check session time
    if st.session_state.session_start:
        elapsed = (datetime.now() - st.session_state.session_start).seconds
        if elapsed >= MAX_SESSION_TIME:
            st.warning("⏰ Session time limit reached. Starting a new session...")
            st.session_state.messages = []
            st.session_state.session_start = datetime.now()
            st.session_state.message_count = 0
            return

    # Transcribe audio
    text = process_voice_input(audio_bytes, st.session_state.voice_processor)

    if not text:
        return

    # Display transcribed user message
    with st.chat_message("user", avatar="🧑"):
        st.markdown(f"🎤 {text}")

    st.session_state.messages.append({"role": "user", "content": text, "avatar": "🧑"})
    st.session_state.message_count += 1

    # Safety check
    is_crisis, category, crisis_response = st.session_state.safety_monitor.check_input(text)

    if is_crisis:
        # Crisis detected - show crisis response
        with st.chat_message("assistant", avatar="🧠"):
            st.markdown(crisis_response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": crisis_response,
            "avatar": "🧠",
            "crisis": True
        })
        st.session_state.crisis_count += 1

        # Log crisis for monitoring
        st.warning(f"⚠️ Crisis keyword detected: {category}")

    else:
        # Normal response - generate with Gemini
        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("Thinking..."):
                try:
                    # Build chat history for context (convert Streamlit roles to Gemini roles)
                    chat = model.start_chat(history=[
                        {
                            "role": "model" if msg["role"] == "assistant" else msg["role"],
                            "parts": [msg["content"]]
                        }
                        for msg in st.session_state.messages[:-1]  # Exclude current message
                        if not msg.get("crisis", False)  # Exclude crisis responses
                    ])

                    # Generate response
                    response = chat.send_message(text)

                    # Validate response safety
                    if not st.session_state.safety_monitor.check_response(response.text):
                        response_text = ("I want to be careful with my response here. "
                                       "This sounds like something really important to discuss with a "
                                       "trusted adult or counselor who can give you proper support. "
                                       "Would you like help finding resources?")
                    else:
                        response_text = response.text

                    # Display text response
                    st.markdown(response_text)

                    # Play voice response
                    st.markdown("---")
                    play_voice_response(response_text, st.session_state.voice_processor)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text,
                        "avatar": "🧠"
                    })

                except Exception as e:
                    error_msg = f"I'm having trouble responding right now. Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "I'm having some technical difficulties. Please try again, or reach out to a trusted adult if you need immediate support.",
                        "avatar": "🧠"
                    })


def show_welcome_message():
    """Display initial welcome message."""
    if len(st.session_state.messages) == 0:
        welcome_msg = f"""Hey {st.session_state.user_name}! 👋

I'm TeenMind Companion, here to listen and support you. 💚

**I can help with:**
- Listening to what's on your mind (school, friends, family stress)
- Suggesting coping strategies (breathing exercises, grounding techniques)
- Connecting you to helpful resources

**Remember:** I'm an AI, not a therapist. For serious concerns or crisis situations, I'll point you to professional help (like 988 Crisis Lifeline).

**What's on your mind today?**"""

        with st.chat_message("assistant", avatar="🧠"):
            st.markdown(welcome_msg)

        st.session_state.messages.append({
            "role": "assistant",
            "content": welcome_msg,
            "avatar": "🧠"
        })


def main():
    """Main application flow."""
    init_session_state()

    # Age gate
    if not st.session_state.age_verified:
        show_age_gate()
        return

    # Consent screen
    if not st.session_state.consent_given:
        show_consent_screen()
        return

    # Main chat interface
    st.title("🧠✨ TeenMind Companion")

    # Initialize Gemini
    model = initialize_gemini()

    # Show sidebar
    show_sidebar()

    # Welcome message
    show_welcome_message()

    # Display chat history
    display_chat_history()

    # Voice Mode Selector
    st.markdown("---")
    st.subheader("🎙️ Communication Mode")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "💬 Text Chat",
            use_container_width=True,
            type="primary" if st.session_state.voice_mode_type == "text" else "secondary"
        ):
            st.session_state.voice_mode_type = "text"
            st.session_state.voice_mode_enabled = False
            stop_realtime_session()
            st.rerun()

    with col2:
        if st.button(
            "🎤 Turn-Based Voice",
            use_container_width=True,
            type="primary" if st.session_state.voice_mode_type == "turn-based" else "secondary"
        ):
            st.session_state.voice_mode_type = "turn-based"
            st.session_state.voice_mode_enabled = True
            stop_realtime_session()
            st.rerun()

    with col3:
        if st.button(
            "⚡ Real-Time Voice",
            use_container_width=True,
            type="primary" if st.session_state.voice_mode_type == "realtime" else "secondary"
        ):
            st.session_state.voice_mode_type = "realtime"
            st.session_state.voice_mode_enabled = False
            st.rerun()

    # Render appropriate interface based on mode
    if st.session_state.voice_mode_type == "realtime":
        # Real-time voice mode (Phase 3)
        render_realtime_voice_ui()

    elif st.session_state.voice_mode_type == "turn-based":
        # Turn-based voice mode (Phase 2)
        voice_enabled = render_voice_mode()
        if voice_enabled:
            handle_voice_input(model)

    else:
        # Text mode (Phase 1)
        handle_user_input(model)


if __name__ == "__main__":
    main()

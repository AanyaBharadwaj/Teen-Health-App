"""Voice mode functionality: audio recording, Speech-to-Text, and Text-to-Speech."""

import streamlit as st
import tempfile
import os
from typing import Optional
import google.generativeai as genai
from config import GEMINI_API_KEY, VOICE_CONFIG


class VoiceProcessor:
    """Handles voice recording, transcription, and synthesis."""

    def __init__(self):
        """Initialize voice processor with API configuration."""
        self.sample_rate = VOICE_CONFIG["sample_rate"]
        self.channels = VOICE_CONFIG["channels"]
        self.audio_format = VOICE_CONFIG["audio_format"]
        genai.configure(api_key=GEMINI_API_KEY)

    def transcribe_audio_simple(self, audio_bytes: bytes, status_container=None) -> Optional[str]:
        """
        Transcribe audio using simple SpeechRecognition library (fallback).

        Args:
            audio_bytes: Audio data in bytes
            status_container: Optional Streamlit container for status messages

        Returns:
            Transcribed text or None if failed
        """
        import speech_recognition as sr

        def show_status(msg):
            """Show status message in container or directly."""
            if status_container:
                status_container.info(msg)
            else:
                st.info(msg)

        tmp_path = None
        try:
            show_status("📝 Step 1/3: Saving audio file...")

            # Try to use pydub for format conversion (optional)
            try:
                from pydub import AudioSegment
                import io

                show_status("📝 Step 2/3: Converting audio format (this may take a moment)...")

                # Convert audio bytes to AudioSegment (handles multiple formats)
                audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

                # Convert to WAV format (required for speech_recognition)
                # Export as mono, 16kHz for best recognition
                audio = audio.set_channels(1).set_frame_rate(16000)

                # Save as WAV to temporary file
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                    audio.export(tmp_file.name, format="wav")
                    tmp_path = tmp_file.name

            except Exception as conversion_error:
                # Fallback: save raw audio bytes directly
                msg = f"⚠️ Audio conversion failed. Trying direct method..."
                if status_container:
                    status_container.warning(msg)
                else:
                    st.warning(msg)
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                    tmp_file.write(audio_bytes)
                    tmp_path = tmp_file.name

            show_status("📝 Step 3/3: Transcribing speech (this uses Google's API and requires internet)...")

            # Initialize recognizer
            recognizer = sr.Recognizer()

            # Adjust for ambient noise
            with sr.AudioFile(tmp_path) as source:
                # Listen for 0.5 seconds to calibrate for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = recognizer.record(source)

            # Transcribe using Google Speech Recognition (free)
            text = recognizer.recognize_google(audio_data, language="en-US", show_all=False)

            # Clean up temp file
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

            return text

        except sr.UnknownValueError:
            st.warning("🎤 Could not understand audio. Please speak clearly and try again.")
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            return None
        except sr.RequestError as e:
            st.error(f"❌ Speech recognition service error: {str(e)}\n\nPlease check your internet connection.")
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            return None
        except Exception as e:
            st.error(f"❌ Transcription error: {str(e)}\n\n**Possible fixes:**\n- Install ffmpeg: `brew install ffmpeg` (macOS) or `apt-get install ffmpeg` (Linux)\n- Check your internet connection\n- Try recording again with clearer audio")
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            return None

    def generate_speech_gemini(self, text: str) -> Optional[bytes]:
        """
        Generate speech from text using Gemini native TTS.

        Args:
            text: Text to convert to speech

        Returns:
            Audio bytes in MP3 format or None if failed
        """
        try:
            # For Phase 2, we use browser's native TTS
            # In Phase 3, we'll integrate Gemini Live for native audio
            return None  # Placeholder - will use browser TTS

        except Exception as e:
            st.error(f"❌ TTS generation error: {str(e)}")
            return None

    def text_to_speech_fallback(self, text: str) -> str:
        """
        Generate browser-compatible TTS using HTML5 audio.

        Args:
            text: Text to speak

        Returns:
            HTML string with TTS functionality
        """
        # Use browser's native Web Speech API for TTS
        # This is a lightweight solution for Phase 2
        # Escape backticks to prevent JavaScript syntax errors
        safe_text = text.replace('`', '\\`').replace('${', '\\${')

        tts_html = f"""
        <script>
            function speakText() {{
                const utterance = new SpeechSynthesisUtterance(`{safe_text}`);
                utterance.rate = 0.9;  // Slightly slower for clarity
                utterance.pitch = 1.0;
                utterance.volume = 1.0;

                // Try to use a calm, female voice (similar to "nova")
                const voices = window.speechSynthesis.getVoices();
                const preferredVoice = voices.find(v =>
                    v.name.includes('Samantha') ||
                    v.name.includes('Female') ||
                    v.name.includes('Zira')
                );
                if (preferredVoice) {{
                    utterance.voice = preferredVoice;
                }}

                window.speechSynthesis.speak(utterance);
            }}

            // Auto-play on load
            if (document.readyState === 'complete') {{
                speakText();
            }} else {{
                window.addEventListener('load', speakText);
            }}
        </script>

        <div style="
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            text-align: center;
        ">
            <p style="margin: 0; color: #00ff88;">🔊 Playing audio response...</p>
            <button onclick="speakText()" style="
                background: linear-gradient(90deg, #00ff88, #00d4ff);
                color: #0f0f23;
                border: none;
                border-radius: 20px;
                padding: 8px 20px;
                margin-top: 10px;
                cursor: pointer;
                font-weight: bold;
            ">🔁 Replay</button>
        </div>
        """
        return tts_html


def render_voice_mode():
    """Render the voice mode UI component."""
    st.markdown("---")

    # Voice mode toggle header
    col1, col2, col3 = st.columns([2, 3, 2])

    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <h2 style="margin-bottom: 10px;">🎤 Voice Mode</h2>
            <p style="opacity: 0.8; font-size: 14px;">Speak naturally, get voice responses</p>
        </div>
        """, unsafe_allow_html=True)

    # Voice mode toggle
    if 'voice_mode_enabled' not in st.session_state:
        st.session_state.voice_mode_enabled = False

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Toggle button with enhanced styling
        button_text = "🎤 Enable Voice Mode" if not st.session_state.voice_mode_enabled else "⌨️ Switch to Text Mode"
        button_type = "primary" if not st.session_state.voice_mode_enabled else "secondary"

        if st.button(button_text, use_container_width=True, type=button_type):
            st.session_state.voice_mode_enabled = not st.session_state.voice_mode_enabled
            st.rerun()

    # Show voice input if enabled
    if st.session_state.voice_mode_enabled:
        st.markdown("""
        <div class="voice-active" style="
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 212, 255, 0.1));
            border: 2px solid #00ff88;
            border-radius: 20px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.2);
        ">
            <div style="text-align: center;">
                <h3 style="color: #00ff88; margin-top: 0; text-shadow: 0 0 10px #00ff88;">
                    🎙️ Voice Input Active
                </h3>
                <p style="color: #e0e0e0; font-size: 16px; margin: 15px 0;">
                    Click the microphone below to start recording
                </p>
            </div>

            <div style="
                background: rgba(255, 255, 255, 0.03);
                border-radius: 15px;
                padding: 20px;
                margin-top: 15px;
            ">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; color: #e0e0e0;">
                    <div>
                        <div style="font-size: 24px; margin-bottom: 5px;">🎵</div>
                        <div style="font-size: 13px; opacity: 0.8;">WAV, MP3, M4A, OGG</div>
                    </div>
                    <div>
                        <div style="font-size: 24px; margin-bottom: 5px;">⏱️</div>
                        <div style="font-size: 13px; opacity: 0.8;">Max 60 seconds</div>
                    </div>
                    <div>
                        <div style="font-size: 24px; margin-bottom: 5px;">🔊</div>
                        <div style="font-size: 13px; opacity: 0.8;">Speak clearly</div>
                    </div>
                    <div>
                        <div style="font-size: 24px; margin-bottom: 5px;">🌐</div>
                        <div style="font-size: 13px; opacity: 0.8;">Internet required</div>
                    </div>
                </div>
            </div>

            <div style="text-align: center; margin-top: 20px; padding: 15px; background: rgba(0, 212, 255, 0.1); border-radius: 10px;">
                <p style="margin: 0; color: #00d4ff; font-size: 14px;">
                    💡 <b>Tip:</b> Your voice will be transcribed and appear in the chat
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        return True

    else:
        # Show info about voice mode when disabled
        with st.expander("ℹ️ About Voice Mode", expanded=False):
            st.markdown("""
            **Voice Mode Features:**
            - 🎤 **Record** your message instead of typing
            - 🗣️ **AI responds** with spoken voice
            - 💬 **Transcripts** appear in chat history
            - 🔄 **Replay** audio responses anytime

            **How it works:**
            1. Click "Enable Voice Mode" above
            2. Record or upload your audio
            3. AI transcribes your speech
            4. Get text + voice response

            **Requirements:**
            - Internet connection (for transcription)
            - Microphone access (browser permission)
            - Clear audio in quiet environment
            """)

    return False


def process_voice_input(audio_bytes: bytes, processor: VoiceProcessor) -> Optional[str]:
    """
    Process voice input: transcribe audio to text.

    Args:
        audio_bytes: Recorded audio data
        processor: VoiceProcessor instance

    Returns:
        Transcribed text or None
    """
    # Create a persistent status container
    status_container = st.empty()

    # The transcription function now shows its own progress
    text = processor.transcribe_audio_simple(audio_bytes, status_container)

    # Clear status messages after completion
    status_container.empty()

    if text:
        st.success(f"✅ **Transcribed:** \"{text}\"")
        return text
    else:
        st.error("❌ Transcription failed. Please try again.")
        return None


def play_voice_response(text: str, processor: VoiceProcessor):
    """
    Play AI response as voice.

    Args:
        text: Response text to speak
        processor: VoiceProcessor instance
    """
    # For Phase 2, use browser TTS (lightweight)
    tts_html = processor.text_to_speech_fallback(text)
    st.components.v1.html(tts_html, height=100)


def get_audio_waveform_viz(_audio_bytes: bytes) -> str:
    """
    Generate a simple waveform visualization for audio.

    Args:
        _audio_bytes: Audio data (not used in current implementation)

    Returns:
        HTML string with waveform visualization
    """
    # Simple animated waveform using CSS
    waveform_html = """
    <div style="
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 3px;
        padding: 20px;
        background: rgba(0, 255, 136, 0.05);
        border-radius: 10px;
        margin: 10px 0;
    ">
        <div class="wave-bar" style="animation-delay: 0s;"></div>
        <div class="wave-bar" style="animation-delay: 0.1s;"></div>
        <div class="wave-bar" style="animation-delay: 0.2s;"></div>
        <div class="wave-bar" style="animation-delay: 0.3s;"></div>
        <div class="wave-bar" style="animation-delay: 0.4s;"></div>
        <div class="wave-bar" style="animation-delay: 0.5s;"></div>
        <div class="wave-bar" style="animation-delay: 0.6s;"></div>
    </div>

    <style>
        .wave-bar {
            width: 4px;
            height: 20px;
            background: linear-gradient(180deg, #00ff88, #00d4ff);
            border-radius: 2px;
            animation: wave 1s ease-in-out infinite;
        }

        @keyframes wave {
            0%, 100% { height: 20px; }
            50% { height: 40px; }
        }
    </style>
    """
    return waveform_html

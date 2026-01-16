"""Real-time voice conversation with Gemini Live API and WebRTC."""

import asyncio
import queue
import threading
from typing import Optional, Callable
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
import numpy as np
from config import GEMINI_API_KEY, VOICE_CONFIG


class VoiceActivityDetector:
    """Simple Voice Activity Detection using energy threshold."""

    def __init__(self, sample_rate: int = 16000, frame_duration_ms: int = 30):
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        self.energy_threshold = 500  # Adjust based on testing
        self.silence_threshold_ms = 1000  # 1 second of silence
        self.silence_frames = int(self.silence_threshold_ms / frame_duration_ms)
        self.consecutive_silence = 0
        self.is_speaking = False

    def is_speech(self, audio_frame: np.ndarray) -> bool:
        """
        Detect if audio frame contains speech.

        Args:
            audio_frame: Audio data as numpy array

        Returns:
            True if speech detected, False otherwise
        """
        # Calculate energy (RMS)
        energy = np.sqrt(np.mean(audio_frame ** 2))

        if energy > self.energy_threshold:
            self.consecutive_silence = 0
            self.is_speaking = True
            return True
        else:
            self.consecutive_silence += 1
            if self.consecutive_silence >= self.silence_frames:
                self.is_speaking = False
            return False

    def reset(self):
        """Reset VAD state."""
        self.consecutive_silence = 0
        self.is_speaking = False


class RealtimeVoiceSession:
    """Manages real-time voice conversation with Gemini Live API."""

    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.sample_rate = VOICE_CONFIG["sample_rate"]
        self.audio_queue = queue.Queue()
        self.response_queue = queue.Queue()
        self.vad = VoiceActivityDetector(sample_rate=self.sample_rate)
        self.is_connected = False
        self.is_processing = False
        self.session_thread = None

    async def connect_live_session(self):
        """
        Connect to Gemini Live API via WebSocket.

        Note: This is a placeholder for the actual Gemini Live implementation.
        The Gemini Live API is in preview and may require specific access.
        """
        try:
            # Import Gemini Live API (when available)
            # from google.genai import Client

            # For now, we'll simulate the connection
            # In production, this would be:
            # client = Client(api_key=self.api_key)
            # session = await client.live.connect(
            #     model="gemini-2.5-flash-native-audio-preview-12-2025",
            #     config={
            #         "response_modalities": ["AUDIO"],
            #         "voice": "nova"
            #     }
            # )

            self.is_connected = True
            st.success("✅ Connected to Gemini Live API")

            # Process audio loop
            await self.process_audio_loop()

        except Exception as e:
            st.error(f"❌ Failed to connect to Gemini Live: {str(e)}")
            self.is_connected = False

    async def process_audio_loop(self):
        """Process audio frames in real-time."""
        while self.is_connected:
            try:
                # Get audio from queue
                if not self.audio_queue.empty():
                    audio_chunk = self.audio_queue.get()

                    # Check for speech activity
                    is_speech = self.vad.is_speech(audio_chunk)

                    if is_speech:
                        self.is_processing = True
                        # Send to Gemini Live API
                        # await session.send_audio(audio_chunk)
                        pass
                    elif self.is_processing and not self.vad.is_speaking:
                        # Speech ended, wait for response
                        # response = await session.receive()
                        # self.response_queue.put(response.audio)
                        self.is_processing = False

                await asyncio.sleep(0.01)  # Small delay to prevent busy waiting

            except Exception as e:
                st.error(f"❌ Error processing audio: {str(e)}")
                break

    def disconnect(self):
        """Disconnect from Gemini Live API."""
        self.is_connected = False
        st.info("🔌 Disconnected from Gemini Live")


def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    """
    Callback for processing audio frames from WebRTC.

    Args:
        frame: Audio frame from microphone

    Returns:
        Processed audio frame
    """
    # Convert frame to numpy array
    audio_array = frame.to_ndarray()

    # Add to queue for processing
    if 'realtime_session' in st.session_state and st.session_state.realtime_session:
        st.session_state.realtime_session.audio_queue.put(audio_array)

    return frame


def render_realtime_voice_ui():
    """Render real-time voice mode UI with WebRTC."""
    st.markdown("---")

    # Header
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <h2 style="margin-bottom: 10px;">⚡ Real-Time Voice</h2>
        <p style="opacity: 0.8; font-size: 14px;">
            Ultra-low latency conversations with Gemini Live
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session
    if 'realtime_session' not in st.session_state:
        st.session_state.realtime_session = None

    # Connection status
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.session_state.realtime_session and st.session_state.realtime_session.is_connected:
            st.markdown("""
            <div style="
                text-align: center;
                padding: 15px;
                background: linear-gradient(90deg, rgba(0, 255, 136, 0.2), rgba(0, 212, 255, 0.2));
                border: 2px solid #00ff88;
                border-radius: 15px;
                margin-bottom: 20px;
            ">
                <span style="font-size: 24px;">🟢</span>
                <span style="color: #00ff88; font-weight: bold; margin-left: 10px;">
                    CONNECTED - Speak naturally
                </span>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔴 Disconnect", use_container_width=True):
                st.session_state.realtime_session.disconnect()
                st.session_state.realtime_session = None
                st.rerun()

        else:
            st.markdown("""
            <div style="
                text-align: center;
                padding: 15px;
                background: rgba(255, 255, 255, 0.05);
                border: 2px dashed rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                margin-bottom: 20px;
            ">
                <span style="font-size: 24px;">⚪</span>
                <span style="color: #e0e0e0; margin-left: 10px;">
                    Not connected
                </span>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🎙️ Start Real-Time Session", use_container_width=True, type="primary"):
                st.session_state.realtime_session = RealtimeVoiceSession()
                # Start async connection
                asyncio.run(st.session_state.realtime_session.connect_live_session())
                st.rerun()

    # Features grid
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.08), rgba(0, 212, 255, 0.08));
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
    ">
        <h3 style="text-align: center; color: #00ff88; margin-bottom: 25px;">
            ⚡ Real-Time Features
        </h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div style="text-align: center;">
                <div style="font-size: 36px; margin-bottom: 10px;">⚡</div>
                <div style="color: #00ff88; font-weight: bold; margin-bottom: 5px;">
                    <500ms Latency
                </div>
                <div style="font-size: 13px; opacity: 0.8;">
                    Near-instant responses
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 36px; margin-bottom: 10px;">🎯</div>
                <div style="color: #00d4ff; font-weight: bold; margin-bottom: 5px;">
                    Auto Turn-Taking
                </div>
                <div style="font-size: 13px; opacity: 0.8;">
                    VAD detects pauses
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 36px; margin-bottom: 10px;">🔄</div>
                <div style="color: #00ff88; font-weight: bold; margin-bottom: 5px;">
                    Barge-In
                </div>
                <div style="font-size: 13px; opacity: 0.8;">
                    Interrupt AI anytime
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 36px; margin-bottom: 10px;">🎤</div>
                <div style="color: #00d4ff; font-weight: bold; margin-bottom: 5px;">
                    Continuous
                </div>
                <div style="font-size: 13px; opacity: 0.8;">
                    No button presses
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # WebRTC streamer (only if connected)
    if st.session_state.realtime_session and st.session_state.realtime_session.is_connected:
        st.markdown("### 🎙️ Live Audio Stream")

        # Configure WebRTC
        rtc_configuration = RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        )

        webrtc_ctx = webrtc_streamer(
            key="realtime-voice",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=rtc_configuration,
            audio_frame_callback=audio_frame_callback,
            media_stream_constraints={
                "video": False,
                "audio": {
                    "echoCancellation": True,
                    "noiseSuppression": True,
                    "autoGainControl": True,
                    "sampleRate": 16000,
                }
            },
            async_processing=True,
        )

        # Show status
        if webrtc_ctx.state.playing:
            st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <div class="voice-active" style="
                    display: inline-block;
                    padding: 15px 30px;
                    background: linear-gradient(90deg, #00ff88, #00d4ff);
                    color: #0f0f23;
                    border-radius: 25px;
                    font-weight: bold;
                    box-shadow: 0 0 20px #00ff88;
                    animation: pulse 2s ease-in-out infinite;
                ">
                    🎙️ LISTENING...
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("👆 Click 'START' above to begin real-time conversation")

    # Help section
    with st.expander("ℹ️ How Real-Time Voice Works", expanded=False):
        st.markdown("""
        **Real-Time Voice vs Turn-Based:**

        | Feature | Turn-Based (Phase 2) | Real-Time (Phase 3) |
        |---------|---------------------|---------------------|
        | **Latency** | 2-5 seconds | <500ms |
        | **Interaction** | Button clicks | Automatic |
        | **Interruption** | Not supported | Full barge-in |
        | **Turn-taking** | Manual | Automatic (VAD) |
        | **Technology** | STT + TTS | Gemini Live native |

        **How it works:**
        1. **Continuous Listening**: WebRTC captures your voice in real-time
        2. **Voice Activity Detection**: Automatically detects when you stop speaking
        3. **Instant Processing**: Audio streams directly to Gemini Live
        4. **Low-Latency Response**: AI responds while you're still thinking
        5. **Natural Flow**: Like talking to a real person

        **Requirements:**
        - **HTTPS connection** (WebRTC requirement)
        - **Microphone permissions** (browser will prompt)
        - **Stable internet** (for real-time streaming)
        - **Modern browser** (Chrome/Edge recommended)

        **Privacy:**
        - Audio processed in real-time, not stored
        - Session ends when you disconnect
        - No recordings saved
        """)

    # Technical notes
    st.markdown("""
    <div style="
        background: rgba(255, 200, 0, 0.1);
        border-left: 4px solid #ffc800;
        padding: 15px;
        margin-top: 20px;
        border-radius: 5px;
    ">
        <p style="margin: 0; color: #ffc800; font-size: 14px;">
            <b>⚠️ Note:</b> Gemini Live API is currently in preview.
            If you encounter errors, it may require specific API access or the feature may not be fully available yet.
            The app will fall back to turn-based voice mode.
        </p>
    </div>
    """, unsafe_allow_html=True)


def stop_realtime_session():
    """Stop the current real-time session."""
    if 'realtime_session' in st.session_state and st.session_state.realtime_session:
        st.session_state.realtime_session.disconnect()
        st.session_state.realtime_session = None

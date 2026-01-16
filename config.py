"""Configuration settings for TeenMind Companion app."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model Configuration
TEXT_MODEL = "gemini-2.5-flash"  # Using available free tier model with better quota
LIVE_VOICE_MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"

# Generation Config
GENERATION_CONFIG = {
    "temperature": 0.7,  # Balanced for empathy
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 1000,  # ~30s speech equivalent
}

# Safety Settings - Balanced for teen safety
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Crisis Keywords - Comprehensive list for detection
CRISIS_KEYWORDS = {
    "self_harm": [
        "cut myself", "cutting", "self harm", "hurt myself", "self-harm",
        "bleed", "bleeding", "razor", "blade", "burn myself"
    ],
    "suicide": [
        "kill myself", "end my life", "suicide", "suicidal", "want to die",
        "better off dead", "end it all", "not worth living", "take my life",
        "hang myself", "overdose", "jump off"
    ],
    "severe_distress": [
        "can't go on", "nothing matters", "no point", "give up",
        "hopeless", "worthless", "nobody cares"
    ],
    "psychosis": [
        "hearing voices", "voices tell me", "see things", "hallucinating",
        "crystal ball", "future seeing", "mind control", "they're watching"
    ],
    "abuse": [
        "being hurt", "someone hurts me", "touches me", "abuse",
        "hit me", "scared of", "unsafe at home"
    ]
}

# Crisis Response Templates
CRISIS_RESPONSE = """🚨 I'm really concerned about what you just shared. **This is serious, and you deserve immediate help from a trained professional.**

**URGENT - Please reach out RIGHT NOW:**
📞 **Call/Text 988** - Suicide & Crisis Lifeline (24/7, free, confidential)
💬 **Text HOME to 741741** - Crisis Text Line (24/7)
🏳️‍🌈 **Trevor Project: 1-866-488-7386** (LGBTQ+ youth, 24/7)

**You are valuable. You matter. Real people care about you.**

I'm an AI companion for coping tips and listening, but I **cannot replace professional help** in emergencies. Please talk to a trusted adult (parent, teacher, counselor) or call the numbers above.

Would you like me to help you find local resources or talk about something else while you reach out?"""

# UI Theme - Neon Dark Mode
THEME = {
    "background_gradient": "linear-gradient(135deg, #0f0f23 0%, #1a0033 100%)",
    "primary_color": "#00ff88",
    "secondary_color": "#ff00ff",
    "text_color": "#e0e0e0",
    "accent_color": "#00d4ff"
}

# Session Configuration
MAX_SESSION_TIME = 900  # 15 minutes in seconds
MIN_USER_AGE = 13
MAX_HISTORY_LENGTH = 50  # messages

# Resources
RESOURCES = {
    "crisis_hotlines": [
        {"name": "988 Suicide & Crisis Lifeline", "number": "988", "available": "24/7"},
        {"name": "Crisis Text Line", "number": "Text HOME to 741741", "available": "24/7"},
        {"name": "Trevor Project (LGBTQ+)", "number": "1-866-488-7386", "available": "24/7"},
        {"name": "SAMHSA National Helpline", "number": "1-800-662-4357", "available": "24/7"},
    ],
    "teen_resources": [
        {"name": "Teen Line", "url": "https://teenlineonline.org", "description": "Teen-to-teen support"},
        {"name": "7 Cups", "url": "https://www.7cups.com", "description": "Free emotional support"},
        {"name": "Your Life Your Voice", "number": "1-800-448-3000", "description": "Boys Town National Hotline"},
    ]
}

# Voice Configuration
VOICE_CONFIG = {
    "sample_rate": 16000,
    "channels": 1,
    "vad_aggressiveness": 2,  # 0-3, 2 for ~1s pause
    "silence_threshold": 1.0,  # seconds
    "voice_name": "nova",  # Calm female voice
    "audio_format": "mp3"
}

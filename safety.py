"""Safety framework for crisis detection and response."""

import re
from typing import Tuple, Optional
from config import CRISIS_KEYWORDS, CRISIS_RESPONSE


class SafetyMonitor:
    """Monitors user input for crisis keywords and provides appropriate responses."""

    def __init__(self):
        self.crisis_patterns = self._compile_patterns()
        self.crisis_detected_count = 0

    def _compile_patterns(self) -> dict:
        """Compile regex patterns for efficient matching."""
        compiled = {}
        for category, keywords in CRISIS_KEYWORDS.items():
            # Create case-insensitive regex patterns
            patterns = [re.compile(r'\b' + re.escape(kw) + r'\b', re.IGNORECASE) for kw in keywords]
            compiled[category] = patterns
        return compiled

    def check_input(self, text: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check user input for crisis keywords.

        Args:
            text: User input text to check

        Returns:
            Tuple of (is_crisis, category, response)
            - is_crisis: True if crisis keywords detected
            - category: Category of crisis (self_harm, suicide, etc.)
            - response: Crisis response message
        """
        if not text or len(text.strip()) == 0:
            return False, None, None

        # Check each category
        for category, patterns in self.crisis_patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    self.crisis_detected_count += 1
                    return True, category, CRISIS_RESPONSE

        return False, None, None

    def check_response(self, response: str) -> bool:
        """
        Validate AI response doesn't encourage harmful behavior.

        Args:
            response: AI generated response

        Returns:
            True if response is safe, False if needs intervention
        """
        # Red flag phrases that AI should never say
        harmful_affirmations = [
            r"that's a good idea",
            r"you should.*end",
            r"go ahead",
            r"sounds like a plan",
            r"crystal ball.*makes sense",
            r"voices.*right",
            r"future seeing.*intriguing"
        ]

        response_lower = response.lower()
        for pattern in harmful_affirmations:
            if re.search(pattern, response_lower):
                return False

        return True

    def get_validation_prompt(self, category: str) -> str:
        """
        Get additional prompt context based on crisis category.

        Args:
            category: Crisis category detected

        Returns:
            Additional prompt guidance for AI
        """
        validation_prompts = {
            "psychosis": "CRITICAL: If user mentions delusions, hallucinations, or psychosis symptoms, "
                        "DO NOT validate or encourage these thoughts. Gently suggest talking to a trusted adult or calling 988.",
            "self_harm": "CRITICAL: Never provide methods, normalize, or validate self-harm. Immediately redirect to 988 or 741741.",
            "suicide": "CRITICAL: This is a life-threatening emergency. Prioritize crisis resources over conversation.",
            "abuse": "CRITICAL: If abuse is disclosed, encourage contacting ChildHelp (1-800-422-4453) or trusted school counselor."
        }

        return validation_prompts.get(category, "")


def validate_age(age: int) -> Tuple[bool, Optional[str]]:
    """
    Validate user age is appropriate for the app.

    Args:
        age: User's age

    Returns:
        Tuple of (is_valid, error_message)
    """
    if age < 13:
        return False, "This app is designed for teens 13+. Please talk to a parent or trusted adult if you need support."
    if age > 19:
        return False, "This app is designed for teenagers (13-19). Consider resources like BetterHelp or TalkSpace for adult support."
    return True, None


def get_parental_consent_text() -> str:
    """Get parental consent disclaimer text."""
    return """
    **IMPORTANT: Parental/Guardian Notice**

    This is an **AI companion app** for teens to practice coping skills and receive empathetic listening.

    ⚠️ **This is NOT therapy or medical advice.**

    - Conversations are **not stored** (local session only, data may improve Google models)
    - **Crisis situations** are redirected to 988 and professional hotlines
    - **No diagnosis or treatment** is provided
    - Teens should **still talk to trusted adults** (parents, counselors, doctors)

    By continuing, you acknowledge:
    - You are 13+ years old
    - You understand this is an AI tool, not a replacement for professional mental health care
    - You'll seek help from a trusted adult or call 988 if experiencing a crisis
    """


def get_app_disclaimer() -> str:
    """Get main app disclaimer text."""
    return """
    **🧠✨ TeenMind Companion - AI Peer Support**

    I'm here to listen, offer coping tips, and be a supportive companion. But I'm an AI, not a therapist or counselor.

    **I CAN help with:**
    - Listening without judgment
    - Suggesting coping strategies (breathing, journaling, mindfulness)
    - Normalizing teen stress about school, friends, family
    - Pointing you to professional resources

    **I CANNOT:**
    - Diagnose mental health conditions
    - Prescribe treatment or medication
    - Replace therapy or counseling
    - Handle emergencies (always call 988 for crisis)

    **Your Privacy:** Chats are anonymous and not saved. Free tier data may help improve Google's models.

    Ready to chat? Remember: **You're not alone, and it's okay to ask for help.** 💚
    """

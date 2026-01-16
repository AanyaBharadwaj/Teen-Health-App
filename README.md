# 🧠✨ TeenMind Companion

An empathetic AI peer support companion for teenagers (ages 13-19) navigating mental health challenges. Built with Streamlit and Google's Gemini AI, emphasizing safety, privacy, and ethical considerations.

## ⚠️ Important Disclaimer

**THIS IS NOT A REPLACEMENT FOR PROFESSIONAL MENTAL HEALTH CARE.**

TeenMind Companion is:
- ✅ An AI tool for coping tips and empathetic listening
- ✅ A bridge to professional resources
- ❌ NOT therapy, counseling, or medical advice
- ❌ NOT a crisis intervention service

**Crisis situations are redirected to 988 Suicide & Crisis Lifeline and other professional hotlines.**

## 🎯 Features

### Phase 1: Text-Based Chat (✅ Implemented)
- Real-time chat with Gemini AI
- Comprehensive safety framework with crisis keyword detection
- Age verification and parental consent
- Session time limits (15 minutes)
- Crisis resource integration (988, Trevor Project, etc.)
- Neon dark theme UI optimized for teens
- Privacy-focused (no data storage, session-only)

### Phase 2: Turn-Based Voice Mode (🚧 Upcoming)
- Audio recording with `st.audio_input()`
- Google Speech-to-Text integration
- Gemini native Text-to-Speech
- Audio playback

### Phase 3: Real-Time Voice (🚧 Upcoming)
- `streamlit-webrtc` for low-latency audio
- Voice Activity Detection (VAD)
- Gemini Live API with WebSocket streaming
- Real-time interruption handling

### Phase 4: Enhancements (🚧 Upcoming)
- Mood tracker with visualization
- Coping strategies library
- Anonymous usage analytics

### Phase 5: Deployment (🚧 Upcoming)
- Streamlit Cloud deployment
- HeyGen avatar integration for lip-sync
- Production safety monitoring

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Gemini API key (free tier from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone/Navigate to the project:**
   ```bash
   cd /Users/kaarthik/LLM/teenmind
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   Your `.env` file is already configured:
   ```
   GEMINI_API_KEY='your-api-key-here'
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser:**
   The app will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
teenmind/
├── app.py                 # Main Streamlit application (Phase 1)
├── config.py              # Configuration, safety settings, resources
├── safety.py              # Safety framework (crisis detection, validation)
├── prompts.py             # System prompts and coping strategies
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
└── README.md             # This file
```

## 🛡️ Safety Framework

### Crisis Detection
Monitors user input for 50+ keywords across categories:
- Self-harm (cutting, burning, etc.)
- Suicide (ideation, planning, methods)
- Severe distress (hopelessness, worthlessness)
- Psychosis (hallucinations, delusions)
- Abuse (physical, sexual, emotional)

**Action:** Immediate redirection to 988 and crisis resources.

### AI Response Validation
Post-generation checks prevent harmful affirmations:
- ❌ Blocks validation of delusions ("crystal ball sounds intriguing")
- ❌ Prevents normalization of self-harm
- ❌ Stops engagement with suicide ideation

### System Prompt Engineering
400+ token instruction set based on:
- APA 2025 guidelines for AI in youth mental health
- Common Sense Media safety benchmarks
- Stanford Brainstorm Lab research
- JAMA psychiatric best practices

Key constraints:
- **Cannot diagnose** ("sounds like depression" → "persistent sadness—talk to counselor")
- **Cannot prescribe** ("try Zoloft" → "doctor can explore medication options")
- **Cannot replace therapy** (redirects complex issues to professionals)
- **Must validate emotions** without validating harmful thoughts

### Privacy Protection
- No conversation logs or databases
- Session-only storage (cleared on exit)
- No personal identifiable information (PII) collected
- Free tier data may improve Google models (disclosed to users)

**Note:** NOT HIPAA-compliant. Personal project only—not for clinical use.

## 🎨 UI/UX Design

### Neon Dark Theme
- **Background:** Deep purple-black gradient (#0f0f23 → #1a0033)
- **Primary Color:** Neon green (#00ff88) with glow effects
- **Accent:** Cyan (#00d4ff) for interactive elements
- **Typography:** Clean, readable sans-serif

### Teen-Friendly Features
- Emoji avatars (🧑 user, 🧠 AI)
- Conversational tone (peer, not parent/therapist)
- Quick access to crisis resources in sidebar
- Session timer to encourage breaks
- Clear disclaimers without overwhelming text

## 📊 Technical Details

### Gemini API Configuration

**Model:** `gemini-2.0-flash-exp` (free tier)
- **Rate Limits:** 10 RPM, 250k TPM (late 2025 free tier)
- **Temperature:** 0.7 (balanced empathy/accuracy)
- **Max Output:** 1000 tokens (~30s speech equivalent)

**Safety Settings:**
- Harassment: `BLOCK_MEDIUM_AND_ABOVE`
- Hate Speech: `BLOCK_MEDIUM_AND_ABOVE`
- Sexual Content: `BLOCK_ONLY_HIGH`
- Dangerous Content: `BLOCK_MEDIUM_AND_ABOVE`

### Session Management
- **Max Duration:** 15 minutes (prevents over-reliance)
- **Message History:** Up to 50 messages (context window)
- **Auto-Reset:** Session clears after time limit

### Dependencies
- `streamlit==1.32.0` - Web framework
- `google-generativeai==0.8.1` - Gemini API
- `python-dotenv==1.0.1` - Environment variables
- `plotly==5.18.0` - Future mood tracking charts
- `streamlit-webrtc==0.47.7` - Phase 3 real-time voice
- `webrtcvad==2.0.10` - Voice activity detection
- `pydub==0.25.1` - Audio processing

## 🧪 Testing Protocol

### Pre-Deployment Checklist
- [ ] Age gate blocks users <13 and >19
- [ ] Consent screen displays all disclaimers
- [ ] Crisis keywords trigger 988 response (test all 50+ keywords)
- [ ] AI does NOT validate delusions or self-harm
- [ ] Session timer enforces 15-minute limit
- [ ] Sidebar crisis resources are accessible
- [ ] No PII is logged or stored

### Scenario Testing (Minimum 100 Conversations)
Based on JAMA mental health scenarios:
1. **Anxiety** (school, social, performance) - 20 tests
2. **Depression** (sadness, isolation, hopelessness) - 20 tests
3. **Stress** (homework, family, friends) - 20 tests
4. **Crisis** (suicide, self-harm, abuse) - 20 tests
5. **Edge Cases** (psychosis, eating disorders, substance use) - 20 tests

**Success Criteria:** 80%+ appropriate redirection rate for crisis scenarios.

## 📞 Crisis Resources Integrated

### 24/7 Hotlines
- **988** - Suicide & Crisis Lifeline (call/text)
- **741741** - Crisis Text Line (text HOME)
- **1-866-488-7386** - Trevor Project (LGBTQ+ youth)
- **1-800-422-4453** - ChildHelp (abuse)
- **1-800-662-4357** - SAMHSA (substance use)
- **1-800-931-2237** - NEDA (eating disorders)

### Teen-Specific Resources
- **Teen Line** - 800-852-8336 (teen-to-teen, 6-10pm PT)
- **7 Cups** - Free emotional support chat
- **Mindshift CBT** - Free anxiety app
- **Calm Harm** - Self-harm urge management

## ⚖️ Legal & Ethical Considerations

### Age Requirements
- **COPPA Compliant:** 13+ only (verified)
- **Parental Awareness:** Consent screen encourages parent/guardian discussion
- **Teen Autonomy:** Balances safety with respect for teen privacy

### Liability Limitations
- **Disclaimer:** Prominently displayed (cannot be missed)
- **No Medical Claims:** Never diagnoses, treats, or prescribes
- **Crisis Handoff:** All emergencies redirected to professionals
- **Non-Clinical:** Personal project—not FDA-regulated medical device

### Data Ethics
- **Minimal Collection:** Age and name (optional) only
- **No Retention:** Session-only, no databases
- **Transparency:** Users informed data may train Google models
- **Future:** Vertex AI for HIPAA BAA if commercialized

### Research Foundation
Design informed by:
- Common Sense Media (2025) - AI chatbot safety report
- Stanford Brainstorm Lab - Teen mental health AI study
- APA Guidelines - AI in youth psychology
- JAMA Psychiatry - Conversational AI benchmarks

**Key Finding:** General AI chatbots fail teen mental health safety (22-40% multi-turn failure rate). This app addresses gaps with custom prompts, crisis detection, and strict no-therapy boundaries.

## 🔮 Roadmap

### Immediate Next Steps
1. ✅ Phase 1: Text chat (COMPLETED)
2. 🚧 Phase 2: Turn-based voice (2-3 weeks)
3. 🚧 Phase 3: Real-time voice (3-4 weeks)
4. 🚧 Phase 4: Mood tracking (1 week)
5. 🚧 Phase 5: Deployment (1 week)

### Future Enhancements
- [ ] Multi-language support (Spanish, Mandarin)
- [ ] Integration with Woebot/Wysa APIs (evidence-based)
- [ ] Parent/guardian dashboard (optional, with teen consent)
- [ ] School counselor referral system
- [ ] Offline mode with cached coping strategies
- [ ] HeyGen avatar for visual engagement

## 💰 Cost Estimates

### Current (Free Tier)
- **Gemini API:** Free (up to 250k TPM, ~20-250 RPD)
- **Streamlit Hosting:** Free (Community Cloud)
- **Total:** $0/month

### If Scaled Beyond Free Tier
- **Gemini (Vertex AI):** ~$0.50/M input tokens
- **Gemini Live:** Preview free (2026 pricing TBD, est. $0.10/min)
- **HeyGen Avatar:** ~$0.10/min video generation
- **Estimated:** $50-200/month for 1000 users

## 🤝 Contributing

This is a personal safety-critical project. If you want to adapt it:

1. **Maintain Safety First:** Do NOT remove crisis detection or disclaimers
2. **Test Rigorously:** Minimum 100 scenario tests before any deployment
3. **Legal Review:** Consult attorney for liability (especially if public)
4. **Ethics Consultation:** Partner with licensed mental health professionals

## 📜 License

This project is for educational purposes. If adapting for production:
- Consult legal counsel (liability, COPPA, state laws)
- Partner with licensed clinicians for safety audits
- Consider malpractice insurance if offering to public
- Ensure compliance with telehealth regulations

## 📧 Support

For technical issues with this implementation:
- Check `streamlit run app.py` logs for errors
- Verify `.env` file has valid `GEMINI_API_KEY`
- Ensure Python 3.9+ and dependencies installed

**For mental health crisis:**
- **Call/Text 988** (Suicide & Crisis Lifeline)
- **Text HOME to 741741** (Crisis Text Line)

---

**Built with care for teen mental health. Remember: It's okay to not be okay, and it's brave to ask for help.** 💚

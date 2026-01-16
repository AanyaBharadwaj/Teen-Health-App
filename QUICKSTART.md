# 🚀 Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

or with Python 3.11 explicitly:

```bash
python3.11 -m pip install -r requirements.txt
```

## Step 2: Configure API Key

Your `.env` file is already set up with:
```
GEMINI_API_KEY='your-api-key-here'
```

## Step 3: Test the Setup (Optional)

```bash
python3.11 test_setup.py
```

This will:
- ✅ Verify API connection
- ✅ List available models
- ✅ Test text generation

## Step 4: Run the App

**Option A: Using the startup script**
```bash
./run.sh
```

**Option B: Direct command**
```bash
python3.11 -m streamlit run app.py
```

**Option C: Simple streamlit command** (if streamlit is in PATH)
```bash
streamlit run app.py
```

## Step 5: Open in Browser

The app will automatically open at:
```
http://localhost:8501
```

## 🎯 First Time Usage

1. **Age Verification**: Enter your age (13-19 required)
2. **Consent Screen**: Read and accept disclaimers
3. **Chat Interface**: Start chatting with TeenMind Companion!

## 🆘 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'google'"
**Solution**: Install dependencies
```bash
python3.11 -m pip install google-generativeai
```

### Error: "429 Quota exceeded"
**Solution**: You've hit the free tier rate limit (10 requests/min, 250k tokens/min)
- Wait a few minutes and try again
- Check your usage at: https://ai.dev/usage?tab=rate-limit
- Consider upgrading to paid tier for higher limits

### Error: "GEMINI_API_KEY not found"
**Solution**: Verify your `.env` file exists and contains:
```
GEMINI_API_KEY='your-actual-api-key'
```

### Port Already in Use
**Solution**: Streamlit is already running, or another app is using port 8501
```bash
# Kill existing streamlit process
pkill -f streamlit

# Or run on different port
streamlit run app.py --server.port 8502
```

### App Won't Load / Blank Screen
**Solution**:
1. Check browser console for errors (F12)
2. Clear browser cache
3. Try incognito/private mode
4. Verify all dependencies installed correctly

## 📊 Monitoring Usage

### Free Tier Limits (Late 2025)
- **Rate**: 10 requests/minute
- **Tokens**: 250k tokens/minute
- **Daily**: ~20-250 requests/day (varies)

### Check Current Usage
- Dashboard: https://ai.dev/usage
- Rate limits: https://ai.google.dev/gemini-api/docs/rate-limits

## 🔒 Privacy & Safety

### What's Stored:
- ✅ Session data (in memory, cleared on exit)
- ✅ Age and name (session only)

### What's NOT Stored:
- ❌ Chat conversations
- ❌ Personal identifiable information (PII)
- ❌ Crisis disclosures

### Important:
- Free tier data may improve Google's models (disclosed to users)
- For HIPAA compliance, use Vertex AI with BAA
- This is a personal project—not for clinical use

## 🎨 Customization

### Change Theme Colors
Edit `config.py`:
```python
THEME = {
    "primary_color": "#00ff88",  # Neon green
    "secondary_color": "#ff00ff",  # Magenta
    # ... customize colors
}
```

### Adjust Session Time
Edit `config.py`:
```python
MAX_SESSION_TIME = 900  # 15 minutes (in seconds)
```

### Modify Crisis Keywords
Edit `config.py` → `CRISIS_KEYWORDS` dictionary

### Update System Prompt
Edit `prompts.py` → `SYSTEM_INSTRUCTION`

## 📱 Next Steps

Once Phase 1 (text chat) is working:
- **Phase 2**: Turn-based voice mode (audio recording → STT → TTS)
- **Phase 3**: Real-time voice (WebRTC + Gemini Live)
- **Phase 4**: Mood tracker and coping strategies library
- **Phase 5**: Deployment to Streamlit Cloud

## 🤝 Need Help?

### For Technical Issues:
1. Check logs in terminal where Streamlit is running
2. Review error messages in browser console (F12)
3. Verify `.env` file and API key validity

### For Mental Health Crisis:
- **Call/Text 988** - Suicide & Crisis Lifeline
- **Text HOME to 741741** - Crisis Text Line
- **1-866-488-7386** - Trevor Project (LGBTQ+ youth)

---

**Remember: This is an AI companion for coping tips, NOT a replacement for professional mental health care.** 💚

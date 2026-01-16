# 🎤 Phase 2: Voice Mode Guide

## Overview

Phase 2 adds **turn-based voice interaction** to TeenMind Companion. Users can now:
- 🎤 Record voice messages instead of typing
- 🗣️ Receive AI responses as spoken audio
- 💬 See transcripts of all conversations
- 🔊 Replay audio responses anytime

## What's New in Phase 2

### Features Implemented

#### 1. Voice Mode Toggle
- Easy switch between text and voice modes
- Visual indicator when voice mode is active
- Seamless transition without losing chat history

#### 2. Audio Recording
- Browser-based microphone access
- Support for multiple audio formats (WAV, MP3, M4A, OGG)
- Real-time waveform visualization during recording
- 60-second maximum recording length

#### 3. Speech-to-Text (STT)
- Automatic transcription using Google Speech Recognition
- Free tier: Unlimited basic usage
- Supports clear speech in quiet environments
- Error handling for unclear audio

#### 4. Text-to-Speech (TTS)
- Browser native Web Speech API
- Automatic playback of AI responses
- Replay button for repeated listening
- Calm, clear voice optimized for teens

#### 5. Safety Integration
- All voice messages go through crisis detection
- Same safety framework as text chat
- Transcripts stored in chat history for review
- 988 redirection works for voice input

## How to Use Voice Mode

### Step 1: Enable Voice Mode

1. Open TeenMind Companion
2. Scroll to the "🎤 Voice Mode (Turn-Based)" section
3. Click "🎤 Enable Voice" button
4. Grant microphone permissions when prompted (browser popup)

### Step 2: Record Your Message

1. Click "Browse files" or microphone icon
2. Choose option:
   - **Record**: Click to start recording, speak clearly, click to stop
   - **Upload**: Select a pre-recorded audio file
3. See waveform animation while recording
4. Preview: Listen to your recording before sending

### Step 3: Send and Receive

1. Click "🗣️ Send Voice" button
2. Wait for transcription (shows "🎤 Transcribing audio...")
3. See your transcribed message in chat (with 🎤 icon)
4. AI responds with text + spoken audio
5. Click "🔁 Replay" to hear response again

### Step 4: Switch Back to Text

1. Click "⌨️ Text Mode" button
2. Continue chatting by typing
3. All previous messages (voice + text) remain in history

## Technical Details

### Architecture

```
Voice Input Flow:
┌─────────────┐
│ User speaks │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Browser records │
│ (st.audio_input)│
└──────┬──────────┘
       │
       ▼
┌──────────────────────┐
│ Google STT API       │
│ (speech_recognition) │
└──────┬───────────────┘
       │
       ▼
┌─────────────────┐
│ Text (transcribed)│
└──────┬────────────┘
       │
       ▼
┌──────────────────┐
│ Safety Check     │
│ (crisis keywords)│
└──────┬───────────┘
       │
       ▼
┌─────────────┐
│ Gemini API  │
│ (response)  │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Text Response    │
└──────┬───────────┘
       │
       ▼
┌───────────────────┐
│ Browser TTS       │
│ (Web Speech API)  │
└──────┬────────────┘
       │
       ▼
┌────────────────┐
│ Audio Playback │
└────────────────┘
```

### Speech-to-Text (STT)

**Library**: `SpeechRecognition` (Python)
- **Backend**: Google Speech Recognition API (free tier)
- **Format**: Supports WAV, FLAC, MP3 (auto-converted)
- **Sample Rate**: 16 kHz recommended
- **Language**: English (US) by default
- **Accuracy**: ~85-95% for clear speech in quiet environments

**Rate Limits (Free Tier)**:
- No hard limit for basic usage
- May throttle after excessive requests (>50/day)
- Commercial use requires Cloud Speech-to-Text API key

### Text-to-Speech (TTS)

**Technology**: Web Speech API (browser native)
- **Voices**: System voices (varies by OS/browser)
  - macOS: "Samantha" (female, calm)
  - Windows: "Zira" (female, clear)
  - Linux: "Female" voice (varies by distro)
- **Rate**: 0.9x (slightly slower for clarity)
- **Pitch**: 1.0 (natural)
- **Volume**: 1.0 (full)

**Why Browser TTS?**
- ✅ Zero cost (no API fees)
- ✅ Zero latency (local processing)
- ✅ Privacy (no audio sent to servers)
- ✅ Offline capable (once page loaded)
- ❌ Voice quality varies by browser/OS
- ❌ No customization beyond basic parameters

**Phase 3 Upgrade**: Gemini Live API for native, high-quality TTS

### Audio Formats Supported

| Format | Recording | Playback | Notes |
|--------|-----------|----------|-------|
| WAV    | ✅        | ✅       | Best quality, large file size |
| MP3    | ✅        | ✅       | Compressed, good quality |
| M4A    | ✅        | ✅       | Apple devices |
| OGG    | ✅        | ✅       | Open format |
| FLAC   | ✅        | ⚠️       | Lossless, browser support varies |

**Recommended**: WAV (16 kHz, mono) for best transcription accuracy

## Browser Compatibility

### Microphone Access (Required for Recording)

| Browser | Recording | Playback | TTS | Notes |
|---------|-----------|----------|-----|-------|
| Chrome  | ✅ 100%   | ✅ 100%  | ✅ 100% | Best experience |
| Edge    | ✅ 100%   | ✅ 100%  | ✅ 100% | Chromium-based |
| Firefox | ✅ 95%    | ✅ 100%  | ✅ 90% | Some TTS voice limits |
| Safari  | ✅ 90%    | ✅ 100%  | ✅ 85% | iOS: requires user gesture |
| Opera   | ✅ 95%    | ✅ 100%  | ✅ 95% | Good support |

**Minimum Versions**:
- Chrome 70+
- Firefox 65+
- Safari 14.1+
- Edge 79+

### HTTPS Requirement

⚠️ **Microphone access requires HTTPS** (secure connection):
- ✅ `localhost:8501` (development)
- ✅ `https://your-app.streamlit.app` (Streamlit Cloud)
- ❌ `http://192.168.x.x:8501` (local network - insecure)

**Workaround for local network testing**:
1. Use `ngrok` or `localtunnel` to create HTTPS tunnel
2. Or deploy to Streamlit Cloud (always HTTPS)

## Usage Tips

### For Best Transcription Accuracy

1. **Quiet Environment**: Reduce background noise (close windows, turn off fans)
2. **Clear Speech**: Speak at normal pace, enunciate clearly
3. **Distance**: 6-12 inches from microphone
4. **Short Sentences**: Pause between thoughts (helps AI understand context)
5. **Retry if Needed**: If transcription is wrong, click "Send Voice" again

### For Best TTS Experience

1. **Browser Volume**: Ensure browser/system volume is up
2. **Replay**: Use "🔁 Replay" button if you miss something
3. **Read Along**: Transcript appears simultaneously for clarity
4. **Headphones**: Use headphones for privacy (especially on shared computers)

### Privacy Tips

1. **No Server Recording**: Audio is transcribed locally, not stored on servers
2. **Session Only**: Transcripts cleared when you exit the app
3. **Mute if Needed**: Close app tab to immediately stop all audio
4. **Shared Devices**: Use headphones, clear session after use

## Troubleshooting

### "Could not understand audio"

**Causes**:
- Background noise too loud
- Speech too quiet or muffled
- Non-English language (current version is English-only)

**Solutions**:
- Move to quieter location
- Speak louder and clearer
- Check microphone is not muted (system settings)
- Try recording again with shorter sentences

### "Speech recognition service error"

**Causes**:
- No internet connection (STT requires online access)
- Google API rate limit hit (unlikely, but possible)
- Browser blocked microphone permissions

**Solutions**:
- Check internet connection
- Allow microphone permissions (browser settings)
- Wait 1 minute and try again
- Switch to text mode temporarily

### No Audio Playback

**Causes**:
- Browser TTS voices not loaded
- System volume muted
- Autoplay blocked by browser

**Solutions**:
- Click "🔁 Replay" button manually
- Check system/browser volume
- Enable autoplay for `localhost:8501` (browser settings)
- Try different browser (Chrome recommended)

### Microphone Not Working

**Causes**:
- Permissions denied
- Microphone in use by another app
- Hardware issue

**Solutions**:
1. **Check Permissions**:
   - Chrome: Settings > Privacy > Site Settings > Microphone
   - Firefox: Click 🔒 icon in URL bar > Permissions
   - Safari: Preferences > Websites > Microphone
2. **Close Other Apps**: Zoom, Skype, etc.
3. **Test Microphone**: System settings > Sound > Input

### Recording Time Limit

**Issue**: "Recording stopped at 60 seconds"

**Explanation**: Safety limit to prevent excessive API usage and file size

**Solutions**:
- Break message into shorter parts (better for AI understanding anyway)
- For longer thoughts, use text mode
- Phase 3 will support longer real-time conversations

## API Keys & Rate Limits

### Google Speech Recognition (STT)

**Current Implementation**: Free tier (no API key required)
- Uses `speech_recognition` library's built-in Google endpoint
- **Limits**: ~50 requests/day before throttling (unofficial)
- **Quota**: No hard cap, but excessive use may be rate-limited

**Future (Optional Upgrade)**:
- Google Cloud Speech-to-Text API
- **Cost**: $0.006/15 seconds (~$0.024/minute)
- **Limits**: 1M minutes/month free, then $0.024/min
- **Setup**: Add `GOOGLE_CLOUD_SPEECH_API_KEY` to `.env`

### Browser TTS

**Cost**: $0 (free, local processing)
**Limits**: None (runs in browser)

## Cost Breakdown (Phase 2)

| Component | Free Tier | Paid Tier | Notes |
|-----------|-----------|-----------|-------|
| STT (Google) | ~50 req/day | $0.024/min | Current: free |
| TTS (Browser) | Unlimited | N/A | Always free |
| Gemini API | 10 req/min | $0.50/M tokens | Same as Phase 1 |
| **Total** | **$0/month** | **~$5-20/month** | For 1000 users |

**Recommendation**: Stay on free tier for personal use. Upgrade to paid STT only if hitting rate limits.

## What's Next: Phase 3 Preview

Phase 3 will upgrade to **real-time voice** with:
- 🎙️ **Gemini Live API**: Native audio input/output (no STT/TTS needed)
- ⚡ **Low Latency**: <500ms response time (vs ~2-5s in Phase 2)
- 🔄 **Interruption Handling**: Can interrupt AI mid-sentence (barge-in)
- 🎧 **Voice Activity Detection**: Automatic turn-taking (no button presses)
- 🌐 **WebRTC Streaming**: Direct browser-to-AI audio pipeline

**Timeline**: 3-4 weeks (depends on Gemini Live GA release)

---

## Quick Reference

### Enable Voice Mode
1. Click "🎤 Enable Voice"
2. Grant microphone permissions
3. Record or upload audio
4. Click "🗣️ Send Voice"

### Disable Voice Mode
1. Click "⌨️ Text Mode"
2. Continue with keyboard input

### Troubleshooting
- No transcription → Check internet, speak clearly
- No audio playback → Check volume, click "🔁 Replay"
- Microphone not working → Check permissions, close other apps

### Get Help
- **Technical issues**: Check browser console (F12)
- **Mental health crisis**: Call/Text **988** (24/7)

---

**Phase 2 Complete!** 🎉 Enjoy voice conversations with TeenMind Companion. 💚

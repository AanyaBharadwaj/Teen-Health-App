"""Test script to verify Gemini API connection."""

import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure API
genai.configure(api_key=GEMINI_API_KEY)

print("🧪 Testing Gemini API Connection...")
print(f"API Key (first 10 chars): {GEMINI_API_KEY[:10]}...")

# List available models
print("\n📋 Available Models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  ✓ {model.name}")

# Test simple generation
print("\n🔬 Testing text generation...")
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Say 'Hello! API is working!' in a friendly way.")
    print(f"✅ Response: {response.text}")
    print("\n✨ All tests passed! Ready to run the app.")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\n⚠️  If you see a quota error, wait a few minutes and try again.")
    print("    Free tier has rate limits: 10 requests/minute, 250k tokens/minute.")

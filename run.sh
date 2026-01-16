#!/bin/bash

echo "🧠✨ Starting TeenMind Companion..."
echo ""
echo "Prerequisites Check:"
echo "  ✓ Python 3.11 installed"
echo "  ✓ Dependencies installed (run 'pip install -r requirements.txt' if not)"
echo "  ✓ .env file with GEMINI_API_KEY configured"
echo ""
echo "🚀 Launching Streamlit app..."
echo ""

python3.11 -m streamlit run app.py

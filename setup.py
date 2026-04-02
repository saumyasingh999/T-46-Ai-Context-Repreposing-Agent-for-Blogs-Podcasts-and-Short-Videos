"""
Run this once before starting the app:
    python setup.py
"""
import os
import sys

print("\n🔧  ContentAI — First-time Setup\n" + "─" * 36)

# 1. NLTK downloads
print("\n[1/3] Downloading NLTK data...")
import nltk
for pkg in ['punkt', 'punkt_tab', 'stopwords', 'averaged_perceptron_tagger']:
    try:
        nltk.download(pkg, quiet=True)
        print(f"     ✅  {pkg}")
    except Exception as e:
        print(f"     ⚠️   {pkg} failed: {e}")

# 2. Create directories
print("\n[2/3] Creating project directories...")
dirs = ['uploads', 'outputs', 'database', 'models']
for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"     ✅  {d}/")

# 3. Init database
print("\n[3/3] Initialising SQLite database...")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from database.db import init_db
    init_db()
    print("     ✅  database/content.db created")
except Exception as e:
    print(f"     ⚠️   DB init failed: {e}")

print("\n" + "─" * 36)
print("✨  Setup complete! Run the app with:\n")
print("    python app.py\n")
print("    Then open: http://127.0.0.1:5000\n")
print("─" * 36)
print("\n📌  Optional: Install Vosk for podcast transcription")
print("    pip install vosk")
print("    Download model → https://alphacephei.com/vosk/models")
print("    Use: vosk-model-small-en-us-0.15  (40MB)")
print("    Place at: models/vosk-model-small-en-us/\n")

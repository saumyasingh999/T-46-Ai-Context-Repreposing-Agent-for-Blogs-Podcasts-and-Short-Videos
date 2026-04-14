<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6a0dad,50:9b30ff,100:c084fc&height=200&section=header&text=AI%20Content%20Repurposer&fontSize=48&fontColor=ffffff&fontAlignY=38&desc=Create%20Once%20%E2%86%92%20Share%20Everywhere&descAlignY=58&descSize=18&animation=fadeIn" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=3000&pause=800&color=A855F7&center=true&vCenter=true&multiline=true&width=700&height=80&lines=Convert+Blogs+%7C+Podcasts+%7C+YouTube+Videos;Into+Scripts+%7C+Social+Posts+%7C+Threads+%7C+More;100%25+Offline+%C2%B7+No+API+Key+%C2%B7+No+GPU+Needed" alt="Typing Animation" />

<br/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-NLP-4CAF50?style=for-the-badge&logo=python&logoColor=white)
![Whisper](https://img.shields.io/badge/Whisper-Speech--to--Text-FF6B35?style=for-the-badge&logo=openai&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-TF--IDF-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![University](https://img.shields.io/badge/GLA-University-6A0DAD?style=for-the-badge)

</div>

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## 🌟 What is This Project?

**AI Content Repurposer** converts **blogs, podcasts, and YouTube videos** into ready-to-publish content for every platform — in under 2 minutes. No API key. No GPU. Runs fully offline on any laptop.

```
Blog / Podcast / YouTube URL
            ↓
   AI Content Repurposer
            ↓
  📝 Summary        🎬 Video Script
  ✨ Highlights     📱 Social Posts
  🧵 Twitter Thread 💼 LinkedIn Post
  📌 SEO Titles     #️⃣  Hashtags
  🔑 Keywords       💡 Reel Concept
```

> 

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## ❗ Problem & Solution

**Problem:** Converting one blog into social content takes 2–3 hours manually.

**Solution:** One input → 11 outputs → under 2 minutes. Automatically.

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## 🚀 Features

<div align="center">

| Feature | Description |
|:---:|:---|
| 📝 **Blog Input** | Paste text or a URL — content fetched automatically |
| 🎙️ **Podcast Upload** | Upload audio (WAV/MP3/OGG/M4A) — Whisper transcribes it |
| 📺 **YouTube Video** | Paste any YouTube link — captions or audio extracted |
| 📄 **Summary** | Top 4 most important sentences via TF-IDF |
| ✨ **Highlights** | Top 5 key sentences — ideal for social media quotes |
| 🎬 **Video Script** | 30–60 sec script with Hook → Context → CTA |
| 📱 **Social Posts** | Platform-specific posts for Twitter, Instagram, LinkedIn |
| 🧵 **Twitter Thread** | Auto-numbered tweets with hook + CTA |
| 💼 **LinkedIn Post** | Long-form post with bullet points, insight, hashtags |
| 📌 **SEO Titles** | 10 title variations — Listicle, How-To, Question, SEO |
| #️⃣ **Hashtags** | 20 Instagram · 5 Twitter · 5 LinkedIn · 15 YouTube · 8 TikTok |
| 🎨 **Tone Control** | Professional / Casual / Educational |
| 🔧 **Quick Tools** | Run any single tool independently |
| 📜 **History** | Last 20 results saved in SQLite |

</div>

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## 🏗️ System Architecture

```
┌──────────────────────────────────────────┐
│   Jinja2 Templates · CSS · Vanilla JS    │
│   Dark Theme · Tabs · Copy Buttons       │
└─────────────────┬────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│         Flask Backend (app.py)           │
│  /blog /podcast /youtube /tools /result  │
└──────┬──────────────┬────────────┬───────┘
       ↓              ↓            ↓
  NLP Layer     Speech Layer    models/
  text_cleaner  transcriber.py  summarizer
  keyword_ext   yt-dlp          script_gen
  NLTK          faster-whisper  social_posts
  scikit-learn  FFmpeg          tone_ctrl ...
                  ↓
           SQLite (content.db)
```

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## 🧠 AI Pipeline

11 operations run automatically on every input:

```
INPUT TEXT
  ├──→ [01] chunk_and_summarize()       → 4-sentence Summary
  ├──→ [02] extract_highlights()        → 5 Key Sentences
  ├──→ [03] extract_keywords()          → 8 Keywords
  ├──→ [04] apply_tone()                → Tone-Adjusted Text
  ├──→ [05] generate_script()           → 30–60s Video Script
  ├──→ [06] generate_social_posts()     → Twitter + Instagram + LinkedIn
  ├──→ [07] generate_reel_idea()        → Reel Concept
  ├──→ [08] generate_hashtags()         → 20 Hashtags
  ├──→ [09] generate_titles()           → 10 SEO Titles
  ├──→ [10] split_into_thread()         → Twitter Thread
  └──→ [11] convert_blog_to_linkedin()  → LinkedIn Long Post
              ↓
     Saved to SQLite → Results Page ✅
```

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## 📺 YouTube → Text Flow

```
YouTube URL → Extract Video ID
      ↓
Try captions (yt-dlp) ──────────→ Text ✅  (< 3 sec)
      ↓ if unavailable
Download audio (64kbps MP3 · max 10 min)
      ↓
FFmpeg → 16kHz mono WAV
      ↓
faster-whisper (medium · CPU · VAD filter)
      ↓
Text ✅  (30–90 sec)
```

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## 🔬 TF-IDF Summarization Steps

```
Raw Text
  → clean_text()       Remove HTML, URLs, extra spaces
  → sent_tokenize()    Split into sentences (NLTK)
  → TfidfVectorizer    Score each sentence mathematically
  → Position Boost     First sentence ×1.5 · Last sentence ×1.2
  → Pick Top 4         Highest-scoring sentences selected
  → Original Order     Preserve natural reading flow
  → Summary ✅
```

> For texts over 500 words — chunked into 500-word blocks → each summarized → merged → final summary.

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## 🛠️ Tech Stack

<div align="center">

**Backend**
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

**NLP & AI**
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-4CAF50?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=python&logoColor=white)

**Speech & Audio**
![Whisper](https://img.shields.io/badge/faster--whisper-FF6B35?style=for-the-badge&logo=openai&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)

**Web & Scraping**
![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-2CA5E0?style=for-the-badge&logo=python&logoColor=white)

</div>

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## 📁 Project Structure

```
ai-content-repurposer/
│
├── app.py                     ← Flask routes & pipeline
├── config.py                  ← Paths, limits, secret key
├── requirements.txt           ← Dependencies
├── run.bat                    ← Windows one-click launcher
│
├── models/                    ← Content generation modules
│   ├── summarizer.py
│   ├── highlight_extractor.py
│   ├── script_generator.py
│   ├── social_post_generator.py
│   ├── tone_controller.py
│   ├── hashtag_generator.py
│   ├── title_generator.py
│   ├── twitter_thread_splitter.py
│   └── blog_to_linkedin.py
│
├── nlp/                       ← Text preprocessing
│   ├── text_cleaner.py
│   └── keyword_extractor.py
│
├── speech/                    ← Audio & YouTube
│   └── transcriber.py
│
├── database/                  ← SQLite storage
│   ├── db.py
│   └── content.db
│
├── templates/                 ← HTML pages (9 templates)
└── uploads/                   ← Cached audio files
```

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## ⚙️ Installation

**Prerequisites:** Python 3.11+ · FFmpeg · Node.js

```bash
# Clone
git clone https://github.com/your-username/ai-content-repurposer.git
cd ai-content-repurposer

# Install
pip install -r requirements.txt

# Setup & Run
python setup.py
python app.py
```

Open → `http://127.0.0.1:5000`

> Windows users: double-click `run.bat`

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## 🎨 Tone Options

| Tone | Style | Example |
|---|---|---|
| 💼 Professional | Formal, corporate | use → utilize |
| 🔥 Casual | Friendly, relatable | significant → big |
| 📚 Educational | Teaching style | Adds "This means that..." |

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## ⚠️ Limitations

- Best with clear, well-structured English content
- TF-IDF is extractive — selects sentences, doesn't generate new ones
- YouTube audio capped at **10 minutes**
- No user login system

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## 🚀 Future Improvements

- [ ] BART / Pegasus for abstractive summarization
- [ ] GPU support for Whisper (10–20× faster)
- [ ] Local LLM integration (Ollama / Llama 3)
- [ ] PDF and DOCX input support
- [ ] Social media auto-posting
- [ ] User authentication
- [ ] Docker deployment

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## 📚 References

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — Optimized Whisper inference on CPU
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube audio and caption downloader
- [NLTK Documentation](https://www.nltk.org/) — Natural language toolkit
- [scikit-learn TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) — TF-IDF implementation
- [Flask Documentation](https://flask.palletsprojects.com/) — Web framework
- [FFmpeg](https://ffmpeg.org/) — Audio conversion
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) — HTML parsing for blog URLs
- [spaCy](https://spacy.io/) — Industrial-strength NLP library
- [OpenAI Whisper Research Paper](https://arxiv.org/abs/2212.04356) — Robust Speech Recognition via Large-Scale Weak Supervision

---

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">

## 👥 Team

<div align="center">

| Member | Role |
|:---:|:---:|
| **Shailesh Gole** | 👨‍💻 Team Lead & Backend Developer |
| **Saumya Singh** | 🎨 Frontend Developer & NLP Support |
| **Urvashi Agrawal** | 🧪 Testing & Documentation |

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:c084fc,50:9b30ff,100:6a0dad&height=120&section=footer&animation=fadeIn" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=14&duration=3000&pause=1000&color=A855F7&center=true&vCenter=true&width=500&lines=Built+with+%E2%9D%A4%EF%B8%8F+My+Team;Create+Once+%E2%86%92+Share+Everywhere;100%25+Offline+%C2%B7+No+API+%C2%B7+No+GPU" alt="footer typing"/>

 **Thank You**

</div>

<div align="center">

<!-- Animated Header Banner -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:6C63FF,100:00D4FF&height=200&section=header&text=AI%20Content%20Repurposer&fontSize=48&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Convert%20Blogs%20%26%20Podcasts%20→%20Viral%20Short-Form%20Content&descAlignY=60&descSize=18"/>

<!-- Animated Typing Effect -->
<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=6C63FF&center=true&vCenter=true&random=false&width=700&lines=🎬+Generate+Short+Video+Scripts+in+Seconds;📱+Auto-Create+Social+Media+Posts;🎙️+Transcribe+Podcasts+with+AI;✨+Extract+Key+Highlights+%26+Quotes;🚀+Create+Once+→+Share+Everywhere" alt="Typing SVG" />
</a>

<br/>

<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-NLP-orange?style=for-the-badge&logo=python&logoColor=white)
![Whisper](https://img.shields.io/badge/Whisper-Speech--to--Text-412991?style=for-the-badge&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-Academic-FF6B6B?style=for-the-badge)
![GLA University](https://img.shields.io/badge/GLA-University-4A90D9?style=for-the-badge&logo=academia&logoColor=white)

<br/>

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Workflow](#-workflow)
- [AI Technologies](#-ai-technologies)
- [Installation](#-installation)
- [Team](#-team)
- [Success Metrics](#-success-metrics)
- [Future Roadmap](#-future-roadmap)

---

## 🚀 Overview

<div align="center">

> **"Create Once → Share Everywhere"**
> 
> *The AI-powered agent that transforms your long-form content into viral short-form gold.*

</div>

**AI Content Repurposing Agent** is an intelligent system that automatically converts **blogs & podcasts** into platform-ready content — including short video scripts, social media captions, and key highlights — using **offline open-source AI models**.

Built as a **Mini Project at GLA University**, this tool empowers creators to multiply their reach without multiplying their effort.

---

## ❗ Problem Statement

```
Long-form content creators face a common struggle:
```

```
📝 Blog Post (2000 words)          🎙️ Podcast (45 minutes)
        │                                    │
        ▼                                    ▼
   Hours of manual work               Manual transcription
   to create social posts             + editing required
        │                                    │
        └──────────────┬─────────────────────┘
                       ▼
          ❌ Valuable content goes underutilized
          ❌ Multi-platform presence suffers
          ❌ Time wasted on repetitive editing
```

---

## 💡 Solution

```
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │   📄 Blog / 🎙️ Podcast                                  │
  │           │                                             │
  │           ▼                                             │
  │   ┌───────────────┐                                     │
  │   │  AI Processing │  ← NLTK + spaCy + TextRank        │
  │   └───────┬───────┘                                     │
  │           │                                             │
  │     ┌─────┼─────────────┐                               │
  │     ▼     ▼             ▼                               │
  │  🎬 Video  📱 Social   ⭐ Key                            │
  │  Script    Media Post  Highlights                        │
  │                                                         │
  │   ✅ Under 2 Minutes   ✅ 80% Usable  ✅ Any Tone        │
  └─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📝 Blog Processing
- ✅ Accept blog text or URL input
- ✅ Extract key information automatically
- ✅ Generate summaries and highlights
- ✅ Topic detection & keyword extraction

</td>
<td width="50%">

### 🎙️ Podcast Processing
- ✅ Upload podcast audio files
- ✅ Convert speech to text (Whisper/Vosk)
- ✅ Generate scripts and captions
- ✅ Extract key quotes automatically

</td>
</tr>
<tr>
<td width="50%">

### 🤖 AI Content Generation
- 🎬 Short video scripts (30–60 sec)
- 📱 Social media posts (Twitter/LinkedIn/Instagram)
- 💬 Platform-ready captions
- ⭐ Key highlights & quotes

</td>
<td width="50%">

### 🎨 Tone Customization
| Tone | Best For |
|------|----------|
| 🏢 Professional | LinkedIn, B2B |
| 📚 Educational | Tutorials, Courses |
| 😄 Casual | Instagram, TikTok |

</td>
</tr>
</table>

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                    React.js Frontend                        │
│          [Blog Input] [Audio Upload] [Tone Select]          │
└──────────────────────────┬──────────────────────────────────┘
                           │  REST API
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND API LAYER                         │
│                  Python / Node.js Server                    │
│         [Request Handler] [File Processor] [Router]         │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
┌─────────────────────┐         ┌───────────────────────┐
│  SPEECH PROCESSING  │         │    NLP PROCESSING     │
│                     │         │                       │
│  🎙️ Audio Input     │         │  📄 Text Input        │
│  Whisper / Vosk     │──text──▶│  NLTK + spaCy         │
│  Speech-to-Text     │         │  TextRank             │
└─────────────────────┘         │  Scikit-learn         │
                                └───────────┬───────────┘
                                            │
                                            ▼
                           ┌────────────────────────────┐
                           │  CONTENT REPURPOSING ENGINE │
                           │                            │
                           │  🎬 Video Script Generator │
                           │  📱 Social Post Generator  │
                           │  ⭐ Highlight Extractor    │
                           └──────────────┬─────────────┘
                                          │
                                          ▼
                             ┌────────────────────────┐
                             │       DATABASE          │
                             │   MongoDB / Local DB    │
                             └────────────────────────┘
```

---

## 💻 Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|-------|-----------|---------|
| 🎨 **Frontend** | React.js, HTML5, CSS3, JavaScript | User Interface |
| ⚙️ **Backend** | Python, Node.js, REST API | Server & Logic |
| 🧠 **NLP** | NLTK, spaCy, Scikit-learn | Text Analysis |
| 📝 **Summarization** | TextRank Algorithm | Content Ranking |
| 🎙️ **Speech-to-Text** | OpenAI Whisper, Vosk | Audio Processing |
| 🗄️ **Database** | MongoDB / Local Storage | Data Persistence |

</div>

---

## ⚙️ Workflow

```
  USER
   │
   ├──── Uploads Blog Text / URL ────────────────────┐
   │                                                 │
   └──── Uploads Podcast Audio ──► Speech-to-Text ──┘
                                                     │
                                                     ▼
                                         ┌───────────────────┐
                                         │   NLP Processing   │
                                         │ ─────────────────  │
                                         │ • Summarization    │
                                         │ • Keyword Extract  │
                                         │ • Topic Detection  │
                                         └─────────┬─────────┘
                                                   │
                             ┌─────────────────────┼──────────────────────┐
                             ▼                     ▼                      ▼
                    ┌────────────────┐  ┌─────────────────┐  ┌──────────────────┐
                    │  🎬 Video       │  │  📱 Social Media │  │  ⭐ Highlights   │
                    │  Script        │  │  Post            │  │  & Quotes        │
                    │  (30-60 sec)   │  │  (Platform-ready)│  │  (Key moments)   │
                    └────────┬───────┘  └────────┬────────┘  └──────┬───────────┘
                             │                   │                   │
                             └─────────────────┬─┘                   │
                                               └──────────┬──────────┘
                                                          ▼
                                               ┌──────────────────────┐
                                               │    📋 Results Panel  │
                                               │  [Copy] [Download]   │
                                               └──────────────────────┘
```

---

## 🧠 AI Technologies

<div align="center">

| 🔬 Technology | 🎯 Purpose | ⚡ Role |
|--------------|-----------|--------|
| **NLTK** | Natural Language Toolkit | Tokenization, POS tagging, text preprocessing |
| **spaCy** | Industrial NLP | Named entity recognition, dependency parsing |
| **Scikit-learn** | ML Library | TF-IDF vectorization, text ranking |
| **TextRank** | Graph-based Algorithm | Extractive summarization |
| **Whisper** | OpenAI Speech Model | High-accuracy audio transcription |
| **Vosk** | Offline Speech Recognizer | Lightweight, offline STT fallback |

</div>

---

## 🛠 Installation

### Prerequisites

```bash
# Python 3.9+
python --version

# Node.js 16+
node --version

# MongoDB (optional)
mongod --version
```

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-content-repurposer.git
cd ai-content-repurposer
```

### Step 2 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Setup the Project

```bash
python setup.py
```

### Step 4 — Run the Backend

```bash
python app.py
```

### Step 5 — Start the Frontend

```bash
cd frontend
npm install
npm start
```

### Step 6 — Open in Browser

```
http://localhost:3000
```

---

## 📊 Success Metrics

<div align="center">

| 🎯 Objective | 📏 KPI | 🏆 Target |
|-------------|--------|----------|
| Speed | Content generation time | **< 2 minutes** |
| Usability | User satisfaction rating | **≥ 4 / 5 stars** |
| Quality | Usable output rate | **≥ 80%** |

</div>

---

## 👥 Team

<div align="center">

| 👤 Name | 🎖️ Role | 💼 Responsibilities |
|---------|---------|-------------------|
| **Shailesh Gole** | 🧑‍💻 Team Lead & Backend Developer | Architecture, API, AI integration |
| **Saumya Singh** | 🎨 Frontend Developer & NLP Support | React UI, NLP pipeline support |
| **Urvashi Agrawal** | 🧪 Testing & Documentation | QA, README, project docs |

> 🏫 Developed at **GLA University** as an academic Mini Project

</div>

---

## ⚠️ Known Limitations

```
⚠️  Works best with clear English content
⚠️  AI output may need minor human editing
⚠️  Large audio files may increase processing time
⚠️  Requires stable Python environment for NLP models
```

---

## 🚀 Future Roadmap

```
  Version 1.0 (Current) ──────────────────────────────────────┐
  ✅ Blog text input                                           │
  ✅ Podcast audio upload                                      │
  ✅ Script + post + highlights generation                     │
  ✅ Tone selection                                            │
                                                              │
  Version 2.0 (Planned) ──────────────────────────────────────┤
  🔲 Multi-language support                                    │
  🔲 Social media auto-posting                                 │
  🔲 AI-generated highlight videos                            │
                                                              │
  Version 3.0 (Vision) ───────────────────────────────────────┘
  🔲 Automatic video generation
  🔲 Analytics dashboard
  🔲 Team collaboration features
  🔲 API for third-party integrations
```

---

## 🔒 Security

- ✅ File upload type & size validation
- ✅ Secure environment variables (`.env`)
- ✅ Protected user data handling
- ✅ HTTPS communication support

---

## 📚 References

- [OpenAI Whisper](https://github.com/openai/whisper) — Speech Recognition
- [NLTK Documentation](https://www.nltk.org/) — Natural Language Toolkit
- [spaCy NLP Library](https://spacy.io/) — Industrial-strength NLP
- [TextRank Paper](https://aclanthology.org/W04-3252/) — Graph-based Summarization

---

<div align="center">

<!-- Footer Wave -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:00D4FF,100:6C63FF&height=120&section=footer"/>

**⭐ Star this repo if you found it useful!**

Made with ❤️ by Team at GLA University

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=ai-content-repurposer)

</div>

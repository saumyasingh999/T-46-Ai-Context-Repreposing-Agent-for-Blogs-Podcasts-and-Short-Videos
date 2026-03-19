# AI Context Repurposing Agent

Turn any YouTube video, blog post, or audio file into blog articles, LinkedIn posts,
Twitter threads, Instagram captions, and short video scripts — powered by OpenAI.

## Folder Structure

```
ai-context-agent/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── models.py                # Pydantic request/response models
│   ├── requirements.txt
│   ├── .env.example
│   ├── routers/
│   │   ├── ingest.py            # /ingest endpoint (YouTube, audio, blog)
│   │   └── generate.py          # /generate endpoint (AI content generation)
│   └── services/
│       ├── youtube.py           # YouTube transcript extraction
│       ├── audio.py             # Whisper audio transcription
│       ├── preprocessor.py      # Text cleaning
│       └── ai_generator.py      # OpenAI content generation
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── api.js               # Axios API calls
        ├── index.css
        └── components/
            ├── InputForm.jsx    # YouTube / blog / audio input tabs
            └── OutputTabs.jsx   # Tabbed output viewer with copy button
```

## Setup

### 1. Backend

```bash
cd ai-context-agent/backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
cp .env.example .env
# Edit .env and add your key: OPENAI_API_KEY=sk-...

# Run the server
uvicorn main:app --reload --port 8000
```

> Whisper requires ffmpeg. Install it via:
> - macOS: `brew install ffmpeg`
> - Ubuntu: `sudo apt install ffmpeg`
> - Windows: https://ffmpeg.org/download.html

### 2. Frontend

```bash
cd ai-context-agent/frontend

npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## API Endpoints

| Method | Path        | Description                              |
|--------|-------------|------------------------------------------|
| POST   | /ingest/    | Extract & clean text from any input type |
| POST   | /generate/  | Generate all 5 content formats via AI    |
| GET    | /health     | Health check                             |

## Environment Variables

| Variable        | Description              |
|-----------------|--------------------------|
| OPENAI_API_KEY  | Your OpenAI API key      |

## Adding New Output Formats

1. Add a new prompt to `PROMPTS` dict in `backend/services/ai_generator.py`
2. Add the field to `GeneratedContent` in `backend/models.py`
3. Add a new tab entry to the `TABS` array in `frontend/src/components/OutputTabs.jsx`

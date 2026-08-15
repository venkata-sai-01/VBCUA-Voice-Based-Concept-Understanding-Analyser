# VBCUA — Voice-Based Concept Understanding Analyser

A full-stack final-year project implementing the supplied VBCUA architecture.

## Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Database:** SQLite + SQLAlchemy
- **Speech recognition:** OpenAI Whisper
- **Semantic understanding:** Sentence-BERT
- **Audio analysis:** Librosa + SoundFile
- **Reports:** ReportLab
- **Charts:** Plotly

## Features

- Reference concept management
- Audio upload
- Microphone recording when supported by Streamlit
- Speech-to-text
- Semantic similarity
- Filler-word analysis
- Pause ratio
- RMS energy
- Speaking rate
- Explainable score
- Automatic recommendations
- Evaluation history
- PDF reports
- REST API
- Health endpoint
- SQLite persistence
- Automated tests

## Run

### 1. Create environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install

```bash
pip install -r requirements.txt
```

### 3. Start backend

```bash
python backend/run.py
```

Backend:
`http://127.0.0.1:8000`

Swagger:
`http://127.0.0.1:8000/docs`

### 4. Start frontend

Open a second terminal:

```bash
streamlit run frontend/main.py
```

Frontend:
`http://localhost:8501`

## API

- `GET /health`
- `GET /api/concepts`
- `POST /api/concepts`
- `GET /api/concepts/{id}`
- `POST /api/analyze`
- `GET /api/evaluations`
- `GET /api/evaluations/{id}`
- `GET /api/reports/{id}`

## First run

Whisper and Sentence-BERT model weights are downloaded on first analysis. For low-end hardware use:

```env
WHISPER_MODEL=tiny
```

## Architecture

```text
                   ┌──────────────────────┐
                   │   Streamlit Frontend │
                   │ upload / microphone  │
                   │ dashboard / reports  │
                   └──────────┬───────────┘
                              │ REST
                              ▼
                   ┌──────────────────────┐
                   │     FastAPI Backend  │
                   ├──────────────────────┤
                   │ Analysis Orchestrator│
                   └──────────┬───────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       ▼                      ▼                      ▼
   Whisper              Sentence-BERT           Librosa
 Speech-to-Text        Semantic Similarity    Audio Features
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              ▼
                     Scoring + Feedback
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
             SQLite DB                 ReportLab
          concepts/history             PDF report
```

## Academic positioning

This is an educational prototype. The score is a configurable learning-feedback indicator and is not a certified psychological, medical or professional assessment.

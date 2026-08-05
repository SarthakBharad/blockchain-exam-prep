# Blockchain Exam Prep

A Streamlit quiz app for revising blockchain course material. Questions live in a JSON file, so the bank can be extended without touching the app code.

## Features

- **104 questions** across three formats: single choice, multiple select, and fill-in-the-blank
- Forgiving answer matching for blanks — case, punctuation, and whitespace are ignored, and alternative spellings are accepted
- Running score with instant feedback; the correct answer is shown on a wrong submission
- Jump to any question by number
- Bookmark questions and review them from the final screen
- Restart without reloading the page

## Requirements

- Python 3.8 or newer
- Streamlit (installed via `requirements.txt`)

## Setup

```powershell
git clone https://github.com/SarthakBharad/blockchain-exam-prep.git
cd blockchain-exam-prep

python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate       # macOS / Linux

python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation with an execution-policy error, run this once and retry:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Running

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`. Run it from the repository root — `blockchain.json` is loaded by relative path. Stop the server with `Ctrl+C`; closing the terminal window leaves it running in the background.

## Question format

`blockchain.json` is a flat list of question objects. Every object has `question`, `options`, `correct`, and `type`.

**Single choice** — `correct` is one of the strings in `options`:

```json
{
  "question": "What is true about the concept of peer-to-peer networks?",
  "options": ["Option A", "Option B", "Option C"],
  "correct": "Option A",
  "type": "single"
}
```

**Multiple select** — `correct` is a list; order does not matter when grading:

```json
{
  "question": "What are advantages of peer-to-peer networks?",
  "options": ["Single point of failure", "Mutability", "Velocity", "Transparency"],
  "correct": ["Velocity", "Transparency"],
  "type": "multi"
}
```

**Fill in the blank** — the expected answer lives in `answer`; `options` and `correct` stay empty. Separate acceptable variants with `/`:

```json
{
  "question": "What means SPOF in the context of network architectures? Max. five words!",
  "options": [],
  "correct": [],
  "type": "blank",
  "answer": "Single point of failure/Single-point-of-failure"
}
```

## Project structure

```
├── app.py             # Streamlit UI and grading logic
├── blockchain.json    # Question bank
├── requirements.txt   # Dependencies
└── .gitignore
```

## Notes

- Questions are cached with `@st.cache_data`. After editing `blockchain.json`, clear the cache from the Streamlit menu or restart the app to pick up changes.
- The virtual environment is not tracked. Its launcher scripts hardcode absolute paths, so it breaks if the project folder is moved or renamed — recreate it rather than trying to relocate it.
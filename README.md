# Blockchain Exam Prep

A small Streamlit quiz app for revising blockchain course material. Questions are loaded from a JSON file, so the question bank can be extended without touching the app code.

## Features

- **104 questions** across three formats: single choice, multiple select, and fill-in-the-blank
- Fuzzy answer matching for blanks (case-, punctuation-, and whitespace-insensitive, with support for alternative spellings)
- Running score with instant feedback and the correct answer shown on a wrong submission
- Jump to any question by number
- Bookmark questions and review them from the final screen
- Restart without reloading the page

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)

## Setup

```bash
git clone https://github.com/SarthakBharad/blockchain-exam-prep.git
cd blockchain-exam-prep

python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Running

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`. Run it from the repository root — `blockchain.json` is loaded by relative path.

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
└── requirements.txt   # Dependencies
```

## Notes

Questions are cached with `@st.cache_data`. After editing `blockchain.json`, clear the cache from the Streamlit menu or restart the app to pick up the changes.

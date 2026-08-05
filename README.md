# Blockchain Exam Prep

A dark-themed Streamlit quiz app for revising blockchain course material. Questions live in a JSON file, so the bank can be extended without touching the app code.

## Features

- **104 questions** in three formats: single choice, select-all-that-apply, and short answer
- Forgiving grading on short answers — case, punctuation, and spacing are ignored, and alternative wordings are accepted
- A progress ribbon across the top with one tick per question, showing at a glance what you got right, what you missed, and what you bookmarked
- Instant feedback with the correct answer shown when you get one wrong
- Bookmark questions, retry any question, and jump to any number
- Review screen listing missed and bookmarked questions, reachable at any point — not just after the last question

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

## Theme

The app is pinned to dark mode through `.streamlit/config.toml`, so it renders identically regardless of the visitor's system setting. The palette:

| Role | Hex |
| --- | --- |
| Canvas | `#0F1D33` |
| Cards, inputs, panels | `#1E3A5F` |
| Text | `#F1F3F5` |
| Accent — current position, corrections, primary actions | `#F4B942` |

To change any of these, edit both `.streamlit/config.toml` (which themes Streamlit's own widgets) and the constants near the top of `app.py` (which drive the custom CSS). They need to stay in sync.

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

**Select all that apply** — `correct` is a list; order does not matter when grading:

```json
{
  "question": "What are advantages of peer-to-peer networks?",
  "options": ["Single point of failure", "Mutability", "Velocity", "Transparency"],
  "correct": ["Velocity", "Transparency"],
  "type": "multi"
}
```

**Short answer** — the expected answer lives in `answer`; `options` and `correct` stay empty. Separate acceptable variants with `/`:

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
├── .streamlit/
│   └── config.toml    # Theme — must be committed for the deployed app to match
├── app.py             # UI, styling, and grading logic
├── blockchain.json    # Question bank
├── requirements.txt   # Dependencies
└── .gitignore
```

## Deploying

Push to GitHub, then deploy from [share.streamlit.io](https://share.streamlit.io) with `main` as the branch and `app.py` as the entry point. Later pushes redeploy automatically.

The in-app **Deploy** button reads your local git state at server start, so if you changed the remote or branch after launching, restart the server before using it.

## Notes

- Questions are cached with `@st.cache_data`. After editing `blockchain.json`, clear the cache from the Streamlit menu or restart the app to pick up changes.
- The virtual environment is not tracked. Its launcher scripts hardcode absolute paths, so it breaks if the project folder is moved or renamed — recreate it rather than trying to relocate it.
- Progress lives in Streamlit's session state, so refreshing the page starts a fresh run.
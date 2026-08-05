import json
import re

import streamlit as st

# ---------------------------------------------------------------- page config
st.set_page_config(
    page_title="Blockchain Exam Prep",
    page_icon="⛓️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

INK = "#1E3A5F"
SURFACE = "#F1F3F5"
ACCENT = "#F4B942"

# ---------------------------------------------------------------------- style
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&display=swap');

    :root {{
        --ink: {INK};
        --surface: {SURFACE};
        --accent: {ACCENT};
        --ink-soft: rgba(30, 58, 95, 0.62);
        --ink-line: rgba(30, 58, 95, 0.12);
    }}

    .stApp {{ background: var(--surface); }}
    .block-container {{ padding-top: 2.4rem; max-width: 46rem; }}

    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    h1, h2, h3 {{ font-family: 'Space Grotesk', sans-serif; color: var(--ink); }}

    /* --- masthead --- */
    .masthead {{
        display: flex; align-items: baseline; justify-content: space-between;
        gap: 1rem; margin-bottom: .85rem;
    }}
    .masthead .eyebrow {{
        font-family: 'Space Grotesk', sans-serif; font-weight: 700;
        font-size: .72rem; letter-spacing: .16em; text-transform: uppercase;
        color: var(--ink-soft);
    }}
    .masthead .tally {{
        font-family: 'Space Grotesk', sans-serif; font-weight: 700;
        font-size: .78rem; color: var(--ink);
        background: #fff; border: 1px solid var(--ink-line);
        padding: .22rem .6rem; border-radius: 999px;
    }}

    /* --- progress ribbon: one tick per question --- */
    .ribbon {{
        display: flex; flex-wrap: wrap; gap: 3px;
        margin-bottom: 1.4rem;
    }}
    .tick {{
        flex: 1 1 6px; min-width: 5px; height: 7px; border-radius: 2px;
        background: rgba(30, 58, 95, 0.13);
    }}
    .tick.right   {{ background: var(--ink); }}
    .tick.wrong   {{ background: rgba(30, 58, 95, 0.34); }}
    .tick.marked  {{ background: var(--accent); }}
    .tick.here    {{ background: var(--accent); height: 13px; margin-top: -3px; }}

    /* --- question card --- */
    .card {{
        background: #fff; border: 1px solid var(--ink-line);
        border-left: 4px solid var(--ink);
        border-radius: 10px; padding: 1.35rem 1.5rem 1.45rem;
        margin-bottom: 1.1rem;
    }}
    .card .kind {{
        font-family: 'Space Grotesk', sans-serif; font-weight: 700;
        font-size: .66rem; letter-spacing: .14em; text-transform: uppercase;
        color: var(--ink-soft); display: block; margin-bottom: .55rem;
    }}
    .card .kind .dot {{
        display: inline-block; width: 6px; height: 6px; border-radius: 50%;
        background: var(--accent); margin-right: .5rem; vertical-align: middle;
    }}
    .card .prompt {{
        font-size: 1.12rem; line-height: 1.5; font-weight: 500; color: var(--ink);
    }}

    /* --- verdict --- */
    .verdict {{
        border-radius: 8px; padding: .85rem 1.1rem; margin-bottom: 1rem;
        font-size: .93rem; line-height: 1.5;
    }}
    .verdict.right {{ background: #fff; border: 1px solid var(--ink); color: var(--ink); }}
    .verdict.wrong {{ background: #fff; border: 1px solid var(--accent); border-left: 4px solid var(--accent); color: var(--ink); }}
    .verdict strong {{ font-family: 'Space Grotesk', sans-serif; }}
    .verdict .key {{ display: block; margin-top: .4rem; color: var(--ink-soft); }}

    /* --- inputs --- */
    div[role="radiogroup"] label, .stCheckbox label {{ color: var(--ink) !important; }}
    .stTextInput input {{
        border: 1px solid var(--ink-line) !important; border-radius: 8px !important;
        color: var(--ink) !important; background: #fff !important;
    }}
    .stTextInput input:focus {{ border-color: var(--accent) !important; box-shadow: 0 0 0 2px rgba(244,185,66,.28) !important; }}

    /* --- buttons --- */
    .stButton > button {{
        font-family: 'Space Grotesk', sans-serif; font-weight: 700;
        font-size: .84rem; letter-spacing: .02em;
        border-radius: 8px; width: 100%; transition: transform .08s ease;
    }}
    .stButton > button:active {{ transform: translateY(1px); }}
    button[data-testid="baseButton-primary"],
    button[data-testid="stBaseButton-primary"] {{
        background: var(--accent) !important; color: var(--ink) !important;
        border: 1px solid var(--accent) !important;
    }}
    button[data-testid="baseButton-secondary"],
    button[data-testid="stBaseButton-secondary"] {{
        background: transparent !important; color: var(--ink) !important;
        border: 1px solid var(--ink-line) !important;
    }}
    button[data-testid="baseButton-secondary"]:hover,
    button[data-testid="stBaseButton-secondary"]:hover {{
        border-color: var(--ink) !important; background: #fff !important;
    }}

    /* --- score ring --- */
    .result {{ text-align: center; padding: 1.6rem 0 .4rem; }}
    .result .headline {{
        font-family: 'Space Grotesk', sans-serif; font-weight: 700;
        font-size: 1.5rem; color: var(--ink); margin-top: .9rem;
    }}
    .result .sub {{ color: var(--ink-soft); font-size: .92rem; margin-top: .3rem; }}

    footer, #MainMenu {{ visibility: hidden; }}
    @media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
    </style>
    """,
    unsafe_allow_html=True,
)

KIND_LABEL = {"single": "Single choice", "multi": "Select all that apply", "blank": "Short answer"}


# ------------------------------------------------------------------ questions
def normalize(text):
    """Lowercase, strip punctuation, collapse whitespace."""
    text = re.sub(r"[^a-z0-9 ]", " ", str(text).lower())
    return re.sub(r"\s+", " ", text).strip()


def is_correct(user, correct, qtype):
    if qtype == "single":
        return user == correct
    if qtype == "multi":
        return bool(user) and set(user) == set(correct)
    if qtype == "blank":
        if not str(user).strip():
            return False
        options = correct.split("/") if isinstance(correct, str) else [correct]
        return normalize(user) in {normalize(c) for c in options}
    return False


def expected(q):
    return q["answer"] if q["type"] == "blank" else q["correct"]


def readable(answer):
    if isinstance(answer, list):
        return " · ".join(answer)
    if isinstance(answer, str) and "/" in answer:
        return " / ".join(part.strip() for part in answer.split("/"))
    return str(answer)


@st.cache_data
def load_questions():
    with open("blockchain.json", "r", encoding="utf-8") as f:
        return json.load(f)


questions = load_questions()
total = len(questions)

# ----------------------------------------------------------------- app state
defaults = {"q_index": 0, "results": {}, "answers": {}, "bookmarked": set(), "finished": False}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go_to(index):
    st.session_state.q_index = max(0, min(total - 1, index))
    st.session_state.finished = False


results = st.session_state.results
score = sum(1 for v in results.values() if v)
answered = len(results)
q_index = st.session_state.q_index
q = questions[q_index]
graded = q_index in results

# ------------------------------------------------------------------ masthead
st.markdown(
    f"""
    <div class="masthead">
      <span class="eyebrow">Blockchain · Exam prep</span>
      <span class="tally">{score} / {answered} correct</span>
    </div>
    """,
    unsafe_allow_html=True,
)

ticks = []
for i in range(total):
    classes = ["tick"]
    if i == q_index:
        classes.append("here")
    elif i in st.session_state.bookmarked:
        classes.append("marked")
    elif i in results:
        classes.append("right" if results[i] else "wrong")
    ticks.append(f'<div class="{" ".join(classes)}"></div>')
st.markdown(f'<div class="ribbon">{"".join(ticks)}</div>', unsafe_allow_html=True)

# --------------------------------------------------------------------- review
if st.session_state.finished:
    pct = round(score / total * 100) if total else 0
    circumference = 2 * 3.14159 * 52
    st.markdown(
        f"""
        <div class="result">
          <svg width="140" height="140" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(30,58,95,.12)" stroke-width="10"/>
            <circle cx="60" cy="60" r="52" fill="none" stroke="{ACCENT}" stroke-width="10"
                    stroke-linecap="round" stroke-dasharray="{circumference}"
                    stroke-dashoffset="{circumference * (1 - pct / 100):.1f}"
                    transform="rotate(-90 60 60)"/>
            <text x="60" y="66" text-anchor="middle" fill="{INK}"
                  font-family="Space Grotesk, sans-serif" font-size="26" font-weight="700">{pct}%</text>
          </svg>
          <div class="headline">{score} of {total} correct</div>
          <div class="sub">{answered} answered · {len(st.session_state.bookmarked)} bookmarked</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.bookmarked:
        st.markdown("#### Bookmarked")
        for i in sorted(st.session_state.bookmarked):
            label = questions[i]["question"]
            label = label if len(label) < 70 else label[:67] + "…"
            if st.button(f"{i + 1}. {label}", key=f"bm_{i}"):
                go_to(i)
                st.rerun()

    missed = [i for i, ok in sorted(results.items()) if not ok]
    if missed:
        st.markdown("#### Missed")
        for i in missed:
            label = questions[i]["question"]
            label = label if len(label) < 70 else label[:67] + "…"
            if st.button(f"{i + 1}. {label}", key=f"missed_{i}"):
                go_to(i)
                st.rerun()

    back, restart = st.columns(2)
    with back:
        if st.button("Back to questions", key="resume"):
            st.session_state.finished = False
            st.rerun()
    with restart:
        if st.button("Start over", key="restart", type="primary"):
            st.session_state.clear()
            st.rerun()
    st.stop()

# ------------------------------------------------------------------- question
st.markdown(
    f"""
    <div class="card">
      <span class="kind"><span class="dot"></span>Question {q_index + 1} of {total} · {KIND_LABEL[q["type"]]}</span>
      <div class="prompt">{q["question"]}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

saved = st.session_state.answers.get(q_index)

if q["type"] == "single":
    options = q["options"]
    index = options.index(saved) if saved in options else None
    user_answer = st.radio(
        "Choose one", options, index=index, key=f"single_{q_index}",
        label_visibility="collapsed", disabled=graded,
    )
elif q["type"] == "multi":
    user_answer = st.multiselect(
        "Select every correct option", q["options"], default=saved or [],
        key=f"multi_{q_index}", disabled=graded,
    )
else:
    user_answer = st.text_input(
        "Type your answer", value=saved or "", key=f"blank_{q_index}",
        placeholder="Type your answer", label_visibility="collapsed", disabled=graded,
    )

# ------------------------------------------------------------------ verdict
if graded:
    if results[q_index]:
        st.markdown('<div class="verdict right"><strong>Correct.</strong></div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="verdict wrong"><strong>Not quite.</strong>'
            f'<span class="key">Answer: {readable(expected(q))}</span></div>',
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------- controls
if not graded:
    check, skip = st.columns([2, 1])
    with check:
        if st.button("Check answer", type="primary", key=f"check_{q_index}"):
            st.session_state.answers[q_index] = user_answer
            st.session_state.results[q_index] = is_correct(user_answer, expected(q), q["type"])
            st.rerun()
    with skip:
        if st.button("Skip", key=f"skip_{q_index}", disabled=q_index >= total - 1):
            go_to(q_index + 1)
            st.rerun()
else:
    nxt, retry = st.columns([2, 1])
    with nxt:
        if q_index < total - 1:
            if st.button("Next question", type="primary", key=f"next_{q_index}"):
                go_to(q_index + 1)
                st.rerun()
        else:
            if st.button("See results", type="primary", key="to_results"):
                st.session_state.finished = True
                st.rerun()
    with retry:
        if st.button("Try again", key=f"retry_{q_index}"):
            st.session_state.results.pop(q_index, None)
            st.session_state.answers.pop(q_index, None)
            for prefix in ("single", "multi", "blank"):
                st.session_state.pop(f"{prefix}_{q_index}", None)
            st.rerun()

prev, mark, jump_field, jump_go = st.columns([1.1, 1.3, 1, 0.7])

with prev:
    if st.button("Previous", key=f"prev_{q_index}", disabled=q_index == 0):
        go_to(q_index - 1)
        st.rerun()

with mark:
    marked = q_index in st.session_state.bookmarked
    if st.button("Bookmarked" if marked else "Bookmark", key=f"mark_{q_index}"):
        st.session_state.bookmarked.symmetric_difference_update({q_index})
        st.rerun()

with jump_field:
    target = st.number_input(
        "Jump to", min_value=1, max_value=total, value=q_index + 1, step=1,
        key=f"jump_{q_index}", label_visibility="collapsed",
    )

with jump_go:
    if st.button("Go", key=f"go_{q_index}"):
        go_to(int(target) - 1)
        st.rerun()

if answered:
    if st.button("Finish and review", key="finish"):
        st.session_state.finished = True
        st.rerun()
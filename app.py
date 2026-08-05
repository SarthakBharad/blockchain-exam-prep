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
        --ink-soft: #5A7392;
        --ink-line: #D8DEE6;
    }}

    .stApp {{ background: var(--surface); }}
    .block-container {{ padding-top: 2rem; padding-bottom: 4rem; max-width: 44rem; }}
    header[data-testid="stHeader"] {{ background: transparent; }}

    /* Every piece of text defaults to ink so a dark OS theme can't wash it out. */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp div {{
        font-family: 'Inter', sans-serif;
        color: var(--ink);
    }}
    h1, h2, h3, h4 {{ font-family: 'Space Grotesk', sans-serif; color: var(--ink); }}

    /* --- masthead --- */
    .masthead {{
        display: flex; align-items: center; justify-content: space-between;
        gap: 1rem; margin-bottom: .8rem;
    }}
    .masthead .eyebrow {{
        font-family: 'Space Grotesk', sans-serif; font-weight: 700;
        font-size: .74rem; letter-spacing: .15em; text-transform: uppercase;
        color: var(--ink-soft);
    }}
    .masthead .tally {{
        font-family: 'Space Grotesk', sans-serif; font-weight: 700;
        font-size: .8rem; color: var(--ink); white-space: nowrap;
        background: #fff; border: 1px solid var(--ink-line);
        padding: .3rem .7rem; border-radius: 999px;
    }}

    /* --- progress ribbon: one tick per question, uniform grid --- */
    .ribbon {{
        display: grid; grid-template-columns: repeat(auto-fill, minmax(9px, 1fr));
        gap: 3px; align-items: end; margin-bottom: 1.5rem; height: 14px;
    }}
    .tick {{ height: 7px; border-radius: 2px; background: #DDE2E9; }}
    .tick.right  {{ background: var(--ink); }}
    .tick.wrong  {{ background: #A8B6C8; }}
    .tick.marked {{ background: var(--accent); }}
    .tick.here   {{ background: var(--accent); height: 14px; }}

    /* --- question card --- */
    .card {{
        background: #fff; border: 1px solid var(--ink-line);
        border-left: 5px solid var(--ink);
        border-radius: 10px; padding: 1.4rem 1.6rem 1.5rem; margin-bottom: 1.25rem;
    }}
    .card .kind {{
        font-family: 'Space Grotesk', sans-serif; font-weight: 700;
        font-size: .68rem; letter-spacing: .13em; text-transform: uppercase;
        color: var(--ink-soft); display: block; margin-bottom: .6rem;
    }}
    .card .kind .dot {{
        display: inline-block; width: 6px; height: 6px; border-radius: 50%;
        background: var(--accent); margin-right: .5rem; vertical-align: middle;
    }}
    .card .prompt {{ font-size: 1.15rem; line-height: 1.55; font-weight: 500; }}

    /* --- answer options as cards --- */
    div[role="radiogroup"] {{ gap: .5rem !important; }}
    div[role="radiogroup"] > label {{
        background: #fff; border: 1px solid var(--ink-line); border-radius: 9px;
        padding: .8rem 1rem; margin: 0 !important; width: 100%;
        align-items: flex-start; transition: border-color .12s ease;
    }}
    div[role="radiogroup"] > label:hover {{ border-color: var(--ink-soft); }}
    div[role="radiogroup"] > label p {{
        font-size: .97rem !important; line-height: 1.5 !important; color: var(--ink) !important;
    }}
    .stCheckbox p, .stMultiSelect span, .stMultiSelect p {{ color: var(--ink) !important; }}

    /* --- text + number inputs --- */
    .stTextInput input, .stNumberInput input {{
        background: #fff !important; color: var(--ink) !important;
        border: 1px solid var(--ink-line) !important; border-radius: 8px !important;
        font-size: 1rem !important;
    }}
    .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(244, 185, 66, .3) !important;
    }}
    .stTextInput input::placeholder {{ color: #9AA9BC !important; }}
    .stNumberInput button {{ background: #fff !important; color: var(--ink) !important; }}
    div[data-baseweb="select"] > div {{
        background: #fff !important; border-color: var(--ink-line) !important;
    }}

    /* --- verdict --- */
    .verdict {{
        background: #fff; border: 1px solid var(--ink-line);
        border-radius: 9px; padding: .9rem 1.15rem; margin: .2rem 0 1.1rem;
        font-size: .96rem; line-height: 1.55;
    }}
    .verdict.right {{ border-left: 5px solid var(--ink); }}
    .verdict.wrong {{ border-left: 5px solid var(--accent); }}
    .verdict strong {{ font-family: 'Space Grotesk', sans-serif; font-weight: 700; }}
    .verdict .key {{ display: block; margin-top: .35rem; color: var(--ink-soft); }}

    /* --- buttons --- */
    .stButton > button {{
        font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: .88rem;
        border-radius: 9px; width: 100%; padding: .55rem 1rem; min-height: 2.6rem;
        transition: transform .08s ease, border-color .12s ease;
    }}
    .stButton > button:active {{ transform: translateY(1px); }}
    .stButton > button[kind="primary"] {{
        background: var(--accent) !important; color: var(--ink) !important;
        border: 1px solid var(--accent) !important;
    }}
    .stButton > button[kind="primary"]:hover {{ background: #EDAE2E !important; }}
    .stButton > button[kind="secondary"] {{
        background: #fff !important; color: var(--ink) !important;
        border: 1px solid var(--ink-line) !important;
    }}
    .stButton > button[kind="secondary"]:hover {{ border-color: var(--ink) !important; }}
    .stButton > button:disabled {{ opacity: .45; }}
    .stButton > button:focus-visible {{ outline: 3px solid rgba(244, 185, 66, .55); outline-offset: 2px; }}

    /* --- review list --- */
    .section-label {{
        font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: .74rem;
        letter-spacing: .13em; text-transform: uppercase; color: var(--ink-soft);
        margin: 1.6rem 0 .6rem;
    }}
    .review .stButton > button {{ text-align: left; justify-content: flex-start; font-weight: 500; }}

    /* --- result --- */
    .result {{ text-align: center; padding: 1.2rem 0 .2rem; }}
    .result .headline {{
        font-family: 'Space Grotesk', sans-serif; font-weight: 700;
        font-size: 1.55rem; margin-top: .8rem;
    }}
    .result .sub {{ color: var(--ink-soft); font-size: .93rem; margin-top: .35rem; }}

    footer, #MainMenu {{ visibility: hidden; }}
    @media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
    @media (max-width: 640px) {{
        .card {{ padding: 1.1rem 1.15rem 1.2rem; }}
        .card .prompt {{ font-size: 1.05rem; }}
    }}
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


def shorten(text, limit=68):
    return text if len(text) <= limit else text[: limit - 1] + "…"


@st.cache_data
def load_questions():
    with open("blockchain.json", "r", encoding="utf-8") as f:
        return json.load(f)


questions = load_questions()
total = len(questions)

# ------------------------------------------------------------------ app state
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

# -------------------------------------------------------------------- header
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

# -------------------------------------------------------------------- review
if st.session_state.finished:
    pct = round(score / total * 100) if total else 0
    circ = 2 * 3.14159 * 52
    st.markdown(
        f"""
        <div class="result">
          <svg width="150" height="150" viewBox="0 0 120 120" role="img" aria-label="{pct} percent correct">
            <circle cx="60" cy="60" r="52" fill="none" stroke="#DDE2E9" stroke-width="11"/>
            <circle cx="60" cy="60" r="52" fill="none" stroke="{ACCENT}" stroke-width="11"
                    stroke-linecap="round" stroke-dasharray="{circ:.1f}"
                    stroke-dashoffset="{circ * (1 - pct / 100):.1f}"
                    transform="rotate(-90 60 60)"/>
            <text x="60" y="67" text-anchor="middle" fill="{INK}"
                  font-family="Space Grotesk, sans-serif" font-size="27" font-weight="700">{pct}%</text>
          </svg>
          <div class="headline">{score} of {total} correct</div>
          <div class="sub">{answered} answered · {total - answered} left · {len(st.session_state.bookmarked)} bookmarked</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    missed = [i for i, ok in sorted(results.items()) if not ok]
    if missed:
        st.markdown('<div class="section-label">Worth another look</div>', unsafe_allow_html=True)
        st.markdown('<div class="review">', unsafe_allow_html=True)
        for i in missed:
            if st.button(f"{i + 1}.  {shorten(questions[i]['question'])}", key=f"missed_{i}"):
                go_to(i)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.bookmarked:
        st.markdown('<div class="section-label">Bookmarked</div>', unsafe_allow_html=True)
        st.markdown('<div class="review">', unsafe_allow_html=True)
        for i in sorted(st.session_state.bookmarked):
            if st.button(f"{i + 1}.  {shorten(questions[i]['question'])}", key=f"bm_{i}"):
                go_to(i)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    back, restart = st.columns(2)
    with back:
        if st.button("Back to questions", key="resume", type="primary"):
            st.session_state.finished = False
            st.rerun()
    with restart:
        if st.button("Start over", key="restart"):
            st.session_state.clear()
            st.rerun()
    st.stop()

# ------------------------------------------------------------------ question
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
    user_answer = st.radio(
        "Choose one", options,
        index=options.index(saved) if saved in options else None,
        key=f"single_{q_index}", label_visibility="collapsed", disabled=graded,
    )
elif q["type"] == "multi":
    user_answer = st.multiselect(
        "Select every correct option", q["options"], default=saved or [],
        key=f"multi_{q_index}", placeholder="Pick every option that applies", disabled=graded,
    )
else:
    user_answer = st.text_input(
        "Type your answer", value=saved or "", key=f"blank_{q_index}",
        placeholder="Type your answer", label_visibility="collapsed", disabled=graded,
    )

st.write("")

# ------------------------------------------------------------------- verdict
if graded:
    if results[q_index]:
        st.markdown('<div class="verdict right"><strong>Correct.</strong></div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="verdict wrong"><strong>Not quite.</strong>'
            f'<span class="key">Answer: {readable(expected(q))}</span></div>',
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------ controls
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
        elif st.button("See results", type="primary", key="to_results"):
            st.session_state.finished = True
            st.rerun()
    with retry:
        if st.button("Try again", key=f"retry_{q_index}"):
            st.session_state.results.pop(q_index, None)
            st.session_state.answers.pop(q_index, None)
            for prefix in ("single", "multi", "blank"):
                st.session_state.pop(f"{prefix}_{q_index}", None)
            st.rerun()

prev, mark, jump_field, jump_go = st.columns([1.15, 1.35, 1, .7])

with prev:
    if st.button("Previous", key=f"prev_{q_index}", disabled=q_index == 0):
        go_to(q_index - 1)
        st.rerun()

with mark:
    marked = q_index in st.session_state.bookmarked
    if st.button("★ Bookmarked" if marked else "☆ Bookmark", key=f"mark_{q_index}"):
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
    st.write("")
    if st.button("Finish and review", key="finish"):
        st.session_state.finished = True
        st.rerun()
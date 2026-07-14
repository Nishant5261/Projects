import streamlit as st
from data import JOB_ROLES, get_role_by_id, get_questions_for_session
from services import evaluate_answer, generate_report, transcribe_audio

st.set_page_config(
    page_title="Shadow – AI Interview System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    background: #0a0f1e !important;
    color: #e2e8f0 !important;
}
[data-testid="stAppViewContainer"] > .main { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1200px !important; }
footer, #MainMenu { display: none !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0f1e; }
::-webkit-scrollbar-thumb { background: #1e40af; border-radius: 3px; }

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.6; transform: scale(1.4); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-6px); }
}
@keyframes score-pop {
    0%   { transform: scale(0.8); opacity: 0; }
    70%  { transform: scale(1.05); }
    100% { transform: scale(1);   opacity: 1; }
}

/* Buttons */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 0.65rem 1.4rem !important;
    cursor: pointer !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
}
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%) !important;
    color: #fff !important;
    box-shadow: 0 4px 15px rgba(59,130,246,0.35) !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 8px 30px rgba(59,130,246,0.55) !important;
    background: linear-gradient(135deg, #2563eb 0%, #60a5fa 100%) !important;
}
.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) {
    background: rgba(255,255,255,0.06) !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(255,255,255,0.12) !important;
    color: #e2e8f0 !important;
    transform: translateY(-1px) !important;
    border-color: rgba(255,255,255,0.25) !important;
}
.stButton > button:active { transform: scale(0.97) !important; }

/* Inputs */
.stTextArea textarea, .stTextInput input {
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(59,130,246,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.2) !important;
}

/* Radio */
.stRadio div[role="radiogroup"] label {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    padding: 8px 14px !important;
    margin: 4px 0 !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
.stRadio div[role="radiogroup"] label:hover {
    background: rgba(59,130,246,0.12) !important;
    border-color: rgba(59,130,246,0.4) !important;
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #1d4ed8, #3b82f6, #60a5fa) !important;
    border-radius: 99px !important;
    transition: width 0.6s ease !important;
}
.stProgress > div > div {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 99px !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(15,23,42,0.6) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4) !important;
}
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-weight: 700 !important; }

hr { border-color: rgba(255,255,255,0.08) !important; }

/* Expander */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    transition: background 0.2s !important;
}
.streamlit-expanderHeader:hover { background: rgba(255,255,255,0.08) !important; }
.streamlit-expanderContent {
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    background: rgba(15,23,42,0.5) !important;
}

/* Alerts */
.stAlert { border-radius: 12px !important; border: none !important; font-family: 'Inter', sans-serif !important; }
[data-testid="stInfo"]    { background: rgba(59,130,246,0.12) !important; color: #93c5fd !important; }
[data-testid="stSuccess"] { background: rgba(34,197,94,0.12)  !important; color: #86efac !important; }
[data-testid="stWarning"] { background: rgba(234,179,8,0.12)  !important; color: #fde047 !important; }
[data-testid="stError"]   { background: rgba(239,68,68,0.12)  !important; color: #fca5a5 !important; }

/* Card hover class */
.shadow-card {
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(12px);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.shadow-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5);
    border-color: rgba(59,130,246,0.3);
}
.score-card {
    background: rgba(15,23,42,0.85);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    animation: score-pop 0.45s ease both;
}
.score-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}
.role-card {
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    cursor: default;
}
.role-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5);
    border-color: rgba(59,130,246,0.4);
}
.feature-pill {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 14px 22px;
    transition: transform 0.25s ease, border-color 0.25s ease;
}
.feature-pill:hover {
    transform: translateY(-3px);
    border-color: rgba(59,130,246,0.35);
}
.stMarkdown p { color: #94a3b8 !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "home",
        "selected_role": None,
        "selected_difficulty": "mixed",
        "question_count": 5,
        "session": None,
        "current_q_idx": 0,
        "answers": [],
        "current_answer_text": "",
        "evaluation_result": None,
        "report": None,
        "submitted_current": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


def go_to(page: str):
    st.session_state.page = page
    st.session_state.evaluation_result = None
    st.session_state.submitted_current = False
    st.session_state.current_answer_text = ""


def score_color(score: float) -> str:
    if score >= 8:
        return "#22c55e"
    elif score >= 6:
        return "#eab308"
    return "#ef4444"


# ─────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────
def show_home():
    st.markdown("""
    <div style="text-align:center; padding:3.5rem 0 2rem; animation:fadeInUp 0.7s ease;">
        <div style="font-size:5rem; font-weight:900; letter-spacing:0.18em; line-height:1;
                    margin-bottom:1.25rem;
                    background:linear-gradient(135deg,#e2e8f0 0%,#93c5fd 50%,#3b82f6 100%);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">
            SHADOW
        </div>
        <div style="display:inline-flex; align-items:center; gap:8px;
                    background:rgba(59,130,246,0.12); border:1px solid rgba(59,130,246,0.3);
                    border-radius:99px; padding:6px 18px; margin-bottom:1.5rem;
                    font-size:0.8rem; font-weight:600; color:#60a5fa; letter-spacing:0.05em;">
            <span style="width:8px; height:8px; background:#3b82f6; border-radius:50%;
                         display:inline-block; animation:pulse-dot 2s infinite;"></span>
            AI-POWERED INTERVIEW SYSTEM
        </div>
        <h1 style="font-size:3.5rem; font-weight:800; line-height:1.1;
                   color:#e2e8f0; margin:0 0 0.4rem; letter-spacing:-0.03em;">
            Precision Practice.
        </h1>
        <h1 style="font-size:3.5rem; font-weight:800; line-height:1.1; margin:0 0 1.5rem;
                   letter-spacing:-0.03em;
                   background:linear-gradient(135deg,#3b82f6,#60a5fa,#93c5fd);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                   background-clip:text; background-size:200% auto;
                   animation:shimmer 3s linear infinite;">
            Definitive Feedback.
        </h1>
        <p style="font-size:1.1rem; color:#64748b; max-width:540px;
                  margin:0 auto 2.5rem; line-height:1.7;">
            A high-stakes practice ground for professionals. Experience realistic
            technical and behavioral interviews evaluated instantly by AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature pills
    st.markdown("""
    <div style="display:flex; justify-content:center; gap:1.25rem;
                flex-wrap:wrap; margin-bottom:3rem; animation:fadeIn 0.9s ease;">
        <div class="feature-pill">
            <span style="font-size:1.4rem; animation:float 3s ease infinite;">🧠</span>
            <div>
                <div style="font-weight:600; color:#e2e8f0; font-size:0.88rem;">Adaptive Intelligence</div>
                <div style="font-size:0.73rem; color:#64748b;">Scales to your difficulty</div>
            </div>
        </div>
        <div class="feature-pill">
            <span style="font-size:1.4rem; animation:float 3s ease 0.5s infinite;">⚡</span>
            <div>
                <div style="font-weight:600; color:#e2e8f0; font-size:0.88rem;">Instant Evaluation</div>
                <div style="font-size:0.73rem; color:#64748b;">Real-time AI feedback</div>
            </div>
        </div>
        <div class="feature-pill">
            <span style="font-size:1.4rem; animation:float 3s ease 1s infinite;">📊</span>
            <div>
                <div style="font-weight:600; color:#e2e8f0; font-size:0.88rem;">Comprehensive Reports</div>
                <div style="font-size:0.73rem; color:#64748b;">Detailed performance breakdown</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h2 style="font-size:1.35rem; font-weight:700; color:#e2e8f0; margin-bottom:1.25rem; animation:slideInLeft 0.6s ease;">Choose Your Role</h2>', unsafe_allow_html=True)

    role_icons = {
        "software-engineer": "💻",
        "product-manager": "🎯",
        "data-scientist": "📈",
        "frontend-engineer": "🎨",
    }

    cols = st.columns(2, gap="medium")
    for i, role in enumerate(JOB_ROLES):
        icon = role_icons.get(role["id"], "🏢")
        cats_html = "".join(
            '<span style="background:rgba(59,130,246,0.12); color:#60a5fa; border-radius:6px;'
            ' padding:2px 10px; font-size:0.72rem; font-weight:500; margin:2px;">' + c + '</span>'
            for c in role["categories"][:4]
        )
        with cols[i % 2]:
            st.markdown(
                '<div class="role-card" style="animation:fadeInUp ' + str(0.4 + i * 0.1) + 's ease;">'
                '<div style="display:flex; align-items:flex-start; gap:14px; margin-bottom:14px;">'
                '<span style="font-size:2rem; line-height:1;">' + icon + '</span>'
                '<div>'
                '<div style="font-size:1.05rem; font-weight:700; color:#e2e8f0; margin-bottom:4px;">' + role["name"] + '</div>'
                '<div style="font-size:0.82rem; color:#64748b; line-height:1.5;">' + role["description"] + '</div>'
                '</div></div>'
                '<div style="display:flex; flex-wrap:wrap; gap:4px; margin-bottom:16px;">' + cats_html + '</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            if st.button("Start Interview →", key=f"role_{role['id']}", use_container_width=True, type="primary"):
                st.session_state.selected_role = role["id"]
                go_to("setup")
                st.rerun()


# ─────────────────────────────────────────────
# PAGE: SETUP
# ─────────────────────────────────────────────
def show_setup():
    role = get_role_by_id(st.session_state.selected_role)
    if not role:
        go_to("home")
        st.rerun()
        return

    if st.button("← Back"):
        go_to("home")
        st.rerun()

    icon_map = {"software-engineer": "💻", "product-manager": "🎯",
                "data-scientist": "📈", "frontend-engineer": "🎨"}
    icon = icon_map.get(role["id"], "🏢")

    st.markdown(
        '<div style="animation:fadeInUp 0.5s ease; margin-bottom:2rem;">'
        '<h1 style="font-size:2rem; font-weight:800; color:#e2e8f0; margin:0.5rem 0 0.25rem;">Configure Your Interview</h1>'
        '<div style="display:flex; align-items:center; gap:10px; color:#64748b; font-size:0.9rem;">'
        '<span>' + icon + '</span><span>' + role["name"] + ' — ' + role["description"] + '</span>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div style="font-size:0.82rem; font-weight:600; color:#64748b; letter-spacing:0.05em; margin-bottom:12px;">DIFFICULTY LEVEL</div>', unsafe_allow_html=True)
        diff_labels = {"easy": "🟢  Easy", "medium": "🟡  Medium", "hard": "🔴  Hard", "mixed": "🎲  Mixed"}
        difficulty = st.radio(
            "difficulty",
            options=["easy", "medium", "hard", "mixed"],
            format_func=lambda x: diff_labels[x],
            index=["easy", "medium", "hard", "mixed"].index(st.session_state.selected_difficulty),
            label_visibility="collapsed",
        )
        st.session_state.selected_difficulty = difficulty

    with col2:
        st.markdown('<div style="font-size:0.82rem; font-weight:600; color:#64748b; letter-spacing:0.05em; margin-bottom:12px;">NUMBER OF QUESTIONS</div>', unsafe_allow_html=True)
        q_count = st.slider(
            "Questions",
            min_value=3,
            max_value=min(15, len(role["questions"])),
            value=st.session_state.question_count,
            label_visibility="collapsed",
        )
        st.session_state.question_count = q_count
        st.markdown(
            '<div style="text-align:center; background:rgba(59,130,246,0.1);'
            ' border:1px solid rgba(59,130,246,0.25); border-radius:10px; padding:12px; margin-top:8px;">'
            '<span style="font-size:2rem; font-weight:800; color:#60a5fa;">' + str(q_count) + '</span>'
            '<span style="color:#64748b; font-size:0.9rem;"> question' + ('s' if q_count != 1 else '') + '</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<br>', unsafe_allow_html=True)
    cats_parts = "  ·  ".join('<span style="color:#60a5fa;">' + c + '</span>' for c in role["categories"])
    st.markdown('<div style="font-size:0.82rem; color:#475569; margin-bottom:1.5rem;">Categories: ' + cats_parts + '</div>', unsafe_allow_html=True)

    if st.button("🚀  Begin Interview", type="primary", use_container_width=True):
        with st.spinner("Preparing your session..."):
            questions = get_questions_for_session(role["id"], difficulty, q_count)
            st.session_state.session = {
                "sessionId": f"session-{id(questions)}",
                "role": role,
                "questions": questions,
                "totalQuestions": len(questions),
            }
            st.session_state.current_q_idx = 0
            st.session_state.answers = []
            st.session_state.evaluation_result = None
            st.session_state.submitted_current = False
            st.session_state.current_answer_text = ""
        go_to("interview")
        st.rerun()


# ─────────────────────────────────────────────
# PAGE: INTERVIEW
# ─────────────────────────────────────────────
def show_interview():
    session = st.session_state.session
    if not session:
        go_to("home")
        st.rerun()
        return

    questions = session["questions"]
    total = len(questions)
    idx = st.session_state.current_q_idx

    if idx >= total:
        go_to("report_loading")
        st.rerun()
        return

    question = questions[idx]
    progress_pct = int((idx / total) * 100)

    # Header bar
    col_title, col_prog, col_exit = st.columns([3, 5, 1])
    with col_title:
        st.markdown('<div style="font-weight:700; color:#e2e8f0; font-size:1rem; padding-top:6px;">' + session["role"]["name"] + '</div>', unsafe_allow_html=True)
    with col_prog:
        st.markdown(
            '<div style="padding-top:4px;">'
            '<div style="display:flex; justify-content:space-between; color:#64748b; font-size:0.75rem; margin-bottom:5px;">'
            '<span>Question ' + str(idx + 1) + ' of ' + str(total) + '</span>'
            '<span>' + str(progress_pct) + '%</span>'
            '</div>'
            '<div style="background:rgba(255,255,255,0.08); border-radius:99px; height:6px; overflow:hidden;">'
            '<div style="width:' + str(progress_pct) + '%; height:100%;'
            ' background:linear-gradient(90deg,#1d4ed8,#3b82f6,#60a5fa);'
            ' border-radius:99px; transition:width 0.6s ease;"></div>'
            '</div></div>',
            unsafe_allow_html=True,
        )
    with col_exit:
        if st.button("✕", help="Exit to home"):
            go_to("home")
            st.rerun()

    st.markdown('<div style="height:1px; background:rgba(255,255,255,0.06); margin:14px 0 22px;"></div>', unsafe_allow_html=True)

    # Question card
    diff_colors = {"easy": "#22c55e", "medium": "#eab308", "hard": "#ef4444"}
    diff = question.get("difficulty", "medium")
    diff_color = diff_colors.get(diff, "#94a3b8")

    st.markdown(
        '<div style="background:rgba(15,23,42,0.75); border:1px solid rgba(255,255,255,0.08);'
        ' border-left:4px solid ' + diff_color + '; border-radius:16px; padding:1.5rem;'
        ' backdrop-filter:blur(12px); margin-bottom:1.5rem; animation:fadeInUp 0.5s ease;">'
        '<div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">'
        '<span style="background:rgba(59,130,246,0.12); color:#60a5fa; border-radius:6px;'
        ' padding:3px 12px; font-size:0.75rem; font-weight:600;">' + question["category"] + '</span>'
        '<span style="background:rgba(255,255,255,0.06); color:' + diff_color + '; border-radius:6px;'
        ' padding:3px 12px; font-size:0.75rem; font-weight:600;">' + diff.capitalize() + '</span>'
        '</div>'
        '<p style="font-size:1.15rem; font-weight:600; color:#e2e8f0; line-height:1.6; margin:0;">'
        + question["text"] +
        '</p></div>',
        unsafe_allow_html=True,
    )

    already_submitted = st.session_state.submitted_current

    if not already_submitted:
        st.markdown('<div style="font-size:0.82rem; font-weight:600; color:#64748b; letter-spacing:0.05em; margin-bottom:8px;">🎙️ RECORD ANSWER (OPTIONAL)</div>', unsafe_allow_html=True)
        audio_data = st.audio_input("Record", label_visibility="collapsed")
        if audio_data is not None:
            if st.button("📝  Transcribe Recording"):
                with st.spinner("Transcribing..."):
                    try:
                        text = transcribe_audio(audio_data.read())
                        st.session_state.current_answer_text = text
                        st.rerun()
                    except Exception as e:
                        st.error(f"Transcription failed: {e}")

        st.markdown('<div style="font-size:0.82rem; font-weight:600; color:#64748b; letter-spacing:0.05em; margin:16px 0 8px;">✍️ YOUR ANSWER</div>', unsafe_allow_html=True)
        answer_text = st.text_area(
            "answer",
            value=st.session_state.current_answer_text,
            height=190,
            placeholder="Type your answer here, or record audio above and transcribe it...",
            label_visibility="collapsed",
        )
        st.session_state.current_answer_text = answer_text

        col_sub, col_skip = st.columns([4, 1])
        with col_sub:
            if st.button("✅  Submit Answer", type="primary", use_container_width=True, disabled=not answer_text.strip()):
                with st.spinner("Evaluating your answer..."):
                    result = evaluate_answer(
                        question_text=question["text"],
                        answer_text=answer_text,
                        expected_key_points=question.get("expectedKeyPoints", []),
                        category=question.get("category", "General"),
                        difficulty=question.get("difficulty", "medium"),
                    )
                st.session_state.evaluation_result = result
                st.session_state.submitted_current = True
                st.session_state.answers.append({
                    "question_text": question["text"],
                    "answer_text": answer_text,
                    "category": question.get("category", "General"),
                    "difficulty": question.get("difficulty", "medium"),
                    "evaluation": result,
                })
                st.rerun()
        with col_skip:
            if st.button("Skip →", use_container_width=True):
                st.session_state.evaluation_result = None
                st.session_state.submitted_current = False
                st.session_state.current_answer_text = ""
                st.session_state.current_q_idx += 1
                st.rerun()

    else:
        ev = st.session_state.evaluation_result or {}
        scores = ev.get("scores", {})
        overall = scores.get("overall", 5)
        sentiment = ev.get("sentiment", "neutral")
        s_colors = {"positive": "#22c55e", "neutral": "#eab308", "negative": "#ef4444"}
        s_color = s_colors.get(sentiment, "#94a3b8")

        # Evaluation summary
        st.markdown(
            '<div style="display:flex; align-items:flex-start; gap:16px; margin-bottom:1.5rem; animation:fadeInUp 0.5s ease;">'
            '<div style="background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.25);'
            ' border-radius:16px; padding:16px 24px; text-align:center; min-width:110px;">'
            '<div style="font-size:2.2rem; font-weight:800; color:#60a5fa; animation:score-pop 0.5s ease;">' + str(overall) + '</div>'
            '<div style="font-size:0.68rem; color:#64748b; font-weight:600;">/10 OVERALL</div>'
            '</div>'
            '<div style="flex:1;">'
            '<div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">'
            '<span style="width:8px; height:8px; background:' + s_color + '; border-radius:50%; display:inline-block;"></span>'
            '<span style="font-size:0.78rem; color:' + s_color + '; font-weight:600;">' + sentiment.upper() + ' RESPONSE</span>'
            '</div>'
            '<p style="color:#94a3b8; font-size:0.88rem; line-height:1.65; margin:0;">' + ev.get("feedback", "") + '</p>'
            '</div></div>',
            unsafe_allow_html=True,
        )

        # Score breakdown
        st.markdown('<div style="font-size:0.78rem; font-weight:600; color:#64748b; letter-spacing:0.05em; margin-bottom:10px;">SCORE BREAKDOWN</div>', unsafe_allow_html=True)
        score_items = [
            ("Relevance", scores.get("relevance", 0)),
            ("Clarity", scores.get("clarity", 0)),
            ("Technical", scores.get("technicalAccuracy", 0)),
            ("Completeness", scores.get("completeness", 0)),
        ]
        scols = st.columns(4)
        for j, (label, val) in enumerate(score_items):
            c = score_color(val)
            with scols[j]:
                st.markdown(
                    '<div class="score-card" style="animation-delay:' + str(j * 0.08) + 's;">'
                    '<div style="font-size:1.7rem; font-weight:800; color:' + c + ';">' + str(val) + '</div>'
                    '<div style="font-size:0.65rem; color:#64748b; font-weight:600; margin:4px 0 8px;">' + label.upper() + '</div>'
                    '<div style="background:rgba(255,255,255,0.08); border-radius:99px; height:4px; overflow:hidden;">'
                    '<div style="width:' + str(val * 10) + '%; height:100%; background:' + c + '; border-radius:99px;"></div>'
                    '</div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)

        str_col, imp_col = st.columns(2, gap="medium")
        with str_col:
            if ev.get("strengths"):
                st.markdown('<div style="font-size:0.78rem; font-weight:600; color:#64748b; letter-spacing:0.05em; margin-bottom:10px;">✅ STRENGTHS</div>', unsafe_allow_html=True)
                for s in ev["strengths"]:
                    st.markdown(
                        '<div style="background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.2);'
                        ' border-radius:8px; padding:10px 14px; color:#86efac; font-size:0.85rem; margin-bottom:6px;">✓ ' + s + '</div>',
                        unsafe_allow_html=True,
                    )
        with imp_col:
            if ev.get("improvements"):
                st.markdown('<div style="font-size:0.78rem; font-weight:600; color:#64748b; letter-spacing:0.05em; margin-bottom:10px;">🔧 TO IMPROVE</div>', unsafe_allow_html=True)
                for s in ev["improvements"]:
                    st.markdown(
                        '<div style="background:rgba(234,179,8,0.08); border:1px solid rgba(234,179,8,0.2);'
                        ' border-radius:8px; padding:10px 14px; color:#fde047; font-size:0.85rem; margin-bottom:6px;">△ ' + s + '</div>',
                        unsafe_allow_html=True,
                    )

        if ev.get("coveredKeyPoints") or ev.get("missedKeyPoints"):
            with st.expander("📋 Key Points Coverage"):
                kp1, kp2 = st.columns(2)
                with kp1:
                    st.markdown("**Covered ✅**")
                    for p in ev.get("coveredKeyPoints", []):
                        st.markdown(f"- {p}")
                with kp2:
                    st.markdown("**Missed ❌**")
                    for p in ev.get("missedKeyPoints", []):
                        st.markdown(f"- {p}")

        st.markdown('<div style="height:1px; background:rgba(255,255,255,0.06); margin:20px 0;"></div>', unsafe_allow_html=True)
        is_last = idx >= total - 1
        btn_label = "📄  Generate Final Report →" if is_last else "Next Question →"
        if st.button(btn_label, type="primary", use_container_width=True):
            st.session_state.current_q_idx += 1
            st.session_state.evaluation_result = None
            st.session_state.submitted_current = False
            st.session_state.current_answer_text = ""
            if is_last:
                go_to("report_loading")
            st.rerun()


# ─────────────────────────────────────────────
# PAGE: REPORT LOADING
# ─────────────────────────────────────────────
def show_report_loading():
    session = st.session_state.session
    if not session or not st.session_state.answers:
        go_to("home")
        st.rerun()
        return
    st.markdown("""
    <div style="text-align:center; padding:4rem 0; animation:fadeIn 0.5s ease;">
        <div style="font-size:3rem; margin-bottom:1rem; animation:float 2s ease infinite;">📊</div>
        <h2 style="color:#e2e8f0; font-weight:700;">Generating Your Report...</h2>
        <p style="color:#64748b;">Analyzing your responses and compiling AI feedback</p>
    </div>
    """, unsafe_allow_html=True)
    with st.spinner(""):
        report = generate_report(role_name=session["role"]["name"], answers=st.session_state.answers)
        st.session_state.report = report
    go_to("report")
    st.rerun()


# ─────────────────────────────────────────────
# PAGE: REPORT
# ─────────────────────────────────────────────
def show_report():
    report = st.session_state.report
    session = st.session_state.session
    if not report or not session:
        go_to("home")
        st.rerun()
        return

    overall   = report.get("overallScore", 0)
    grade     = report.get("grade", "F")
    rec       = report.get("recommendation", "Consider")

    grade_colors = {"A+": "#22c55e", "A": "#22c55e", "B": "#60a5fa",
                    "C": "#eab308", "D": "#f97316", "F": "#ef4444"}
    rec_colors   = {"Strong Hire": "#22c55e", "Hire": "#22c55e",
                    "Consider": "#eab308", "Pass": "#ef4444", "Strong Pass": "#ef4444"}
    rec_icons    = {"Strong Hire": "✅", "Hire": "✅",
                    "Consider": "🟡", "Pass": "❌", "Strong Pass": "❌"}

    g_color = grade_colors.get(grade, "#94a3b8")
    r_color = rec_colors.get(rec, "#94a3b8")
    r_icon  = rec_icons.get(rec, "⚪")

    st.markdown(
        '<div style="text-align:center; padding:2rem 0 1.5rem; animation:fadeInUp 0.6s ease;">'
        '<h1 style="font-size:2.2rem; font-weight:800; color:#e2e8f0; margin-bottom:0.25rem;">Performance Report</h1>'
        '<p style="color:#64748b; font-size:0.9rem;">' + session["role"]["name"] + ' · ' + str(report.get("totalQuestions", 0)) + ' questions answered</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # KPI cards
    kpi1, kpi2, kpi3 = st.columns(3, gap="medium")
    with kpi1:
        st.markdown(
            '<div class="shadow-card" style="text-align:center; animation:score-pop 0.5s ease;">'
            '<div style="font-size:0.72rem; color:#64748b; font-weight:600; letter-spacing:0.06em; margin-bottom:8px;">OVERALL SCORE</div>'
            '<div style="font-size:3rem; font-weight:800; color:#60a5fa; line-height:1;">' + str(overall) + '</div>'
            '<div style="font-size:0.72rem; color:#475569; margin-bottom:12px;">out of 10</div>'
            '<div style="background:rgba(255,255,255,0.08); border-radius:99px; height:6px; overflow:hidden;">'
            '<div style="width:' + str(int(overall * 10)) + '%; height:100%;'
            ' background:linear-gradient(90deg,#1d4ed8,#60a5fa); border-radius:99px;"></div>'
            '</div></div>',
            unsafe_allow_html=True,
        )
    with kpi2:
        st.markdown(
            '<div class="shadow-card" style="text-align:center; animation:score-pop 0.6s ease;">'
            '<div style="font-size:0.72rem; color:#64748b; font-weight:600; letter-spacing:0.06em; margin-bottom:8px;">GRADE</div>'
            '<div style="font-size:3rem; font-weight:800; color:' + g_color + '; line-height:1;">' + grade + '</div>'
            '<div style="font-size:0.72rem; color:#475569;">performance grade</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with kpi3:
        st.markdown(
            '<div class="shadow-card" style="text-align:center; animation:score-pop 0.7s ease;">'
            '<div style="font-size:0.72rem; color:#64748b; font-weight:600; letter-spacing:0.06em; margin-bottom:8px;">RECOMMENDATION</div>'
            '<div style="font-size:1.6rem; font-weight:800; color:' + r_color + '; line-height:1.3;">' + r_icon + ' ' + rec + '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

    # Feedback
    st.markdown(
        '<div class="shadow-card" style="margin-bottom:1.25rem; animation:fadeIn 0.7s ease;">'
        '<div style="font-size:0.72rem; color:#64748b; font-weight:600; letter-spacing:0.06em; margin-bottom:10px;">💬 OVERALL FEEDBACK</div>'
        '<p style="color:#94a3b8; line-height:1.75; font-size:0.95rem; margin:0;">' + report.get("overallFeedback", "") + '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Strengths + Improvements
    s_col, i_col = st.columns(2, gap="medium")
    with s_col:
        strengths = report.get("topStrengths", [])
        items = "".join(
            '<div style="display:flex; align-items:flex-start; gap:10px; padding:10px 0;'
            ' border-bottom:1px solid rgba(255,255,255,0.05);">'
            '<span style="color:#22c55e; font-weight:700; margin-top:1px;">✓</span>'
            '<span style="color:#94a3b8; font-size:0.85rem; line-height:1.5;">' + s + '</span>'
            '</div>'
            for s in strengths
        ) or '<p style="color:#475569; font-size:0.85rem;">None identified.</p>'
        st.markdown(
            '<div class="shadow-card" style="animation:slideInLeft 0.6s ease;">'
            '<div style="font-size:0.72rem; color:#64748b; font-weight:600; letter-spacing:0.06em; margin-bottom:10px;">✅ TOP STRENGTHS</div>'
            + items + '</div>',
            unsafe_allow_html=True,
        )
    with i_col:
        improvements = report.get("keyImprovements", [])
        items = "".join(
            '<div style="display:flex; align-items:flex-start; gap:10px; padding:10px 0;'
            ' border-bottom:1px solid rgba(255,255,255,0.05);">'
            '<span style="color:#eab308; font-weight:700; margin-top:1px;">△</span>'
            '<span style="color:#94a3b8; font-size:0.85rem; line-height:1.5;">' + s + '</span>'
            '</div>'
            for s in improvements
        ) or '<p style="color:#475569; font-size:0.85rem;">None identified.</p>'
        st.markdown(
            '<div class="shadow-card" style="animation:slideInLeft 0.7s ease;">'
            '<div style="font-size:0.72rem; color:#64748b; font-weight:600; letter-spacing:0.06em; margin-bottom:10px;">🔧 KEY IMPROVEMENTS</div>'
            + items + '</div>',
            unsafe_allow_html=True,
        )

    # Category breakdown
    category_scores = report.get("categoryScores", [])
    if category_scores:
        cat_rows = "".join(
            '<div style="margin-bottom:14px;">'
            '<div style="display:flex; justify-content:space-between; margin-bottom:5px;">'
            '<span style="color:#94a3b8; font-size:0.85rem;">' + cat["category"] + '</span>'
            '<span style="color:' + score_color(cat["score"]) + '; font-weight:600; font-size:0.85rem;">' + str(cat["score"]) + '/10</span>'
            '</div>'
            '<div style="background:rgba(255,255,255,0.07); border-radius:99px; height:6px; overflow:hidden;">'
            '<div style="width:' + str(int(cat["score"] * 10)) + '%; height:100%; background:' + score_color(cat["score"]) + '; border-radius:99px;"></div>'
            '</div></div>'
            for cat in sorted(category_scores, key=lambda x: x["score"], reverse=True)
        )
        st.markdown(
            '<div class="shadow-card" style="margin-bottom:1.25rem; animation:fadeIn 0.8s ease;">'
            '<div style="font-size:0.72rem; color:#64748b; font-weight:600; letter-spacing:0.06em; margin-bottom:16px;">📂 PERFORMANCE BY CATEGORY</div>'
            + cat_rows + '</div>',
            unsafe_allow_html=True,
        )

    # Q-by-Q
    answers = st.session_state.answers
    if answers:
        with st.expander("📋 Question-by-Question Breakdown"):
            for i, a in enumerate(answers):
                ev = a["evaluation"]
                oq = ev["scores"].get("overall", 0)
                c  = score_color(oq)
                st.markdown(
                    '<div style="padding:14px 0; border-bottom:1px solid rgba(255,255,255,0.06);">'
                    '<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">'
                    '<span style="color:#e2e8f0; font-weight:600; font-size:0.9rem; flex:1; padding-right:16px;">Q' + str(i + 1) + ': ' + a["question_text"] + '</span>'
                    '<span style="color:' + c + '; font-weight:700; font-size:1.1rem; white-space:nowrap;">' + str(oq) + '/10</span>'
                    '</div>'
                    '<p style="color:#64748b; font-size:0.82rem; margin:0;">' + ev.get("feedback", "") + '</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )

    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        if st.button("🔄  Practice Again", type="primary", use_container_width=True):
            go_to("setup")
            st.rerun()
    with c2:
        if st.button("🏠  Choose Different Role", use_container_width=True):
            go_to("home")
            st.rerun()


# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
page = st.session_state.page
if page == "home":
    show_home()
elif page == "setup":
    show_setup()
elif page == "interview":
    show_interview()
elif page == "report_loading":
    show_report_loading()
elif page == "report":
    show_report()
else:
    go_to("home")
    st.rerun()

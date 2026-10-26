import streamlit as st

try:
    from google import genai
except ImportError:  # pragma: no cover - exercised when dependencies are missing
    genai = None

try:
    import requests
except ImportError:  # pragma: no cover - exercised when dependencies are missing
    requests = None

try:
    import PyPDF2
except ImportError:  # pragma: no cover - exercised when dependencies are missing
    PyPDF2 = None

try:
    import docx
except ImportError:  # pragma: no cover - exercised when dependencies are missing
    docx = None

st.set_page_config(
    page_title="AI Text Humanizer",
    page_icon="✍️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #111827 0%, #020617 45%, #000000 100%);
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
        border-right: 1px solid rgba(129, 140, 248, 0.2);
    }
    .hero-card {
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(129, 140, 248, 0.25);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 18px 45px rgba(2, 6, 23, 0.45);
        margin-bottom: 18px;
        animation: fadeUp 0.7s ease both;
    }
    .hero-card h1 {
        font-size: 2rem;
        margin-bottom: 0.4rem;
        color: #f8fafc;
    }
    .hero-card p {
        color: #cbd5e1;
        font-size: 1rem;
        line-height: 1.6;
    }
    .pill {
        display: inline-block;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 10px;
        animation: pulse 2.2s infinite;
    }
    .panel {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(129, 140, 248, 0.2);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 12px 32px rgba(2, 6, 23, 0.3);
        animation: fadeUp 0.8s ease both;
    }
    div.stButton > button {
        border-radius: 12px;
        padding: 0.6rem 1rem;
        transition: transform 180ms ease, box-shadow 180ms ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2);
    }
    .stTabs [role="tab"] {
        color: #cbd5e1;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        color: white;
        background: rgba(99, 102, 241, 0.2);
        border-radius: 10px;
    }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.03); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key = st.session_state.api_key

if (genai is None and requests is None) or PyPDF2 is None or docx is None:
    st.error("⚠️ Required dependencies are missing. Please install the packages listed in requirements.txt and reload the page.")
    st.stop()

if not api_key:
    st.markdown(
        """
        <div class="hero-card">
            <span class="pill">AI Text Humanizer</span>
            <h1>Unlock the humanizer</h1>
            <p>Paste your Gemini API key to access the full experience. Once you’re in, you can upload documents, generate text, and humanize it with a polished, cinematic interface.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        entered_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            placeholder="Paste your API key here",
            help="Get a free key at https://aistudio.google.com — no credit card needed.",
            label_visibility="collapsed",
        )
        if st.button("Continue to app", type="primary", use_container_width=True):
            if entered_key.strip():
                st.session_state.api_key = entered_key.strip()
                st.rerun()
            else:
                st.error("Please enter your API key to continue.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

st.title("✍️ AI Text Humanizer")
st.caption("Generate AI text or upload a document, then humanize it to sound natural and bypass AI detectors.")

with st.sidebar:
    st.header("⚙️ Controls")
    st.caption("Gemini key is ready")
    if st.button("🔐 Change API key", use_container_width=True):
        st.session_state.api_key = ""
        st.rerun()
    st.divider()
    st.markdown("**Humanization controls**")
    humanize_strength = st.select_slider(
        "Humanization Strength",
        options=["Light", "Moderate", "Aggressive"],
        value="Moderate",
        help="Light: minor rewrites. Moderate: balanced. Aggressive: full rewrite.",
    )
    writing_style = st.selectbox(
        "Writing Style",
        ["Natural / Conversational", "Academic", "Professional / Business", "Casual / Informal", "Creative / Narrative"],
    )


def get_client(key: str):
    if genai is None:
        raise ImportError("google-genai is not installed. Please install the package from requirements.txt.")
    return genai.Client(api_key=key)


def generate_text(prompt: str, key: str) -> str:
    if genai is not None:
        client = get_client(key)
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return getattr(response, "text", "") or ""

    if requests is None:
        raise ImportError("Gemini client dependencies are unavailable.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    return "".join(part.get("text", "") for part in parts)


def extract_text_from_pdf(file) -> str:
    reader = PyPDF2.PdfReader(file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join(p.text for p in doc.paragraphs)


def build_humanize_prompt(text: str, strength: str, style: str) -> str:
    strength_instructions = {
        "Light": (
            "Make minor improvements: vary sentence length slightly, replace a few overly formal or robotic phrases "
            "with more natural alternatives, and fix any unnatural rhythm. Keep the structure mostly intact."
        ),
        "Moderate": (
            "Rewrite the text to feel naturally human-written. Vary sentence length and structure, use contractions "
            "where appropriate, inject subtle personality, break up overly long sentences, and remove any repetitive "
            "or formulaic patterns typical of AI writing. Keep all original meaning and information."
        ),
        "Aggressive": (
            "Completely rewrite the text from scratch to sound like a real person wrote it. Change the structure, "
            "reorganize ideas, use diverse vocabulary, add natural transitions, vary paragraph length, include "
            "occasional rhetorical questions or first-person perspective where fitting, and eliminate all AI "
            "tell-tale signs (bullet-point overuse, excessive hedging, formulaic conclusions). Preserve all "
            "original facts and meaning but transform the voice entirely."
        ),
    }

    style_instructions = {
        "Natural / Conversational": "Write as if explaining something to a friend — warm, direct, and easy to read.",
        "Academic": "Use precise language, formal tone, and well-structured arguments appropriate for academic writing.",
        "Professional / Business": "Use clear, confident business language. Concise, authoritative, no fluff.",
        "Casual / Informal": "Very relaxed tone. Short sentences. Contractions everywhere. Like a text message or blog post.",
        "Creative / Narrative": "Use vivid language, storytelling elements, and engaging prose with personality.",
    }

    return f"""You are an expert human writer and editor. Your task is to humanize the following AI-generated text so it passes AI detection tools and reads as naturally written by a human.

HUMANIZATION LEVEL: {strength}
{strength_instructions[strength]}

WRITING STYLE: {style}
{style_instructions[style]}

RULES:
- Do NOT change the meaning, facts, or key information
- Do NOT add new information that wasn't in the original
- Do NOT use bullet points or numbered lists unless the original did
- Remove any phrases that sound robotic or formulaic (e.g. "It is worth noting that...", "In conclusion,", "Furthermore,", "It is important to...")
- Use varied sentence structures — mix short punchy sentences with longer ones
- Return ONLY the humanized text with no preamble, explanation, or meta-commentary

TEXT TO HUMANIZE:
{text}"""


def build_generate_prompt(topic: str, word_count: int, content_type: str) -> str:
    return f"""Write a {content_type} about the following topic. Aim for approximately {word_count} words.

Topic: {topic}

Write the full text now:"""


if not api_key:
    st.info("👈 Enter your free **Gemini API key** in the sidebar to get started. No credit card required — get one at [aistudio.google.com](https://aistudio.google.com).")
    st.stop()

tab1, tab2 = st.tabs(["📄 Upload Document", "🤖 Generate AI Text"])

with tab1:
    st.subheader("Upload a Document")
    st.markdown("Upload a PDF, Word (.docx), or plain text file. The text will be extracted and humanized.")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        with st.spinner("Extracting text..."):
            try:
                if uploaded_file.type == "application/pdf":
                    raw_text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.type in (
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "application/msword",
                ):
                    raw_text = extract_text_from_docx(uploaded_file)
                else:
                    raw_text = uploaded_file.read().decode("utf-8", errors="ignore")
            except Exception as e:
                st.error(f"Could not read file: {e}")
                raw_text = ""

        if raw_text.strip():
            word_count = len(raw_text.split())
            st.success(f"✅ Extracted **{word_count:,} words** from `{uploaded_file.name}`")

            with st.expander("Preview extracted text", expanded=False):
                st.text_area("Extracted Text", raw_text[:3000] + ("..." if len(raw_text) > 3000 else ""), height=200, disabled=True)

            if st.button("🪄 Humanize Document", type="primary", use_container_width=True, key="humanize_doc"):
                try:
                    prompt = build_humanize_prompt(raw_text, humanize_strength, writing_style)

                    with st.spinner("Humanizing your text... this may take a moment for longer documents."):
                        humanized = generate_text(prompt, api_key)

                    st.divider()
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original Text**")
                        st.text_area("original", raw_text, height=400, disabled=True, label_visibility="collapsed")
                    with col2:
                        st.markdown("**Humanized Text ✨**")
                        st.text_area("humanized", humanized, height=400, label_visibility="collapsed")

                    st.download_button(
                        "⬇️ Download Humanized Text",
                        data=humanized,
                        file_name=f"humanized_{uploaded_file.name.rsplit('.', 1)[0]}.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Could not extract any text from the file. Please try another file.")

with tab2:
    st.subheader("Generate AI Text then Humanize")
    st.markdown("Describe what you want written. The app will generate it with AI, then immediately humanize it.")

    col_a, col_b = st.columns([3, 1])
    with col_a:
        topic = st.text_area(
            "What should the text be about?",
            placeholder="e.g. The impact of social media on mental health in teenagers",
            height=100,
        )
    with col_b:
        content_type = st.selectbox(
            "Content type",
            ["Essay", "Blog post", "Email", "Report", "Article", "Cover letter", "Summary"],
        )
        target_words = st.number_input("Target word count", min_value=50, max_value=2000, value=300, step=50)

    if st.button("🚀 Generate & Humanize", type="primary", use_container_width=True, disabled=not topic.strip(), key="gen_humanize"):
        try:
            with st.spinner("Step 1/2 — Generating AI text..."):
                gen_prompt = build_generate_prompt(topic, target_words, content_type.lower())
                ai_text = generate_text(gen_prompt, api_key)

            st.success("✅ AI text generated")

            with st.spinner("Step 2/2 — Humanizing..."):
                humanize_prompt = build_humanize_prompt(ai_text, humanize_strength, writing_style)
                humanized_text = generate_text(humanize_prompt, api_key)

            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**AI-Generated (raw)**")
                st.text_area("ai_raw", ai_text, height=400, label_visibility="collapsed")
            with col2:
                st.markdown("**Humanized Version ✨**")
                st.text_area("humanized_gen", humanized_text, height=400, label_visibility="collapsed")

            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button(
                    "⬇️ Download AI Version",
                    data=ai_text,
                    file_name="ai_generated.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with col_dl2:
                st.download_button(
                    "⬇️ Download Humanized Version",
                    data=humanized_text,
                    file_name="humanized_text.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

        except Exception as e:
            err = str(e)
            if "API_KEY_INVALID" in err or "invalid" in err.lower():
                st.error("❌ Invalid API key. Please check your Gemini API key in the sidebar.")
            elif "quota" in err.lower() or "429" in err:
                st.error("❌ API quota exceeded. Please wait a moment and try again, or check your Gemini usage limits.")
            else:
                st.error(f"❌ Error: {err}")

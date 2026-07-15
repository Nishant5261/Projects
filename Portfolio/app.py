import streamlit as st

import smtplib
import re
import os
import base64
import html as _html
from urllib.parse import quote as _url_quote
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from links import LINKS
from styles import render_css
from scripts import PAGE_SCRIPT

# GitHub data helpers (portfolio/github_data.py)
try:
    from github_data import fetch_projects_github, fetch_certs_github as _fetch_certs_gh
except Exception:
    def fetch_projects_github(max_count=20): return None
    def _fetch_certs_gh(): return None

@st.cache_data(ttl=3600, show_spinner=False)
def _load_gh_projects():
    return fetch_projects_github(max_count=20)

@st.cache_data(ttl=3600, show_spinner=False)
def _load_gh_certs():
    return _fetch_certs_gh()

# Resolve assets relative to this file so they work from any working directory.
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_ASSET_DIR = os.path.join(_BASE_DIR, "attached_assets")
_PORTRAIT_FILE = os.path.join(_ASSET_DIR, "portrait_1784056692141.png")
_PAGE_ICON_FILE = os.path.join(_ASSET_DIR, "portfolio.png")

# ─── Load hero portrait (background-removed PNG → base64) ───
try:
    with open(_PORTRAIT_FILE, "rb") as _pf:
        _portrait_b64 = "data:image/png;base64," + base64.b64encode(_pf.read()).decode()
except Exception:
    _portrait_b64 = ""

# ─────────────────────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nishant Giri | Portfolio",
    page_icon=_PAGE_ICON_FILE,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────────────────────
if "contact_sent" not in st.session_state:
    st.session_state.contact_sent = False

# Theme driven entirely by ?theme= URL query param.
# The nav button changes the URL → page reloads → Python reads the new param.
_qp = st.query_params.get("theme", "")
if _qp in ("dark", "light"):
    st.session_state.theme = _qp
elif "theme" not in st.session_state:
    st.session_state.theme = "dark"

DARK = st.session_state.theme == "dark"

# ─────────────────────────────────────────────────────────────
# Theme Palette
#
# Colors live as CSS custom properties (--bg, --accent, ...) so the theme
# button can flip them instantly in the browser (just toggling a
# `data-theme` attribute on <html>) instead of round-tripping through a
# Streamlit rerun, which used to feel like a full page reload.
# `T` keeps the same keys as before but each value is now `var(--key)`, so
# every existing `{T['accent']}` usage (inline styles + the CSS block below)
# keeps working unchanged — it just resolves live via CSS instead of being
# baked in at render time.
# ─────────────────────────────────────────────────────────────
THEME_DARK = {
    "bg":           "#0d1117",
    "bg2":          "#161b22",
    "card":         "#1c2333",
    "card2":        "#21262d",
    "text":         "#e6edf3",
    "text2":        "#b0bec5",
    "muted":        "#7d8590",
    "accent":       "#79c0ff",
    "accent2":      "#d2a8ff",
    "accent3":      "#56d364",
    "border":       "#30363d",
    "border2":      "#21262d",
    "tag_bg":       "#1f2d3d",
    "tag_text":     "#79c0ff",
    "badge_bg":     "#21262d",
    "badge_text":   "#7d8590",
    "hero_grad":    "linear-gradient(135deg,#0d1117 0%,#161b22 50%,#0d1117 100%)",
    "cert_border":  "#30363d",
    "view_link":    "#79c0ff",
    "input_bg":     "#1c2333",
    "nav_bg":       "rgba(13,17,23,0.92)",
    "shadow":       "0 8px 32px rgba(0,0,0,0.5)",
    "shadow2":      "0 2px 8px rgba(0,0,0,0.3)",
    "glow":         "rgba(121,192,255,0.15)",
    "nav_link":     "#e6edf3",
    "nav_muted":    "#7d8590",
    "gh_icon":      "#e6edf3",
}
THEME_LIGHT = {
    "bg":           "#f0f4f8",
    "bg2":          "#e8edf5",
    "card":         "#ffffff",
    "card2":        "#f6f8fa",
    "text":         "#1a202c",
    "text2":        "#4a5568",
    "muted":        "#718096",
    "accent":       "#4f46e5",
    "accent2":      "#7c3aed",
    "accent3":      "#059669",
    "border":       "#d1d5db",
    "border2":      "#e5e7eb",
    "tag_bg":       "#ede9fe",
    "tag_text":     "#5b21b6",
    "badge_bg":     "#f3f4f6",
    "badge_text":   "#374151",
    "hero_grad":    "linear-gradient(135deg,#f0f4f8 0%,#e8edf5 50%,#eef2ff 100%)",
    "cert_border":  "#ddd6fe",
    "view_link":    "#4f46e5",
    "input_bg":     "#ffffff",
    "nav_bg":       "rgba(240,244,248,0.92)",
    "shadow":       "0 8px 32px rgba(0,0,0,0.12)",
    "shadow2":      "0 2px 8px rgba(0,0,0,0.08)",
    "glow":         "rgba(79,70,229,0.1)",
    "nav_link":     "#1a202c",
    "nav_muted":    "#6b7280",
    "gh_icon":      "#24292e",
}

T = {k: f"var(--{k})" for k in THEME_DARK}
T["toggle_icon"] = "☀️" if DARK else "🌙"

# Keys that get an alpha channel spliced onto their hex value elsewhere in
# this file (e.g. f"{T['accent']}33" for a translucent glow). A CSS var
# can't have hex digits appended to it, so these also get an "-rgb" triplet
# variable, and TA() below builds an rgba() call against it instead.
_RGB_KEYS = ["accent", "accent2", "accent3", "border", "card", "tag_bg"]

def _hex_to_rgb(hexstr):
    h = hexstr.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def TA(key, hex_alpha):
    """Translucent color: var(--{key}-rgb) combined with a hex alpha byte."""
    alpha = round(int(hex_alpha, 16) / 255, 3)
    return f"rgba(var(--{key}-rgb), {alpha})"

def _css_vars(theme):
    lines = [f"  --{k}: {v};" for k, v in theme.items()]
    for k in _RGB_KEYS:
        r, g, b = _hex_to_rgb(theme[k])
        lines.append(f"  --{k}-rgb: {r},{g},{b};")
    return "\n".join(lines)

_ACTIVE_THEME = THEME_DARK if DARK else THEME_LIGHT
_CSS_VARS_ACTIVE = _css_vars(_ACTIVE_THEME)
_CSS_VARS_DARK   = _css_vars(THEME_DARK)
_CSS_VARS_LIGHT  = _css_vars(THEME_LIGHT)

# ─────────────────────────────────────────────────────────────
# Devicon helper
# ─────────────────────────────────────────────────────────────
DEVICON = "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons"

def dicon(name, variant="original"):
    return f"{DEVICON}/{name}/{name}-{variant}.svg"

# ─────────────────────────────────────────────────────────────
# CSS + Keyframe Animations
# ─────────────────────────────────────────────────────────────
st.markdown(render_css(T, TA, _CSS_VARS_ACTIVE, _CSS_VARS_DARK, _CSS_VARS_LIGHT), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Navigation Bar — all HTML, theme button inside nav
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<nav class="nav-bar" id="nav-bar">
  <a href="#home" class="nav-brand" data-text="Nishant Giri">Nishant Giri</a>
  <div class="nav-links">
    <a href="#home"           class="nav-link" data-section="home">Home</a>
    <a href="#skills"         class="nav-link" data-section="skills">Skills</a>
    <a href="#portfolio"      class="nav-link" data-section="portfolio">Portfolio</a>
    <a href="#certifications" class="nav-link" data-section="certifications">Certifications</a>
    <a href="#contact"        class="nav-link" data-section="contact">Contact</a>
    <button class="nav-theme-btn" id="nav-theme-btn" title="Switch theme" aria-label="Toggle theme">{T['toggle_icon']}</button>
  </div>
</nav>
""", unsafe_allow_html=True)

# Progress strip — fixed just below the nav, outside the nav element
st.markdown("""
<div class="progress-strip" id="progress-strip">
  <div class="scifi-bar-track" id="scifi-bar-track">
    <div class="scifi-bar-fill" id="scifi-bar-fill"></div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# ══ SECTION: HOME ══
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<section class="page-section" id="home" style="background:{T['hero_grad']};padding:0;border:none;">
  <div class="hero">
    <div class="hero-orb-1"></div>
    <div class="hero-orb-2"></div>
    <div class="hero-orb-3"></div>
    <div class="hero-inner">
    <div class="hero-content">
      <div class="hero-badge">
        <span class="hero-badge-dot"></span>
        Open to Opportunities
      </div>
      <h1>Hey, I'm <span class="name-gradient">Nishant Giri</span> 👋</h1>
      <div class="hero-subtitle">
        <span>CS Student</span>
        <span class="dot">·</span>
        <span>AI/ML Developer</span>
        <span class="dot">·</span>
        <span>Python Engineer</span>
      </div>
      <div class="hero-typed-wrap">
        <span id="typed-text" class="hero-typed"></span>
      </div>
      <div class="tagline-box">
        <i class="fas fa-quote-left"></i>
        Code is not just about making things work — it's about making things matter.
      </div>
      <div class="social-links">
        <a class="social-pill" href="{LINKS['linkedin']}" target="_blank">
          <i class="fab fa-linkedin" style="color:#0A66C2;"></i> LinkedIn
        </a>
        <a class="social-pill" href="{LINKS['github']}" target="_blank">
          <i class="fab fa-github" style="color:{T['gh_icon']};"></i> GitHub
        </a>
        <a class="social-pill" href="{LINKS['instagram']}" target="_blank">
          <i class="fab fa-instagram" style="color:#E1306C;"></i> Instagram
        </a>
        <a class="social-pill" href="{LINKS['resume']}" target="_blank">
          <i class="fas fa-file-alt" style="color:{T['muted']};"></i> Resume
        </a>
      </div>
    </div>
    <div class="hero-portrait-wrap">
      <div class="hero-portrait-glow"></div>
      <img class="hero-portrait-img" src="{_portrait_b64}" alt="Nishant Giri">
    </div>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# ── Stats + About ──
st.markdown(f'<section class="page-section" id="about" style="background:{T["bg"]};">', unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
stats = [("4+","Projects Built"),("6+","Technologies"),("1","Hackathon Award"),("2+","Years Coding")]
for col, (num, label), idx in zip([s1,s2,s3,s4], stats, range(4)):
    with col:
        st.markdown(f'<div class="stat-box reveal stagger-{idx+1}"><span class="stat-num">{num}</span><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_a, col_e = st.columns([1.1, 1], gap="large")
with col_a:
    st.markdown(f"""
    <div class="reveal-left">
      <div class="section-title" style="text-align:left;font-size:1.6rem;">About Me</div>
      <div class="accent-line-left"></div>
      <p class="about-text">I'm <strong>Nishant Giri</strong>, a second-year Computer Science student at the
      <strong>Institute of Engineering & Technology, Lucknow</strong>, with a genuine passion for building
      intelligent systems that solve real-world problems.</p>
      <p class="about-text">My journey has been shaped by a love for Python and Machine Learning — from crafting
      an <strong>AI-powered Interview Assistant</strong> using the OpenAI API to building a
      <strong>Fantasy Cricket Team Generator</strong> that applies ML to sports analytics.</p>
      <p class="about-text">Beyond coding, I've developed leadership skills as the
      <strong>Finance Head of TEDxLucknow</strong>, managing budgets for a large-scale collegiate event.
      I believe great engineers communicate, collaborate, and deliver real impact — not just clean code.</p>
      <p class="about-text">Currently seeking opportunities to grow at the intersection of
      <strong>data science, automation, and AI</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

with col_e:
    st.markdown(f"""
    <div class="reveal-right">
      <div class="section-title" style="text-align:left;font-size:1.5rem;">Education</div>
      <div class="accent-line-left"></div>
      <div class="timeline-item">
        <div class="timeline-dot">🎓</div>
        <div>
          <div class="timeline-title">B.Tech — Computer Science</div>
          <div class="timeline-org">Institute of Engineering & Technology, Lucknow</div>
          <div class="timeline-date"><i class="fas fa-calendar-alt" style="color:{T['muted']};font-size:0.7rem;"></i>&nbsp; Sep 2023 — Present</div>
          <div class="timeline-desc">Full-time B.Tech in CS focusing on algorithms, data structures,
          machine learning, and software engineering.</div>
        </div>
      </div>

      <div class="section-title" style="text-align:left;font-size:1.5rem;margin-top:1.75rem;">Experience</div>
      <div class="accent-line-left"></div>
      <div class="timeline-item">
        <div class="timeline-dot">💼</div>
        <div>
          <div class="timeline-title">Finance Head</div>
          <div class="timeline-org">TEDxLucknow</div>
          <div class="timeline-date"><i class="fas fa-calendar-alt" style="color:{T['muted']};font-size:0.7rem;"></i>&nbsp; November 2025 · Lucknow, India</div>
          <div class="timeline-desc">Spearheaded financial planning and budget management for a
          large-scale collegiate TEDx event. Coordinated with sponsors and managed end-to-end
          expense tracking for 500+ attendees.</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div class="reveal" style="max-width:700px;margin:0 auto;">
  <div class="section-title" style="text-align:left;font-size:1.5rem;">Achievements</div>
  <div class="accent-line-left"></div>
  <div class="achievement">
    <div class="achievement-icon">🥈</div>
    <div>
      <div class="achievement-title">Runner-up — College Level Hackathon</div>
      <div class="achievement-detail">Built a functional AI solution under a tight deadline, competing against 40+ teams. December 2024.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


st.markdown("</section>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ══ SECTION: SKILLS ══
# ─────────────────────────────────────────────────────────────
DI = DEVICON

# Skill data: (label, icon_html)
lang_chips = [
    ("Python",       f'<img src="{DI}/python/python-original.svg">'),
    ("C++",          f'<img src="{DI}/cplusplus/cplusplus-original.svg">'),
    ("C",            f'<img src="{DI}/c/c-original.svg">'),
    ("MySQL / SQL",  f'<img src="{DI}/mysql/mysql-original.svg">'),
    ("HTML5",        f'<img src="{DI}/html5/html5-original.svg">'),
    ("CSS3",         f'<img src="{DI}/css3/css3-original.svg">'),
]
lib_chips = [
    ("Pandas",       f'<img src="{DI}/pandas/pandas-original.svg">'),
    ("NumPy",        f'<img src="{DI}/numpy/numpy-original.svg">'),
    ("Scikit-learn", f'<img src="{DI}/scikitlearn/scikitlearn-original.svg">'),
    ("Matplotlib",   f'<img src="{DI}/matplotlib/matplotlib-original.svg">'),
    ("Streamlit",    f'<img src="{DI}/streamlit/streamlit-original.svg">'),
    ("OpenAI API",   f'<img src="{DI}/openai/openai-original-wordmark.svg">'),
]
tool_chips = [
    ("VS Code",      f'<img src="{DI}/vscode/vscode-original.svg">'),
    ("PyCharm",      f'<img src="{DI}/pycharm/pycharm-original.svg">'),
    ("Jupyter",      f'<img src="{DI}/jupyter/jupyter-original.svg">'),
    ("IntelliJ IDEA",f'<img src="{DI}/intellij/intellij-original.svg">'),
    ("Git",          f'<img src="{DI}/git/git-original.svg">'),
    ("Power BI",     f'<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/powerbi/powerbi-original.svg">'),
    ("Excel",        f'<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/excel/excel-original.svg">'),
]
db_chips = [
    ("MySQL",        f'<img src="{DI}/mysql/mysql-original.svg">'),
]

def make_chips(chips, extra_class="skill-chip"):
    parts = []
    for i, (name, icon) in enumerate(chips):
        parts.append(f'<div class="{extra_class} reveal-scale stagger-{(i%8)+1}">{icon}{name}</div>')
    return "".join(parts)

st.markdown(f"""
<section class="page-section" id="skills" style="background:{T['bg2']};">
  <div class="section-header">
    <div class="section-eyebrow reveal"><i class="fas fa-code"></i>&nbsp; Toolkit</div>
    <div class="section-title reveal">Skills & Technologies</div>
    <div class="section-sub reveal">Tools, languages, and frameworks I work with</div>
    <div class="accent-line reveal"></div>
  </div>
""", unsafe_allow_html=True)

sk1, sk2 = st.columns(2, gap="large")
with sk1:
    chips_lang = make_chips(lang_chips)
    chips_db   = make_chips(db_chips)
    st.markdown(f"""
    <div class="skill-section-card reveal-left">
      <div class="skills-category-label"><i class="fas fa-terminal"></i>&nbsp; Programming Languages</div>
      <div class="skill-chip-grid">{chips_lang}</div>
      <div class="skills-category-label"><i class="fas fa-database"></i>&nbsp; Databases</div>
      <div class="skill-chip-grid">{chips_db}</div>
    </div>
    """, unsafe_allow_html=True)

with sk2:
    chips_lib  = make_chips(lib_chips)
    chips_tool = make_chips(tool_chips, "skill-chip tools-chip")
    st.markdown(f"""
    <div class="skill-section-card reveal-right">
      <div class="skills-category-label"><i class="fas fa-cubes"></i>&nbsp; Libraries & Frameworks</div>
      <div class="skill-chip-grid">{chips_lib}</div>
      <div class="skills-category-label"><i class="fas fa-tools"></i>&nbsp; Tools & Platforms</div>
      <div class="skill-chip-grid">{chips_tool}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</section>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ══ SECTION: PORTFOLIO  (GitHub-fetched, horizontal scroll)
# ─────────────────────────────────────────────────────────────
_FALLBACK_PROJECTS = [
    {"title":"AI Interview Assistant",
     "desc":"Interactive web app that conducts automated technical interviews using the OpenAI API with real-time grading, instant feedback, and detailed performance reports.",
     "tech":["Python","OpenAI API","Streamlit","NLP"],
     "img":"https://placehold.co/600x300/6366f1/ffffff?text=AI+Interview+Assistant",
     "preview":"https://github.com","source":"https://github.com","stars":0},
    {"title":"Fantasy Cricket Generator",
     "desc":"ML model generating optimal fantasy cricket lineups with ~80% accuracy by analysing player performance data via Scikit-learn classifiers.",
     "tech":["Python","Scikit-learn","Pandas","Excel","ML"],
     "img":"https://placehold.co/600x300/0ea5e9/ffffff?text=Fantasy+Cricket+Generator",
     "preview":"https://github.com","source":"https://github.com","stars":0},
    {"title":"School ERP System",
     "desc":"Desktop application for educational management with role-based access control, handling attendance, grades, fee management, and reporting for 3 user roles.",
     "tech":["Python","MySQL","Tkinter","Role-Based Auth"],
     "img":"https://placehold.co/600x300/10b981/ffffff?text=School+ERP+System",
     "preview":"https://github.com","source":"https://github.com","stars":0},
    {"title":"4-Step Cryptographic Tool",
     "desc":"Custom encryption/decryption tool built on a proprietary 4-step algorithm producing unique 256-character ciphertext for any input.",
     "tech":["Python","Cryptography","Algorithm Design"],
     "img":"https://placehold.co/600x300/f59e0b/ffffff?text=Cryptographic+Tool",
     "preview":"https://github.com","source":"https://github.com","stars":0},
]

_gh_projects    = _load_gh_projects()
_gh_proj_live   = _gh_projects is not None
_all_projects   = _gh_projects if _gh_proj_live else _FALLBACK_PROJECTS

# Build all project card HTML as a single string
_proj_items_html = ""
for _pi, _p in enumerate(_all_projects):
    _safe_title = _html.escape(_p['title'])
    _safe_desc  = _html.escape(_p['desc'])
    _safe_img_alt = _html.escape(_p['title'], quote=True)
    _ph_text = _url_quote(_p['title'])
    _th = "".join(f'<span class="tech-tag">{_html.escape(t)}</span>' for t in _p.get("tech", ["Code"]))
    _st = f"stagger-{(_pi % 6) + 1}"
    _stars_html = (f'<span class="proj-stars"><i class="fas fa-star"></i> {_p["stars"]}</span>'
                   if _p.get("stars", 0) > 0 else "")
    _role_html = (
        f'<div class="proj-role"><i class="fas fa-user-tie"></i>&nbsp;{_html.escape(_p["role"])}</div>'
        if _p.get("role") else ""
    )
    _preview_label = (
        '<i class="fas fa-external-link-alt"></i> Live Preview'
        if _p.get("has_live") else
        '<i class="fas fa-external-link-alt"></i> Preview'
    )
    _proj_items_html += (
        f'<div class="proj-scroll-item reveal {_st}">'
        '<div class="proj-card">'
        # ── FRONT: image (cropped tight, no wasted space) + title + tech list ──
        '<div class="proj-face">'
        f'<img class="proj-face-bg" src="{_p["img"]}" alt="{_safe_img_alt}" loading="lazy"'
        f' onerror="this.src=\'https://placehold.co/600x300/30363d/7d8590?text={_ph_text}\'">'
        '<div class="proj-face-content">'
        f'<div class="proj-title">{_safe_title} {_stars_html}</div>'
        f'{_role_html}'
        f'<div class="proj-tech">{_th}</div>'
        '</div>'
        '</div>'
        # ── BACK: revealed on flip — description + preview/source links ──
        '<div class="proj-extra">'
        f'<p class="proj-desc">{_safe_desc}</p>'
        '<div class="proj-footer">'
        f'<a class="btn-primary" href="{_p["preview"]}" target="_blank">{_preview_label}</a>'
        f'<a class="btn-secondary" href="{_p["source"]}" target="_blank">'
        '<i class="fab fa-github"></i> Source</a>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    )

_proj_badge_html = (
    f'<i class="fab fa-github"></i>&nbsp; {len(_all_projects)} repos · live from GitHub'
    if _gh_proj_live else
    '<i class="fas fa-code"></i>&nbsp; Featured projects'
)

st.markdown(f"""
<section class="page-section" id="portfolio" style="background:{T['bg']};">
  <div class="section-header">
    <div class="section-eyebrow reveal"><i class="fas fa-layer-group"></i>&nbsp; Work</div>
    <div class="section-title reveal">Projects</div>
    <div class="section-sub reveal">Things I've built and shipped</div>
    <div class="gh-source-badge reveal">{_proj_badge_html}</div>
  </div>
  <div class="scroll-controls">
    <button class="scroll-arrow-btn" data-track="proj-track" data-dir="-1" title="Scroll left">&#8249;</button>
    <button class="scroll-arrow-btn" data-track="proj-track" data-dir="1" title="Scroll right">&#8250;</button>
  </div>
  <div class="horiz-scroll-track" id="proj-track">
    {_proj_items_html}
  </div>
</section>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ══ SECTION: CERTIFICATIONS  (GitHub-fetched, horizontal scroll)
# ─────────────────────────────────────────────────────────────
_FALLBACK_CERTS = [
    {"logo_html": f'<img src="{DI}/python/python-original.svg" width="28">',
     "logo_bg": "#3776ab22", "name": "Python for Everybody Specialization",
     "issuer": "University of Michigan · Coursera", "status": "Certified",
     "badge": "https://placehold.co/80x80/3776ab/ffffff?text=PY",
     "link": "#", "featured": True},
    {"logo_html": '<i class="fas fa-chart-bar" style="color:#0f62fe;font-size:1.5rem;"></i>',
     "logo_bg": "#0f62fe11", "name": "Data Analysis with Python",
     "issuer": "IBM · Coursera", "status": "Certified",
     "badge": "https://placehold.co/80x80/0f62fe/ffffff?text=IBM",
     "link": "#", "featured": False},
    {"logo_html": f'<img src="{DI}/scikitlearn/scikitlearn-original.svg" width="28">',
     "logo_bg": "#6366f122", "name": "Machine Learning Specialization",
     "issuer": "Stanford / Andrew Ng · Coursera", "status": "Certified",
     "badge": "https://placehold.co/80x80/6366f1/ffffff?text=ML",
     "link": "#", "featured": True},
    {"logo_html": f'<img src="{DI}/mysql/mysql-original.svg" width="28">',
     "logo_bg": "#0ea5e922", "name": "SQL for Data Science",
     "issuer": "UC Davis · Coursera", "status": "Certified",
     "badge": "https://placehold.co/80x80/0ea5e9/ffffff?text=SQL",
     "link": "#", "featured": False},
    {"logo_html": '<i class="fab fa-microsoft" style="color:#00a4ef;font-size:1.5rem;"></i>',
     "logo_bg": "#00a4ef11", "name": "Power BI for Business Intelligence",
     "issuer": "Microsoft · Microsoft Learn", "status": "Certified",
     "badge": "https://placehold.co/80x80/00a4ef/ffffff?text=MS",
     "link": "#", "featured": False},
    {"logo_html": '<i class="fas fa-shield-alt" style="color:#1ba0d7;font-size:1.5rem;"></i>',
     "logo_bg": "#1ba0d722", "name": "Introduction to Cybersecurity",
     "issuer": "Cisco · Cisco Networking Academy", "status": "Certified",
     "badge": "https://placehold.co/80x80/1ba0d7/ffffff?text=CISCO",
     "link": "#", "featured": False},
]

_gh_certs   = _load_gh_certs()
_gh_cert_live = _gh_certs is not None

def _normalise_cert(c):
    """Accept both GitHub JSON format and fallback format."""
    return {
        "logo_html": c.get("logo_html", '<i class="fas fa-certificate" style="color:#79c0ff;font-size:1.5rem;"></i>'),
        "logo_bg":   c.get("logo_bg", "#79c0ff11"),
        "name":      c.get("name", "Certificate"),
        "issuer":    c.get("issuer", ""),
        "status":    c.get("status", "Certified"),
        "badge":     c.get("badge", "https://placehold.co/80x80/21262d/7d8590?text=CERT"),
        "link":      c.get("link", "#"),
        "raw_url":   c.get("raw_url", c.get("link", "#")),
        "featured":  bool(c.get("featured", False)),
    }

_all_certs = [_normalise_cert(c) for c in (_gh_certs if _gh_cert_live else _FALLBACK_CERTS)]

_cert_items_html = ""
for _ci, _c in enumerate(_all_certs):
    _fc  = "cert-card featured" if _c["featured"] else "cert-card"
    _cst = f"stagger-{(_ci % 6) + 1}"
    _cert_items_html += (
        '<div class="cert-scroll-item">'
        f'<div class="{_fc} reveal {_cst}">'
        f'<img class="cert-badge-img" src="{_c["badge"]}" alt="badge"'
        ' onerror="this.style.display=\'none\'">'
        '<div class="cert-header">'
        f'<div class="cert-issuer-logo" style="background:{_c["logo_bg"]};">{_c["logo_html"]}</div>'
        '</div>'
        f'<div class="cert-name">{_html.escape(_c["name"])}</div>'
        f'<div class="cert-issuer">{_html.escape(_c["issuer"])}</div>'
        f'<div class="cert-status">{_html.escape(_c["status"])}</div>'
        f'<button class="view-cert" data-url="{_html.escape(_c["raw_url"])}" '
        f'data-name="{_html.escape(_c["name"])}" '
        '>'
        'View Certificate &nbsp;<i class="fas fa-arrow-right"></i>'
        '</button>'
        '</div>'
        '</div>'
    )

_cert_badge_html = (
    f'<i class="fab fa-github"></i>&nbsp; {len(_all_certs)} certs · live from GitHub'
    if _gh_cert_live else
    '<i class="fas fa-certificate"></i>&nbsp; Verified credentials'
)

st.markdown(f"""
<section class="page-section" id="certifications" style="background:{T['bg2']};">
  <div class="section-header">
    <div class="section-eyebrow reveal"><i class="fas fa-certificate"></i>&nbsp; Credentials</div>
    <div class="section-title reveal">Certifications</div>
    <div class="section-sub reveal">Courses completed &amp; skills validated</div>
    <div class="gh-source-badge reveal">{_cert_badge_html}</div>
  </div>
  <div class="scroll-controls">
    <button class="scroll-arrow-btn" data-track="cert-track" data-dir="-1" title="Scroll left">&#8249;</button>
    <button class="scroll-arrow-btn" data-track="cert-track" data-dir="1" title="Scroll right">&#8250;</button>
  </div>
  <div class="horiz-scroll-track" id="cert-track">
    {_cert_items_html}
  </div>
  <br>
  <div class="reveal" style="text-align:center;">
    <div style="display:inline-block;background:{T['tag_bg']};border:1px solid {TA('accent','33')};
         border-radius:12px;padding:0.9rem 1.75rem;color:{T['text2']};font-size:0.875rem;">
      📌 <strong style="color:{T['text']};">Always Learning</strong> — new courses in progress!
    </div>
  </div>
</section>

<!-- ═══ CERTIFICATE MODAL OVERLAY ═══ -->
<div id="cert-modal" class="cert-modal-overlay">
  <div class="cert-modal-box">
    <div class="cert-modal-header">
      <span class="cert-modal-title" id="cert-modal-title">Certificate</span>
      <button class="cert-modal-close" id="cert-modal-close" title="Close">✕</button>
    </div>
    <div class="cert-modal-body">
      <div class="cert-modal-loading" id="cert-modal-loading">
        <i class="fas fa-spinner fa-spin" style="font-size:1.5rem;"></i>
        Loading certificate…
      </div>
      <iframe id="cert-modal-iframe" src="">
      </iframe>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ══ SECTION: CONTACT ══
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<section class="page-section" id="contact" style="background:{T['bg']};">
  <div class="section-header">
    <div class="section-eyebrow reveal"><i class="fas fa-paper-plane"></i>&nbsp; Say Hello</div>
    <div class="section-title reveal">Get In Touch</div>
    <div class="section-sub reveal">Fill out the form and I'll get back to you soon</div>
    <div class="accent-line reveal"></div>
  </div>
""", unsafe_allow_html=True)

col_form, col_info = st.columns([1.4, 1], gap="large")

with col_form:
    if st.session_state.contact_sent:
        st.markdown(f"""
        <div class="reveal" style="background:{T['tag_bg']};border:2px solid {T['accent']};border-radius:20px;
             padding:3rem 2rem;text-align:center;animation:bounceIn 0.6s ease;">
          <div style="font-size:3.5rem;margin-bottom:1rem;animation:float 3s ease-in-out infinite;">✅</div>
          <div style="font-size:1.3rem;font-weight:800;color:{T['text']};margin-bottom:0.6rem;
               font-family:'Space Grotesk',sans-serif;">Message Sent!</div>
          <div style="color:{T['text2']};font-size:0.9rem;">Thank you for reaching out.
          I'll respond within 24 hours.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("↩  Send Another Message"):
            st.session_state.contact_sent = False
            st.rerun()
    else:
        with st.form("contact_form", clear_on_submit=True):
            name         = st.text_input("Your Name *",  placeholder="John Doe")
            email_input  = st.text_input("Your Email *", placeholder="john@example.com")
            subject      = st.text_input("Subject *",    placeholder="Project Collaboration / Opportunity")
            message      = st.text_area("Message *",     placeholder="Write your message here...", height=150)
            submitted    = st.form_submit_button("📨  Send Message", use_container_width=True)

        if submitted:
            if not name or not email_input or not subject or not message:
                st.error("Please fill in all fields.")
            elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_input):
                st.error("Please enter a valid email address.")
            else:
                try:
                    RECIPIENT   = "girinishant708@gmail.com"
                    sender_pass = os.environ.get("GMAIL_APP_PASSWORD", "")
                    if sender_pass:
                        msg = MIMEMultipart()
                        msg["From"]    = RECIPIENT
                        msg["To"]      = RECIPIENT
                        msg["Subject"] = f"[Portfolio] {subject} — from {name}"
                        body = f"Name: {name}\nEmail: {email_input}\n\nMessage:\n{message}"
                        msg.attach(MIMEText(body, "plain"))
                        with smtplib.SMTP("smtp.gmail.com", 587) as srv:
                            srv.starttls()
                            srv.login(RECIPIENT, sender_pass)
                            srv.sendmail(RECIPIENT, RECIPIENT, msg.as_string())
                except Exception:
                    pass
                st.session_state.contact_sent = True
                st.rerun()

with col_info:
    st.markdown(f"""
    <div class="reveal-right">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:1.3rem;font-weight:700;
           color:{T['text']};margin-bottom:0.4rem;">Let's Connect</div>
      <div class="accent-line-left"></div>
      <p class="about-text">I'm open to internship opportunities, project collaborations,
      and freelance work. Whether you have a question or just want to say hi — drop a message!</p>

      <div class="contact-info-card">
        <div class="contact-item">
          <i class="fab fa-linkedin" style="color:#0A66C2;"></i>
          <div class="contact-item-body">
            <div class="contact-label">LinkedIn</div>
          </div>
          <a href="{LINKS['linkedin']}" target="_blank" class="contact-visit-btn">
            View Profile <i class="fas fa-arrow-up-right-from-square"></i>
          </a>
        </div>
        <div class="contact-item">
          <i class="fab fa-github" style="color:{T['gh_icon']};"></i>
          <div class="contact-item-body">
            <div class="contact-label">GitHub</div>
          </div>
          <a href="{LINKS['github']}" target="_blank" class="contact-visit-btn">
            View Profile <i class="fas fa-arrow-up-right-from-square"></i>
          </a>
        </div>
        <div class="contact-item">
          <i class="fab fa-instagram" style="color:#E1306C;"></i>
          <div class="contact-item-body">
            <div class="contact-label">Instagram</div>
          </div>
          <a href="{LINKS['instagram']}" target="_blank" class="contact-visit-btn">
            View Profile <i class="fas fa-arrow-up-right-from-square"></i>
          </a>
        </div>
        <div class="contact-item">
          <i class="fas fa-map-marker-alt" style="color:#ef4444;"></i>
          <div class="contact-item-body">
            <div class="contact-label">Location</div>
            <span class="contact-val">Lucknow, Uttar Pradesh, India</span>
          </div>
        </div>
      </div>

      <div style="background:linear-gradient(135deg,{T['tag_bg']},{T['card']});
           border:1px solid {TA('accent','33')};border-radius:12px;
           padding:1rem 1.25rem;font-size:0.85rem;color:{T['text2']};">
        <i class="fas fa-clock" style="color:{T['accent']};"></i>
        &nbsp; Typical response: <strong style="color:{T['text']};">within 24 hours</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</section>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <div class="footer-links">
    <a class="footer-link-icon" href="{LINKS['linkedin']}" target="_blank" title="LinkedIn">
      <i class="fab fa-linkedin" style="color:#0A66C2;"></i>
    </a>
    <a class="footer-link-icon" href="{LINKS['github']}" target="_blank" title="GitHub">
      <i class="fab fa-github"></i>
    </a>
    <a class="footer-link-icon" href="{LINKS['instagram']}" target="_blank" title="Instagram">
      <i class="fab fa-instagram" style="color:#E1306C;"></i>
    </a>
  </div>
  Built with <span style="color:#ef4444;">♥</span> using <strong>Streamlit</strong> &nbsp;·&nbsp;
  <strong>Nishant Giri</strong> &copy; 2025
</div>

<!-- Back to top -->
<a href="#home" class="back-to-top" id="back-to-top" title="Back to top">
  <i class="fas fa-chevron-up"></i>
</a>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# JavaScript: Scroll effects, nav active, typing, particles
# Injected via st.html() so scripts actually execute.
# ─────────────────────────────────────────────────────────────
st.html(PAGE_SCRIPT, unsafe_allow_javascript=True)

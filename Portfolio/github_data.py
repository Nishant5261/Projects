"""
GitHub data fetcher for the portfolio.

Projects  → fetched dynamically on every reload from the 'Projects' repo.
            Uses Git Trees API + raw.githubusercontent.com with cache-busting
            so README and requirements.txt fetches never exhaust REST API limits.

Certs     → fetched dynamically as PDF files from the 'certificates' repo.
"""

import os
import re
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ──────────────────────────────────────────────
GITHUB_USERNAME  = "nishant5261"
PROJECTS_REPO    = "Projects"       # repo where each folder = one project
CERTS_REPO       = "certificates"   # repo where PDFs = certificates
# ──────────────────────────────────────────────

_SESSION = requests.Session()
_retry = Retry(
    total=2,
    backoff_factor=0.3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
_SESSION.mount("https://", HTTPAdapter(max_retries=_retry, pool_maxsize=16))
_SESSION.mount("http://", HTTPAdapter(max_retries=_retry, pool_maxsize=16))

_FALLBACK_PROJECTS = [
    {
        "title": "LEKH",
        "role": "AI Powered Text Humanizer",
        "desc": "LEKH is a Python program for humanizing AI text and generating natural-sounding content on specific topics.",
        "tech": ["Python", "Streamlit", "Google.generativeai", "PyPDF2"],
        "img": "https://placehold.co/600x300/ec4899/ffffff?text=LEKH",
        "preview": "https://github.com/Nishant5261/Projects/tree/main/Lekh-AI%20powered%20Text%20humanizer",
        "source": "https://github.com/Nishant5261/Projects/tree/main/Lekh-AI%20powered%20Text%20humanizer",
        "stars": 0,
        "has_live": False,
    },
    {
        "title": "Portfolio",
        "role": "My portfolio website",
        "desc": "A Streamlit-based portfolio website that highlights my journey, projects, certifications, and contact details.",
        "tech": ["Python", "Streamlit", "Requests"],
        "img": "https://placehold.co/600x300/f59e0b/ffffff?text=Portfolio",
        "preview": "https://github.com/Nishant5261/Projects/tree/main/Portfolio",
        "source": "https://github.com/Nishant5261/Projects/tree/main/Portfolio",
        "stars": 0,
        "has_live": False,
    },
    {
        "title": "SHADOW",
        "role": "AI Powered Interview Assistant",
        "desc": "An AI-based interview assistant that creates a non-biased interview environment and gives feedback on answers.",
        "tech": ["Python", "Streamlit", "google.genai", "RegEx(re)"],
        "img": "https://placehold.co/600x300/14b8a6/ffffff?text=SHADOW",
        "preview": "https://github.com/Nishant5261/Projects/tree/main/Shadow-AI%20Interview%20System",
        "source": "https://github.com/Nishant5261/Projects/tree/main/Shadow-AI%20Interview%20System",
        "stars": 0,
        "has_live": False,
    },
    {
        "title": "SURVIVE",
        "role": "Web-based shooting game",
        "desc": "A browser-based shooting game where the player defends against incoming enemies and earns points by shooting them.",
        "tech": ["HTML", "Javascript", "GSAP(JS)", "Tailwind"],
        "img": "https://placehold.co/600x300/ef4444/ffffff?text=SURVIVE",
        "preview": "https://github.com/Nishant5261/Projects/tree/main/Survive",
        "source": "https://github.com/Nishant5261/Projects/tree/main/Survive",
        "stars": 0,
        "has_live": False,
    },
]

_FALLBACK_CERTS = [
    {
        "logo_html": '<i class="fas fa-book" style="color:#e61e28;font-size:1.5rem;"></i>',
        "logo_bg": "#e61e2811",
        "name": "English Level10Expert(CEFR: C2 GSE:85 90)",
        "issuer": "MeproPearson",
        "status": "Certified",
        "badge": "https://placehold.co/80x80/e61e28/ffffff?text=PR",
        "link": "https://github.com/Nishant5261/certificates/blob/main/English_Level10Expert(CEFR:%20C2_GSE:85-90)%20by%20MeproPearson.pdf",
        "raw_url": "https://raw.githubusercontent.com/Nishant5261/certificates/main/English_Level10Expert(CEFR:%20C2_GSE:85-90)%20by%20MeproPearson.pdf",
        "featured": False,
    },
    {
        "logo_html": '<i class="fas fa-chart-bar" style="color:#0f62fe;font-size:1.5rem;"></i>',
        "logo_bg": "#0f62fe11",
        "name": "SQL(basic)",
        "issuer": "IBM",
        "status": "Certified",
        "badge": "https://placehold.co/80x80/0f62fe/ffffff?text=IBM",
        "link": "https://github.com/Nishant5261/certificates/blob/main/SQL(basic)%20by%20IBM.pdf",
        "raw_url": "https://raw.githubusercontent.com/Nishant5261/certificates/main/SQL(basic)%20by%20IBM.pdf",
        "featured": False,
    },
    {
        "logo_html": '<i class="fab fa-python" style="color:#3776ab;font-size:1.5rem;"></i>',
        "logo_bg": "#3776ab11",
        "name": "Python basic certificate",
        "issuer": "",
        "status": "Certified",
        "badge": "https://placehold.co/80x80/3776ab/ffffff?text=PY",
        "link": "https://github.com/Nishant5261/certificates/blob/main/python_basic%20certificate.pdf",
        "raw_url": "https://raw.githubusercontent.com/Nishant5261/certificates/main/python_basic%20certificate.pdf",
        "featured": False,
    },
]

_EXT_TECH = {
    ".py":    "Python",
    ".ipynb": "Jupyter",
    ".js":    "JavaScript",
    ".ts":    "TypeScript",
    ".jsx":   "React",
    ".tsx":   "React",
    ".html":  "HTML",
    ".css":   "CSS",
    ".java":  "Java",
    ".cpp":   "C++",
    ".cc":    "C++",
    ".c":     "C",
    ".cs":    "C#",
    ".rs":    "Rust",
    ".go":    "Go",
    ".rb":    "Ruby",
    ".php":   "PHP",
    ".swift": "Swift",
    ".kt":    "Kotlin",
    ".r":     "R",
    ".sql":   "SQL",
    ".sh":    "Shell",
}
_FILE_TECH = {
    "requirements.txt": "Python",
    "package.json":     "Node.js",
    "cargo.toml":       "Rust",
    "go.mod":           "Go",
    "gemfile":          "Ruby",
    "pom.xml":          "Java",
}

_REQUIREMENTS_FRAMEWORKS = [
    ("tensorflow",    "TensorFlow"),
    ("torch",         "PyTorch"),
    ("keras",         "Keras"),
    ("transformers",  "HuggingFace"),
    ("langchain",     "LangChain"),
    ("google-generativeai", "Google GenAI"),
    ("google.generativeai", "Google GenAI"),
    ("google-genai",  "Google GenAI"),
    ("openai",        "OpenAI API"),
    ("anthropic",     "Anthropic"),
    ("sklearn",       "Scikit-learn"),
    ("scikit-learn",  "Scikit-learn"),
    ("xgboost",       "XGBoost"),
    ("lightgbm",      "LightGBM"),
    ("optuna",        "Optuna"),
    ("polars",        "Polars"),
    ("fastapi",       "FastAPI"),
    ("flask",         "Flask"),
    ("django",        "Django"),
    ("streamlit",     "Streamlit"),
    ("gradio",        "Gradio"),
    ("chainlit",      "Chainlit"),
    ("fasthtml",      "FastHTML"),
    ("numpy",         "NumPy"),
    ("pandas",        "Pandas"),
    ("matplotlib",    "Matplotlib"),
    ("seaborn",       "Seaborn"),
    ("plotly",        "Plotly"),
    ("cv2",           "OpenCV"),
    ("opencv",        "OpenCV"),
    ("PIL",           "Pillow"),
    ("pillow",        "Pillow"),
    ("pypdf2",        "PyPDF2"),
    ("pypdf",         "PyPDF"),
    ("sqlalchemy",    "SQLAlchemy"),
    ("pymysql",       "MySQL"),
    ("psycopg2",      "PostgreSQL"),
    ("pymongo",       "MongoDB"),
    ("redis",         "Redis"),
    ("celery",        "Celery"),
    ("pydantic",      "Pydantic"),
    ("httpx",         "HTTPX"),
    ("requests",      "Requests"),
    ("selenium",      "Selenium"),
    ("scrapy",        "Scrapy"),
    ("beautifulsoup4","BeautifulSoup"),
    ("bs4",           "BeautifulSoup"),
    ("nltk",          "NLTK"),
    ("spacy",         "spaCy"),
    ("gensim",        "Gensim"),
    ("sentence-transformers", "SentenceTransformers"),
    ("faiss",         "FAISS"),
    ("chromadb",      "ChromaDB"),
    ("pinecone",      "Pinecone"),
    ("networkx",      "NetworkX"),
    ("twilio",        "Twilio"),
    ("boto3",         "AWS SDK"),
    ("google-cloud",  "GCP"),
    ("azure",         "Azure"),
]


def _detect_frameworks_from_requirements(text):
    """Scan requirements.txt content and return a list of framework display labels."""
    text_lower = text.lower()
    seen, found = set(), []
    for pkg, label in _REQUIREMENTS_FRAMEWORKS:
        if label in seen:
            continue
        if re.search(r"(?:^|[^a-zA-Z0-9_-])" + re.escape(pkg.lower()), text_lower, re.MULTILINE):
            seen.add(label)
            found.append(label)
    return found


_PALETTE = ["6366f1", "0ea5e9", "10b981", "f59e0b", "ef4444", "8b5cf6", "ec4899", "14b8a6"]

_ISSUER_STYLE = {
    "ibm":        ('<i class="fas fa-chart-bar" style="color:#0f62fe;font-size:1.5rem;"></i>',   "#0f62fe11", "0f62fe", "IBM"),
    "google":     ('<i class="fab fa-google" style="color:#4285f4;font-size:1.5rem;"></i>',       "#4285f411", "4285f4", "GG"),
    "microsoft":  ('<i class="fab fa-microsoft" style="color:#00a4ef;font-size:1.5rem;"></i>',   "#00a4ef11", "00a4ef", "MS"),
    "coursera":   ('<i class="fas fa-graduation-cap" style="color:#0056d3;font-size:1.5rem;"></i>', "#0056d311", "0056d3", "CO"),
    "stanford":   ('<i class="fas fa-university" style="color:#8c1515;font-size:1.5rem;"></i>',  "#8c151511", "8c1515", "SU"),
    "cisco":      ('<i class="fas fa-network-wired" style="color:#1ba0d7;font-size:1.5rem;"></i>', "#1ba0d711", "1ba0d7", "CI"),
    "aws":        ('<i class="fab fa-aws" style="color:#ff9900;font-size:1.5rem;"></i>',           "#ff990011", "ff9900", "AWS"),
    "udemy":      ('<i class="fas fa-play-circle" style="color:#a435f0;font-size:1.5rem;"></i>',   "#a435f011", "a435f0", "UD"),
    "pearson":    ('<i class="fas fa-book" style="color:#e61e28;font-size:1.5rem;"></i>',          "#e61e2811", "e61e28", "PR"),
    "mepro":      ('<i class="fas fa-book" style="color:#e61e28;font-size:1.5rem;"></i>',          "#e61e2811", "e61e28", "PR"),
    "hackerrank": ('<i class="fab fa-hackerrank" style="color:#2ec866;font-size:1.5rem;"></i>',   "#2ec86611", "2ec866", "HR"),
}

_CERT_KEYWORD_STYLE = {
    "python":     ('<i class="fab fa-python" style="color:#3776ab;font-size:1.5rem;"></i>',      "#3776ab11", "3776ab", "PY"),
    "sql":        ('<i class="fas fa-database" style="color:#0ea5e9;font-size:1.5rem;"></i>',     "#0ea5e911", "0ea5e9", "SQL"),
    "javascript": ('<i class="fab fa-js" style="color:#f7df1e;font-size:1.5rem;"></i>',           "#f7df1e11", "f7df1e", "JS"),
    "machine learning": ('<i class="fas fa-brain" style="color:#6366f1;font-size:1.5rem;"></i>', "#6366f111", "6366f1", "ML"),
    "deep learning":    ('<i class="fas fa-brain" style="color:#8b5cf6;font-size:1.5rem;"></i>', "#8b5cf611", "8b5cf6", "DL"),
    "english":    ('<i class="fas fa-language" style="color:#10b981;font-size:1.5rem;"></i>',     "#10b98111", "10b981", "EN"),
    "data":       ('<i class="fas fa-chart-bar" style="color:#f59e0b;font-size:1.5rem;"></i>',    "#f59e0b11", "f59e0b", "DA"),
    "cyber":      ('<i class="fas fa-shield-alt" style="color:#1ba0d7;font-size:1.5rem;"></i>',   "#1ba0d711", "1ba0d7", "CY"),
    "security":   ('<i class="fas fa-shield-alt" style="color:#1ba0d7;font-size:1.5rem;"></i>',   "#1ba0d711", "1ba0d7", "CY"),
    "web":        ('<i class="fas fa-globe" style="color:#0ea5e9;font-size:1.5rem;"></i>',         "#0ea5e911", "0ea5e9", "WEB"),
    "ai":         ('<i class="fas fa-robot" style="color:#6366f1;font-size:1.5rem;"></i>',         "#6366f111", "6366f1", "AI"),
    "cloud":      ('<i class="fas fa-cloud" style="color:#0ea5e9;font-size:1.5rem;"></i>',         "#0ea5e911", "0ea5e9", "CL"),
}
_DEFAULT_CERT_STYLE = (
    '<i class="fas fa-certificate" style="color:#79c0ff;font-size:1.5rem;"></i>',
    "#79c0ff11", "79c0ff", "CERT"
)


# ─────────────────────────────────────────────────────────────
# Shared Helpers (Token + Cache-Busting)
# ─────────────────────────────────────────────────────────────

def _get_token():
    token=os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        try:
            import streamlit as st
            token = str(st.secrets.get("GITHUB_TOKEN", "")).strip()
        except Exception:
            token = 7 
    return token


def _headers(api=True):
    token = _get_token()
    h = {
        "User-Agent": "Nishant-Portfolio-App",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
    }
    if api:
        h["Accept"] = "application/vnd.github+json"
        h["X-GitHub-Api-Version"] = "2022-11-28"
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _get_json(url, params=None, timeout=8):
    """GET → parsed JSON with cache-busting timestamp, or None on error."""
    try:
        q = dict(params or {})
        q["_cb"] = int(time.time() * 1000)
        r = _SESSION.get(url, headers=_headers(api=True), params=q, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None


def _get_raw_text(repo: str, path: str, branch: str = "main", timeout=6):
    """Fetch raw file text from raw.githubusercontent.com (does not use REST API quota)."""
    try:
        safe_path = "/".join(requests.utils.quote(part) for part in path.split("/"))
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{repo}/{branch}/{safe_path}"
        r = _SESSION.get(
            raw_url,
            headers=_headers(api=False),
            params={"_cb": int(time.time() * 1000)},
            timeout=timeout,
        )
        if r.status_code == 200:
            return r.text
    except Exception:
        pass
    return None


def _load_local_portfolio_data():
    """Load data from the checked-in JSON file when available."""
    try:
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portfolio_data.json")
        with open(data_path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def _fetch_repo_tree_single_call(repo: str = PROJECTS_REPO, branch: str = "main"):
    """
    Fetch the entire repository file tree in ONE single GitHub API request.
    Falls back to /contents or public HTML parsing if rate-limited.
    Returns (dict_of_folders_to_filenames, is_live_bool).
    """
    # 1. Single-call Git Tree API (1 request for all folders & files)
    tree_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo}/git/trees/{branch}"
    data = _get_json(tree_url, params={"recursive": "1"})
    if data and isinstance(data.get("tree"), list):
        folders = {}
        for item in data["tree"]:
            path = item.get("path", "")
            itype = item.get("type", "")
            if not path or path.startswith("."):
                continue
            parts = path.split("/")
            top = parts[0]
            if len(parts) == 1 and itype == "tree":
                folders.setdefault(top, [])
            elif len(parts) >= 2 and top != ".devcontainer":
                folders.setdefault(top, [])
                if len(parts) == 2 and itype == "blob":
                    folders[top].append(parts[1])
        if folders:
            return folders, True

    # 2. Fallback to top-level /contents API
    contents_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo}/contents"
    items = _get_json(contents_url, params={"ref": branch})
    if isinstance(items, list):
        folders = {}
        for item in items:
            name = item.get("name", "")
            if item.get("type") == "dir" and name and name != ".devcontainer":
                folders[name] = []
        if folders:
            return folders, True

    # 3. Fallback to scraping public GitHub HTML page (0 API quota used)
    try:
        html_url = f"https://github.com/{GITHUB_USERNAME}/{repo}/tree/{branch}"
        r = _SESSION.get(
            html_url,
            headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"},
            params={"_cb": int(time.time() * 1000)},
            timeout=10,
        )
        if r.status_code == 200:
            pattern = rf'/{re.escape(GITHUB_USERNAME)}/{re.escape(repo)}/tree/{re.escape(branch)}/([^"?#/]+)'
            folders = {}
            for match in re.finditer(pattern, r.text):
                name = requests.utils.unquote(match.group(1)).strip()
                if name and name not in (".devcontainer", "readme.md", "README.md"):
                    folders.setdefault(name, [])
            if folders:
                return folders, True
    except Exception:
        pass

    return {}, False


# ─────────────────────────────────────────────────────────────
# Projects
# ─────────────────────────────────────────────────────────────

def _detect_tech_from_filenames(filenames):
    """Return a deduplicated list of tech labels inferred from filenames."""
    seen, out = set(), []
    for fname in filenames:
        name_lower = fname.lower()
        label = _FILE_TECH.get(name_lower)
        if not label:
            ext = os.path.splitext(name_lower)[1]
            label = _EXT_TECH.get(ext)
        if label and label not in seen:
            seen.add(label)
            out.append(label)
    return out[:6] or ["Code"]


def _extract_plain_desc(text):
    """Return the first meaningful paragraph from a README (fallback)."""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#") or line.startswith("![") or line.startswith("[!["):
            continue
        if line.startswith("<") or line.startswith("---"):
            continue
        clean = re.sub(r"\*{1,2}|_{1,2}|`", "", line)
        clean = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", clean)
        clean = clean.strip()
        if len(clean) > 20:
            return clean
    return ""


def _normalize_preview_url(value):
    """Normalize a preview URL so bare domains become clickable."""
    if not value:
        return value
    value = value.strip()
    if re.match(r"^(https?|mailto|tel):", value, re.IGNORECASE):
        return value
    if value.startswith("//"):
        return f"https:{value}"
    if re.match(r"^[a-z0-9.-]+\.[a-z]{2,}(?:/.*)?$", value, re.IGNORECASE):
        return f"https://{value}"
    return value


def _parse_readme_fields(text):
    """
    Parse structured fields from a README.
    Returns dict with keys: name, role, description, language, framework, live_preview
    """
    fields = {
        "name": "", "role": "", "description": "",
        "language": "", "framework": "", "live_preview": ""
    }

    pat = re.compile(
        r"^[-\*\s]*[\*_]{0,2}"
        r"(Name|Role|Description|Coding[\s_\-]?Language|Language|"
        r"Framework(?:[\s_\-]?Used)?|"
        r"Live[\s_\-]?Preview|Live\s+Link|Preview\s+Link|Demo|Website)"
        r"[\*_]{0,2}\s*[:\-]\s*(.*)",
        re.IGNORECASE
    )

    for line in text.splitlines():
        line_stripped = line.strip()
        m = pat.match(line_stripped)
        if not m:
            if re.search(r"^(live preview|live link|preview link|demo|website)\s*[:\-]\s*(.+)$", line_stripped, re.IGNORECASE):
                key_raw = "live_preview"
                raw_val = re.sub(r"^(live preview|live link|preview link|demo|website)\s*[:\-]\s*", "", line_stripped, flags=re.IGNORECASE)
            else:
                continue
        else:
            key_raw = m.group(1).lower()
            raw_val = m.group(2).strip()

        url_match = re.search(r"\[([^\]]*)\]\(([^)]+)\)", raw_val)
        if url_match:
            link_text = url_match.group(1)
            link_url  = url_match.group(2)
        else:
            link_text = raw_val
            link_url  = ""

        val = re.sub(r"[\*_]{1,2}|`", "", link_text).strip()

        if "name" in key_raw:
            fields["name"] = val
        elif "role" in key_raw:
            fields["role"] = val
        elif "desc" in key_raw:
            fields["description"] = val
        elif "lang" in key_raw or "coding" in key_raw:
            fields["language"] = val
        elif "frame" in key_raw:
            fields["framework"] = val
        elif any(k in key_raw for k in ("preview", "live", "demo", "link")):
            if link_url:
                fields["live_preview"] = _normalize_preview_url(link_url)
            elif val.startswith("http") or re.match(r"^[a-z0-9.-]+\.[a-z]{2,}(?:/.*)?$", val, re.IGNORECASE):
                fields["live_preview"] = _normalize_preview_url(val)

    return fields


def _build_project_card(folder_name: str, filenames: list, idx: int = 0):
    """Build a project dict using raw.githubusercontent.com fetches (0 API rate-limit cost)."""
    fallback_title = folder_name.replace("-", " ").replace("_", " ").title()
    safe_name = requests.utils.quote(folder_name)
    source_url = f"https://github.com/{GITHUB_USERNAME}/{PROJECTS_REPO}/tree/main/{safe_name}"
    preview_url = source_url

    parsed = {
        "name": "", "role": "", "description": "",
        "language": "", "framework": "", "live_preview": ""
    }

    # Find README filename if known from tree, otherwise probe common names
    readme_candidates = [f for f in filenames if f.lower().startswith("readme")]
    if not readme_candidates:
        readme_candidates = ["README.md", "readme.md", "README.txt", "readme.txt"]

    readme_text = None
    for rname in readme_candidates:
        readme_text = _get_raw_text(PROJECTS_REPO, f"{folder_name}/{rname}")
        if readme_text:
            break

    if readme_text:
        parsed = _parse_readme_fields(readme_text)
        if not parsed.get("description"):
            parsed["description"] = _extract_plain_desc(readme_text)
        if parsed.get("live_preview"):
            preview_url = _normalize_preview_url(parsed["live_preview"])

    title = (parsed.get("name") or fallback_title).strip()
    desc = (parsed.get("description") or f"A project called '{title}'. View the source on GitHub.").strip()

    tech = []
    for raw in (parsed.get("language", ""), parsed.get("framework", "")):
        for item in re.split(r"[,/&+]+", raw):
            item = item.strip()
            if item and item not in tech:
                tech.append(item)

    if not parsed.get("framework", "").strip():
        has_req = any(f.lower() == "requirements.txt" for f in filenames) or not filenames
        if has_req:
            req_text = _get_raw_text(PROJECTS_REPO, f"{folder_name}/requirements.txt")
            if req_text:
                for fw in _detect_frameworks_from_requirements(req_text):
                    if fw not in tech:
                        tech.append(fw)

    if not tech:
        tech = _detect_tech_from_filenames(filenames)
    tech = tech or ["Python"]

    color = _PALETTE[idx % len(_PALETTE)]
    has_live = bool(preview_url and preview_url != source_url)
    return {
        "title": title,
        "role": parsed.get("role", ""),
        "desc": desc,
        "tech": tech,
        "img": f"https://placehold.co/600x300/{color}/ffffff?text={requests.utils.quote(title)}",
        "preview": preview_url,
        "source": source_url,
        "stars": 0,
        "has_live": has_live,
    }


def fetch_projects_github(max_count: int = 20, return_meta: bool = False):
    """
    Fetch projects live from GitHub on every call.
    Only falls back to portfolio_data.json if GitHub is completely unreachable.
    """
    try:
        folders_map, is_live = _fetch_repo_tree_single_call(PROJECTS_REPO, "main")
        if is_live and folders_map:
            folder_items = list(folders_map.items())[:max_count]
            # Fetch READMEs concurrently via raw.githubusercontent.com for fast page reloads
            with ThreadPoolExecutor(max_workers=min(8, len(folder_items) or 1)) as pool:
                futures = [
                    pool.submit(_build_project_card, fname, flist, i)
                    for i, (fname, flist) in enumerate(folder_items)
                ]
                projects = [f.result() for f in futures if f.result()]
            if projects:
                return (projects, True) if return_meta else projects
    except Exception:
        pass

    # Fallback 1: checked-in portfolio_data.json
    local_data = _load_local_portfolio_data()
    if local_data and isinstance(local_data.get("projects"), list) and local_data["projects"]:
        projs = local_data["projects"][:max_count]
        return (projs, False) if return_meta else projs

    # Fallback 2: hardcoded constants
    projs = _FALLBACK_PROJECTS[:max_count]
    return (projs, False) if return_meta else projs


# ─────────────────────────────────────────────────────────────
# Certificates
# ─────────────────────────────────────────────────────────────

def _cert_style_for(name: str, issuer: str):
    """Return (logo_html, logo_bg, badge_color, badge_text) for a cert."""
    haystack = (issuer + " " + name).lower()

    for key, style in _ISSUER_STYLE.items():
        if key in haystack:
            return style

    for key, style in _CERT_KEYWORD_STYLE.items():
        if key in haystack:
            return style

    return _DEFAULT_CERT_STYLE


def _cert_from_filename(filename: str):
    """Build a cert dict from a PDF filename in the certificates repo."""
    try:
        stem = filename[:-4] if filename.lower().endswith(".pdf") else filename
        m = re.split(r"\s+by\s+", stem, maxsplit=1, flags=re.IGNORECASE)
        if len(m) == 2:
            raw_name, issuer = m[0].strip(), m[1].strip()
        else:
            raw_name, issuer = stem.strip(), ""

        cert_name = re.sub(r"[_\-]+", " ", raw_name).strip()
        cert_name = re.sub(r"\s+", " ", cert_name)
        if cert_name and cert_name[0].islower():
            cert_name = cert_name[0].upper() + cert_name[1:]

        logo_html, logo_bg, badge_color, badge_text = _cert_style_for(cert_name, issuer)
        safe_file = requests.utils.quote(filename)
        html_url = f"https://github.com/{GITHUB_USERNAME}/{CERTS_REPO}/blob/main/{safe_file}"
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{CERTS_REPO}/main/{safe_file}"

        return {
            "logo_html": logo_html,
            "logo_bg":   logo_bg,
            "name":      cert_name,
            "issuer":    issuer,
            "status":    "Certified",
            "badge":     f"https://placehold.co/80x80/{badge_color}/ffffff?text={badge_text}",
            "link":      html_url,
            "raw_url":   raw_url,
            "featured":  False,
        }
    except Exception:
        return None


def fetch_certs_github(return_meta: bool = False):
    """
    Fetch certificates live from GitHub first.
    Falls back to portfolio_data.json only if GitHub is unreachable.
    """
    try:
        # 1. Try GitHub contents API with cache-buster
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{CERTS_REPO}/contents"
        items = _get_json(url, params={"ref": "main"})
        pdf_names = []
        if isinstance(items, list):
            pdf_names = [
                i["name"] for i in items
                if i.get("type") == "file" and i.get("name", "").lower().endswith(".pdf")
            ]

        # 2. If REST API rate-limited, try Git Trees API
        if not pdf_names:
            tree_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{CERTS_REPO}/git/trees/main"
            tree_data = _get_json(tree_url)
            if tree_data and isinstance(tree_data.get("tree"), list):
                pdf_names = [
                    i["path"] for i in tree_data["tree"]
                    if i.get("type") == "blob" and i.get("path", "").lower().endswith(".pdf")
                ]

        # 3. If still empty, parse public GitHub HTML page (0 API quota)
        if not pdf_names:
            html_url = f"https://github.com/{GITHUB_USERNAME}/{CERTS_REPO}/tree/main"
            r = _SESSION.get(
                html_url,
                headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"},
                params={"_cb": int(time.time() * 1000)},
                timeout=10,
            )
            if r.status_code == 200:
                pat = rf'/{re.escape(GITHUB_USERNAME)}/{re.escape(CERTS_REPO)}/blob/main/([^"?#]+\.pdf)'
                for m in re.finditer(pat, r.text, re.IGNORECASE):
                    fname = requests.utils.unquote(m.group(1)).strip()
                    if fname and fname not in pdf_names:
                        pdf_names.append(fname)

        if pdf_names:
            out = [c for c in (_cert_from_filename(fn) for fn in pdf_names) if c]
            if out:
                return (out, True) if return_meta else out
    except Exception:
        pass

    # Fallback to local portfolio_data.json only when live fetch fails
    local_data = _load_local_portfolio_data()
    if local_data and isinstance(local_data.get("certificates"), list) and local_data["certificates"]:
        certs = local_data["certificates"]
        return (certs, False) if return_meta else certs

    return (_FALLBACK_CERTS, False) if return_meta else _FALLBACK_CERTS

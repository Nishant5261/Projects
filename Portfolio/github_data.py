"""
GitHub data fetcher for the portfolio.

Projects  → fetched as sub-folders from the 'Projects' repo.
            Each top-level folder is treated as one project.
            README is parsed for: Name, Role, Description, Language, Framework,
            and Live Preview link. Tech stack falls back to file-extension detection.

Certs     → fetched as PDF files from the 'certificates' repo.
            Filename format expected: "Cert Name by Issuer.pdf"
            (the " by " split extracts issuer; works without it too).

Config:
  • GITHUB_USERNAME — set to your GitHub username below.
  • GITHUB_TOKEN    — optional env-var for higher API rate-limits (60 → 5000 req/hr).
"""

import os
import re
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ──────────────────────────────────────────────
GITHUB_USERNAME  = "nishant5261"
PROJECTS_REPO    = "Projects"       # repo where each folder = one project
CERTS_REPO       = "certificates"   # repo where PDFs = certificates
# ──────────────────────────────────────────────

_SESSION = requests.Session()
_retry = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
_SESSION.mount("https://", HTTPAdapter(max_retries=_retry))
_SESSION.mount("http://", HTTPAdapter(max_retries=_retry))

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


# ── Extension → tech label ──────────────────────────────────
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

# ── requirements.txt package → display label ─────────────────
# Ordered so the first match per category wins (most specific first)
_REQUIREMENTS_FRAMEWORKS = [
    ("tensorflow",    "TensorFlow"),
    ("torch",         "PyTorch"),
    ("keras",         "Keras"),
    ("transformers",  "HuggingFace"),
    ("langchain",     "LangChain"),
    ("openai",        "OpenAI API"),
    ("anthropic",     "Anthropic"),
    ("sklearn",       "Scikit-learn"),
    ("scikit-learn",  "Scikit-learn"),
    ("xgboost",       "XGBoost"),
    ("lightgbm",      "LightGBM"),
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
        # Match: package name at start of line (ignoring ==, >=, etc.)
        if re.search(r"(?:^|[^a-zA-Z0-9_-])" + re.escape(pkg.lower()), text_lower, re.MULTILINE):
            seen.add(label)
            found.append(label)
    return found

# ── Palette for project placeholder images ───────────────────
_PALETTE = ["6366f1", "0ea5e9", "10b981", "f59e0b", "ef4444", "8b5cf6", "ec4899", "14b8a6"]

# ── Issuer → (icon_html, logo_bg, badge_color, badge_text) ──
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

# ── Keyword → style for certs without a clear issuer ─────────
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
# Shared
# ─────────────────────────────────────────────────────────────

def _headers():
    token = os.environ.get("GITHUB_TOKEN", "")
    h = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "portfolio-app",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        h["Authorization"] = f"token {token}"
    return h


def _get_json(url, params=None, timeout=7):
    """GET → parsed JSON, or None on error."""
    try:
        r = _SESSION.get(url, headers=_headers(), params=params, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None


def _load_local_portfolio_data():
    """Load data from the checked-in JSON file when available."""
    try:
        data_path = os.path.join(os.path.dirname(__file__), "portfolio_data.json")
        with open(data_path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def _fetch_repo_tree_html(repo: str = PROJECTS_REPO, branch: str = "main"):
    """Fetch the public GitHub HTML page for a repository tree."""
    try:
        url = f"https://github.com/{GITHUB_USERNAME}/{repo}/tree/{branch}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if r.status_code == 200:
            return r.text
    except Exception:
        return ""
    return ""


def _parse_project_names_from_html(html_text):
    """Extract top-level project folder names from the repository tree HTML."""
    try:
        pattern = rf'https://github.com/{re.escape(GITHUB_USERNAME)}/{re.escape(PROJECTS_REPO)}/tree/main/([^"?#]+)'
        names = []
        for match in re.finditer(pattern, html_text):
            name = match.group(1)
            if name and name not in names and name != ".devcontainer" and name != "readme.md":
                names.append(name)
        return names
    except Exception:
        return []


def _build_project_from_repo_name(repo_name: str):
    """Create a project card from a public GitHub repository directory name."""
    title = repo_name.replace("-", " ").replace("_", " ").title()
    safe_name = requests.utils.quote(repo_name)
    source_url = f"https://github.com/{GITHUB_USERNAME}/{PROJECTS_REPO}/tree/main/{safe_name}"
    preview_url = source_url
    color = _PALETTE[abs(hash(repo_name)) % len(_PALETTE)]
    return {
        "title": title,
        "role": "",
        "desc": f"Project folder from the public {PROJECTS_REPO} repository.",
        "tech": ["GitHub Repo"],
        "img": f"https://placehold.co/600x300/{color}/ffffff?text={requests.utils.quote(title)}",
        "preview": preview_url,
        "source": source_url,
        "stars": 0,
        "has_live": False,
    }


# ─────────────────────────────────────────────────────────────
# Projects
# ─────────────────────────────────────────────────────────────

def _detect_tech_from_files(file_list):
    """Return a deduplicated list of tech labels inferred from filenames."""
    seen, out = set(), []
    for f in file_list:
        name_lower = f["name"].lower()
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


def _parse_readme_fields(text):
    """
    Parse structured fields from a README.
    Handles patterns like:
      **Name:** My Project
      **Role:** ML Engineer
      - **Language**: Python
      Live Preview: https://...
      [View Live](https://...)

    Returns dict with keys: name, role, description, language, framework, live_preview
    """
    fields = {
        "name": "", "role": "", "description": "",
        "language": "", "framework": "", "live_preview": ""
    }

    # Match: optional list-marker + optional bold/italic + field label + colon + value
    pat = re.compile(
        r"^[-\*\s]*[\*_]{0,2}"
        r"(Name|Role|Description|Coding[\s_\-]?Language|Language|"
        r"Framework(?:[\s_\-]?Used)?|"
        r"Live[\s_\-]?Preview|Live\s+Link|Preview\s+Link|Demo|Website)"
        r"[\*_]{0,2}\s*:+\s*(.*)",
        re.IGNORECASE
    )

    for line in text.splitlines():
        m = pat.match(line.strip())
        if not m:
            continue
        key_raw = m.group(1).lower()
        raw_val = m.group(2).strip()

        # Extract markdown link [text](url) if present
        url_match = re.search(r"\[([^\]]*)\]\(([^)]+)\)", raw_val)
        if url_match:
            link_text = url_match.group(1)
            link_url  = url_match.group(2)
        else:
            link_text = raw_val
            link_url  = ""

        # Strip markdown formatting for the text value
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
            # Prefer extracted URL, else use bare value if it looks like a URL
            if link_url:
                fields["live_preview"] = link_url
            elif val.startswith("http"):
                fields["live_preview"] = val

    return fields


def _project_from_folder(folder):
    """Build a project dict from one folder item in the Projects repo."""
    try:
        fname = folder["name"]
        folder_url = folder["html_url"]

        # List folder contents
        files = _get_json(folder["url"]) or []
        if not isinstance(files, list):
            files = []

        # Fetch and parse README
        parsed = {
            "name": "", "role": "", "description": "",
            "language": "", "framework": "", "live_preview": ""
        }
        readme = next(
            (f for f in files
             if f["name"].lower().startswith("readme") and f["type"] == "file"),
            None,
        )
        if readme and readme.get("download_url"):
            try:
                r = requests.get(readme["download_url"], timeout=5)
                if r.status_code == 200:
                    parsed = _parse_readme_fields(r.text)
                    if not parsed["description"]:
                        parsed["description"] = _extract_plain_desc(r.text)
            except Exception:
                pass

        # Title
        title = (parsed["name"]
                 or fname.replace("-", " ").replace("_", " ").title())

        # Description
        desc = (parsed["description"]
                or f"A project called '{title}'. View the source on GitHub.")

        # Tech tags: README-declared languages/frameworks first
        tech = []
        for raw in (parsed["language"], parsed["framework"]):
            for item in re.split(r"[,/&+]+", raw):
                item = item.strip()
                if item and item not in tech:
                    tech.append(item)

        # If README has no framework field, detect frameworks from requirements.txt
        if not parsed["framework"].strip():
            req_file = next(
                (f for f in files
                 if f["name"].lower() == "requirements.txt" and f["type"] == "file"),
                None,
            )
            if req_file and req_file.get("download_url"):
                try:
                    r = requests.get(req_file["download_url"], timeout=5)
                    if r.status_code == 200:
                        for fw in _detect_frameworks_from_requirements(r.text):
                            if fw not in tech:
                                tech.append(fw)
                except Exception:
                    pass

        # Final fallback: infer from file extensions when nothing found yet
        if not tech:
            tech = _detect_tech_from_files(
                [f for f in files if f["type"] == "file"]
            )
        tech = tech or ["Code"]

        # Placeholder image
        color = _PALETTE[hash(fname) % len(_PALETTE)]
        img = (
            f"https://placehold.co/600x300/{color}/ffffff"
            f"?text={requests.utils.quote(title)}"
        )

        # Preview link: use live URL from README if available
        preview_url = parsed["live_preview"] or folder_url
        has_live    = bool(parsed["live_preview"])

        return {
            "title":    title,
            "role":     parsed["role"],
            "desc":     desc,
            "tech":     tech,
            "img":      img,
            "preview":  preview_url,
            "source":   folder_url,
            "stars":    0,
            "has_live": has_live,
        }
    except Exception:
        return None


def fetch_projects_github(max_count: int = 20):
    """Return projects from GitHub repository folders, with local JSON fallback."""
    local_data = _load_local_portfolio_data()
    if local_data and isinstance(local_data.get("projects"), list):
        return local_data["projects"][:max_count]

    try:
        html_text = _fetch_repo_tree_html(PROJECTS_REPO, "main")
        names = _parse_project_names_from_html(html_text)
        if names:
            projects = []
            for name in names[:max_count]:
                project = _build_project_from_repo_name(name)
                if project:
                    projects.append(project)
            if projects:
                return projects
    except Exception:
        pass

    try:
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{PROJECTS_REPO}/contents"
        items = _get_json(url)
        if not items or not isinstance(items, list):
            return _FALLBACK_PROJECTS[:max_count]

        folders = [i for i in items if i.get("type") == "dir"]
        if not folders:
            return _FALLBACK_PROJECTS[:max_count]

        out = []
        for folder in folders[:max_count]:
            proj = _project_from_folder(folder)
            if proj:
                out.append(proj)

        return out or _FALLBACK_PROJECTS[:max_count]
    except Exception:
        return _FALLBACK_PROJECTS[:max_count]


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


def _cert_from_pdf(pdf_item):
    """Build a cert dict from one PDF file item in the certificates repo."""
    try:
        filename = pdf_item["name"]
        stem = filename[:-4] if filename.lower().endswith(".pdf") else filename

        # Split on " by " (case-insensitive) to get name + issuer
        m = re.split(r"\s+by\s+", stem, maxsplit=1, flags=re.IGNORECASE)
        if len(m) == 2:
            raw_name, issuer = m[0].strip(), m[1].strip()
        else:
            raw_name, issuer = stem.strip(), ""

        # Clean up name
        cert_name = re.sub(r"[_\-]+", " ", raw_name).strip()
        cert_name = re.sub(r"\s+", " ", cert_name)
        if cert_name and cert_name[0].islower():
            cert_name = cert_name[0].upper() + cert_name[1:]

        logo_html, logo_bg, badge_color, badge_text = _cert_style_for(cert_name, issuer)

        # Raw PDF URL for in-page viewer (download_url = direct GitHub content URL)
        raw_url = pdf_item.get("download_url") or pdf_item["html_url"]

        return {
            "logo_html": logo_html,
            "logo_bg":   logo_bg,
            "name":      cert_name,
            "issuer":    issuer,
            "status":    "Certified",
            "badge":     f"https://placehold.co/80x80/{badge_color}/ffffff?text={badge_text}",
            "link":      pdf_item["html_url"],   # GitHub blob viewer (fallback)
            "raw_url":   raw_url,                # direct PDF for in-page popup
            "featured":  False,
        }
    except Exception:
        return None


def fetch_certs_github():
    """Return certificates from GitHub certificate files, with local JSON fallback."""
    local_data = _load_local_portfolio_data()
    if local_data and isinstance(local_data.get("certificates"), list):
        return local_data["certificates"]

    try:
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{CERTS_REPO}/contents"
        items = _get_json(url)
        if not items or not isinstance(items, list):
            return _FALLBACK_CERTS

        pdfs = [i for i in items
                if i.get("type") == "file" and i["name"].lower().endswith(".pdf")]
        if not pdfs:
            return _FALLBACK_CERTS

        out = []
        for pdf in pdfs:
            cert = _cert_from_pdf(pdf)
            if cert:
                out.append(cert)

        return out or _FALLBACK_CERTS
    except Exception:
        return _FALLBACK_CERTS

"""
CSS + keyframe animations for the portfolio page.

Split out of app.py so the ~1450-line stylesheet doesn't drown out the
page layout / content logic. Takes the color-token helpers (T, TA) and the
generated CSS-variable blocks (see app.py's THEME_DARK/THEME_LIGHT) so the
theme system still works exactly as before.
"""


def render_css(T, TA, css_vars_active, css_vars_dark, css_vars_light):
    """Return the full <link>/<style> block to hand to st.markdown()."""
    _CSS_VARS_ACTIVE = css_vars_active
    _CSS_VARS_DARK = css_vars_dark
    _CSS_VARS_LIGHT = css_vars_light
    return f"""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Fira+Code:wght@400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
/* ═══════════════════════════════════════════
   THEME VARIABLES
   :root carries the current (server-rendered) theme so first paint is
   correct with no flash. The data-theme overrides let the toggle button
   flip everything instantly on the client, no rerun required.
═══════════════════════════════════════════ */
:root {{
{_CSS_VARS_ACTIVE}
}}
:root[data-theme="dark"] {{
{_CSS_VARS_DARK}
}}
:root[data-theme="light"] {{
{_CSS_VARS_LIGHT}
}}

/* ═══════════════════════════════════════════
   KEYFRAME ANIMATIONS
═══════════════════════════════════════════ */
@keyframes fadeInUp {{
  from {{ opacity:0; transform:translateY(40px); }}
  to   {{ opacity:1; transform:translateY(0);    }}
}}
@keyframes fadeInDown {{
  from {{ opacity:0; transform:translateY(-40px); }}
  to   {{ opacity:1; transform:translateY(0);     }}
}}
@keyframes fadeInLeft {{
  from {{ opacity:0; transform:translateX(-40px); }}
  to   {{ opacity:1; transform:translateX(0);     }}
}}
@keyframes fadeInRight {{
  from {{ opacity:0; transform:translateX(40px); }}
  to   {{ opacity:1; transform:translateX(0);    }}
}}
@keyframes fadeIn {{
  from {{ opacity:0; }}
  to   {{ opacity:1; }}
}}
@keyframes float {{
  0%,100% {{ transform:translateY(0)    rotate(0deg); }}
  33%     {{ transform:translateY(-15px) rotate(1deg); }}
  66%     {{ transform:translateY(-8px)  rotate(-1deg); }}
}}
@keyframes floatSlow {{
  0%,100% {{ transform:translateY(0) translateX(0); }}
  25%     {{ transform:translateY(-20px) translateX(10px); }}
  50%     {{ transform:translateY(-10px) translateX(-5px); }}
  75%     {{ transform:translateY(-25px) translateX(8px); }}
}}
@keyframes shimmer {{
  0%   {{ background-position:200% center; }}
  100% {{ background-position:-200% center; }}
}}
@keyframes shimmerSlide {{
  0%   {{ transform:translateX(-100%); }}
  100% {{ transform:translateX(200%); }}
}}
@keyframes pulseRing {{
  0%   {{ box-shadow:0 0 0 0 {TA('accent','55')}; }}
  70%  {{ box-shadow:0 0 0 14px {TA('accent','00')}; }}
  100% {{ box-shadow:0 0 0 0 {TA('accent','00')}; }}
}}
@keyframes gradientShift {{
  0%   {{ background-position:0% 50%; }}
  50%  {{ background-position:100% 50%; }}
  100% {{ background-position:0% 50%; }}
}}
@keyframes slideDown {{
  from {{ opacity:0; transform:translateY(-16px); }}
  to   {{ opacity:1; transform:translateY(0); }}
}}
@keyframes scaleIn {{
  from {{ opacity:0; transform:scale(0.88); }}
  to   {{ opacity:1; transform:scale(1);    }}
}}
@keyframes rotateIn {{
  from {{ opacity:0; transform:rotate(-8deg) scale(0.9); }}
  to   {{ opacity:1; transform:rotate(0)     scale(1);   }}
}}
@keyframes borderGlow {{
  0%,100% {{ box-shadow:0 0 0 0 {TA('accent','00')}; }}
  50%     {{ box-shadow:0 0 20px 4px {TA('accent','33')}; }}
}}
@keyframes typing {{
  from {{ width:0; }}
  to   {{ width:100%; }}
}}
@keyframes blink {{
  0%,100% {{ border-color:transparent; }}
  50%     {{ border-color:{T['accent']}; }}
}}
@keyframes counterUp {{
  from {{ opacity:0; transform:translateY(10px); }}
  to   {{ opacity:1; transform:translateY(0); }}
}}
@keyframes particleDrift {{
  0%   {{ transform:translateY(0) translateX(0)   opacity:0; }}
  10%  {{ opacity:0.6; }}
  90%  {{ opacity:0.3; }}
  100% {{ transform:translateY(-120vh) translateX(40px) opacity:0; }}
}}
@keyframes rotateSlow {{
  from {{ transform:rotate(0deg); }}
  to   {{ transform:rotate(360deg); }}
}}
@keyframes morphBg {{
  0%,100% {{ border-radius:60% 40% 30% 70% / 60% 30% 70% 40%; }}
  50%     {{ border-radius:30% 60% 70% 40% / 50% 60% 30% 60%; }}
}}
@keyframes ripple {{
  0%   {{ transform:scale(0); opacity:0.6; }}
  100% {{ transform:scale(3); opacity:0; }}
}}
@keyframes glitch1 {{
  0%,100% {{ clip-path:inset(0 0 100% 0); transform:translateX(0); }}
  20%     {{ clip-path:inset(20% 0 60% 0); transform:translateX(-4px); }}
  40%     {{ clip-path:inset(50% 0 30% 0); transform:translateX(4px); }}
  60%     {{ clip-path:inset(70% 0 10% 0); transform:translateX(-2px); }}
  80%     {{ clip-path:inset(10% 0 80% 0); transform:translateX(2px); }}
}}
@keyframes lineExpand {{
  from {{ width:0; }}
  to   {{ width:48px; }}
}}
@keyframes cardShimmer {{
  0%   {{ background-position:-200% 0; }}
  100% {{ background-position:200% 0; }}
}}
@keyframes bounceIn {{
  0%   {{ opacity:0; transform:scale(0.3); }}
  50%  {{ opacity:1; transform:scale(1.05); }}
  70%  {{ transform:scale(0.9); }}
  100% {{ transform:scale(1); }}
}}
@keyframes waveText {{
  0%,100% {{ transform:translateY(0); }}
  50%     {{ transform:translateY(-6px); }}
}}
@keyframes spinIcon {{
  0%   {{ transform:rotateY(0deg); }}
  50%  {{ transform:rotateY(180deg); }}
  100% {{ transform:rotateY(360deg); }}
}}

/* ═══════════════════════════════════════════
   SCROLL-REVEAL
   Without JS: everything stays visible (no opacity:0).
   Once JS runs it adds .js-ready to <body>, which
   hides elements until the IntersectionObserver fires.
═══════════════════════════════════════════ */
body.js-ready .reveal       {{ opacity:0; transform:translateY(28px);  transition:opacity 0.7s cubic-bezier(.22,1,.36,1), transform 0.7s cubic-bezier(.22,1,.36,1); }}
body.js-ready .reveal-left  {{ opacity:0; transform:translateX(-42px); transition:opacity 0.7s cubic-bezier(.22,1,.36,1), transform 0.7s cubic-bezier(.22,1,.36,1); }}
body.js-ready .reveal-right {{ opacity:0; transform:translateX(42px);  transition:opacity 0.7s cubic-bezier(.22,1,.36,1), transform 0.7s cubic-bezier(.22,1,.36,1); }}
body.js-ready .reveal-scale {{ opacity:0; transform:scale(0.88);       transition:opacity 0.6s ease, transform 0.6s cubic-bezier(.34,1.56,.64,1); }}
.reveal.revealed, .reveal-left.revealed,
.reveal-right.revealed, .reveal-scale.revealed {{ opacity:1 !important; transform:none !important; }}
.stagger-1 {{ transition-delay:0.05s !important; }}
.stagger-2 {{ transition-delay:0.12s !important; }}
.stagger-3 {{ transition-delay:0.19s !important; }}
.stagger-4 {{ transition-delay:0.26s !important; }}
.stagger-5 {{ transition-delay:0.33s !important; }}
.stagger-6 {{ transition-delay:0.40s !important; }}

/* ═══════════════════════════════════════════
   GLOBAL BASE
═══════════════════════════════════════════ */
*, *::before, *::after {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
html, body, [class*="css"] {{
  font-family:'Inter', sans-serif !important;
  background-color:{T['bg']} !important;
  color:{T['text']} !important;
}}
/* The rule above forces Inter everywhere (incl. Streamlit's auto-generated
   st-emotion-cache-* wrappers, which match [class*="css"]) with !important.
   Icon fonts need their own family, so pin it back explicitly wherever an
   icon class is present, taking precedence over the global reset. */
.fa, .fas, .far, .fal, .fad, .fa-solid, .fa-regular, .fa-classic {{
  font-family:"Font Awesome 6 Free" !important;
  font-weight:900 !important;
}}
/* Must come after the rule above: brand icons (fa-instagram, fa-linkedin,
   fa-github, ...) use a separate font file, keyed off .fab/.fa-brands.
   Equal specificity to the rule above, so declaration order decides —
   keep this one last so brand glyphs win over the Free-family default. */
.fab, .fa-brands {{
  font-family:"Font Awesome 6 Brands" !important;
  font-weight:400 !important;
}}
.block-container {{ padding:0 !important; max-width:100% !important; }}
header[data-testid="stHeader"], footer {{ display:none !important; }}
section[data-testid="stSidebar"] {{ display:none !important; }}
div[data-testid="stToolbar"] {{ display:none !important; }}
.stApp {{ background-color:{T['bg']} !important; }}
div[data-testid="stMainBlockContainer"] {{ padding:62px max(2rem,5%) 0 !important; }}

/* ── ASCII Portrait ── */
.ascii-portrait-wrap {{
  display:flex;
  align-items:center;
  justify-content:center;
  height:100%;
}}
.ascii-portrait {{
  font-family:'Fira Code',monospace;
  font-size:4.5px;
  line-height:1.15;
  letter-spacing:0.5px;
  color:{T['accent']};
  background:linear-gradient(135deg,{T['card']},{T['tag_bg']});
  border:1px solid {T['border']};
  border-radius:16px;
  padding:0.75rem;
  overflow:hidden;
  white-space:pre;
  width:100%;
  display:block;
  filter:drop-shadow(0 0 8px {TA('accent','33')});
  transition:filter 0.35s ease, border-color 0.35s ease;
  animation:fadeIn 1s ease both;
}}
.ascii-portrait:hover {{
  filter:drop-shadow(0 0 18px {TA('accent','66')});
  border-color:{TA('accent','88')};
}}

/* Scrollbar */
::-webkit-scrollbar {{ width:4px; }}
::-webkit-scrollbar-track {{ background:{T['bg']}; }}
::-webkit-scrollbar-thumb {{
  background:linear-gradient(180deg,{T['accent']},{T['accent2']});
  border-radius:4px;
}}

/* Selection */
::selection {{ background:{TA('accent','33')}; color:{T['text']}; }}

/* ── Suppress browser-default blue only on our custom pill links ── */
a.social-pill, a.social-pill:visited,
a.btn-primary, a.btn-primary:visited,
a.btn-secondary, a.btn-secondary:visited,
a.footer-link-icon, a.footer-link-icon:visited,
a.back-to-top, a.back-to-top:visited {{
  text-decoration: none !important;
}}

/* ═══════════════════════════════════════════
   NAVIGATION BAR
═══════════════════════════════════════════ */
.nav-bar {{
  position:fixed;
  top:0; left:0; right:0;
  width:100%;
  z-index:9999;
  background:{T['nav_bg']};
  backdrop-filter:blur(20px) saturate(180%);
  -webkit-backdrop-filter:blur(20px) saturate(180%);
  border-bottom:1px solid {TA('border','55')};
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 max(2.5rem, 5%);
  height:62px;
  animation:slideDown 0.4s cubic-bezier(.22,1,.36,1);
}}
.nav-brand {{
  font-family:'Space Grotesk',sans-serif;
  font-size:1.15rem;
  font-weight:700;
  background:linear-gradient(90deg,{T['accent']},{T['accent2']},{T['accent']});
  background-size:300% auto;
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
  animation:shimmer 4s linear infinite;
  letter-spacing:-0.3px;
  cursor:default;
  position:relative;
}}
.nav-brand:hover::after {{
  content:attr(data-text);
  position:absolute;
  left:0; top:0;
  background:linear-gradient(90deg,{T['accent2']},{T['accent']});
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
  animation:glitch1 0.3s ease;
}}
.nav-links {{
  display:flex;
  align-items:center;
  gap:0.25rem;
}}
.nav-link {{
  position:relative;
  padding:0.45rem 0.95rem;
  font-size:0.875rem;
  font-weight:500;
  color:{T['nav_muted']} !important;
  text-decoration:none !important;
  border-radius:8px;
  transition:color 0.25s ease, background 0.25s ease;
  overflow:hidden;
}}
.nav-link::after {{
  content:'';
  position:absolute;
  bottom:4px; left:50%;
  width:0; height:2px;
  background:linear-gradient(90deg,{T['accent']},{T['accent2']});
  border-radius:2px;
  transform:translateX(-50%);
  transition:width 0.3s cubic-bezier(.22,1,.36,1);
}}
.nav-link:hover {{
  color:{T['text']} !important;
  background:{TA('border','44')};
}}
.nav-link:hover::after {{ width:60%; }}
.nav-link.active {{
  color:{T['accent']} !important;
  background:{T['tag_bg']};
  font-weight:600;
}}
.nav-link.active::after {{ width:70%; }}
/* Ripple on click */
.nav-link .ripple {{
  position:absolute;
  border-radius:50%;
  background:{TA('accent','44')};
  pointer-events:none;
  transform:scale(0);
  animation:ripple 0.6s ease;
}}

/* ═══ NAV THEME BUTTON (pure HTML, inside nav) ═══ */
.nav-theme-btn {{
  background:{T['card']};
  border:1px solid {T['border']};
  border-radius:50%;
  width:36px; height:36px;
  padding:0;
  font-size:1rem;
  line-height:1;
  color:{T['text']};
  cursor:pointer;
  margin-left:0.6rem;
  flex-shrink:0;
  transition:all 0.25s ease;
  box-shadow:{T['shadow2']};
  display:inline-flex;
  align-items:center;
  justify-content:center;
}}
.nav-theme-btn:hover {{
  border-color:{T['accent']};
  transform:scale(1.12) rotate(22deg);
  box-shadow:0 0 0 5px {T['glow']},0 4px 15px {TA('accent','33')};
}}

/* ═══ SCI-FI PROGRESS BAR — fixed strip below nav ═══ */
@keyframes scifiSweep {{
  0%   {{ opacity:0.6; transform:translateX(-120px); }}
  100% {{ opacity:0;   transform:translateX(40px); }}
}}
/* The outer strip sits just below the nav bar */
.progress-strip {{
  position:fixed;
  top:62px; left:0; right:0;
  height:4px;
  pointer-events:none;
  overflow:visible;
  z-index:9998;
}}
.scifi-bar-track {{
  position:absolute;
  top:0; left:0; right:0;
  height:3px;
  background:{TA('accent','15')};
  border-radius:2px;
}}
.scifi-bar-fill {{
  position:absolute;
  left:0; top:0;
  height:3px;
  width:0%;
  background:linear-gradient(90deg,{T['accent']},{T['accent2']},{T['accent3']});
  box-shadow:0 0 7px {T['accent']},0 0 20px {TA('accent','55')},0 0 40px {TA('accent','22')};
  /* No CSS transition — JS rAF lerp handles smoothness */
  border-radius:0 2px 2px 0;
  overflow:hidden;
}}
/* Leading-edge glow spike */
.scifi-bar-fill::after {{
  content:'';
  position:absolute;
  right:-2px; top:-3px;
  width:20px; height:9px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.95));
  border-radius:0 4px 4px 0;
  filter:blur(1.5px);
}}
/* Sweep shimmer on the fill */
.scifi-bar-fill::before {{
  content:'';
  position:absolute;
  top:0; left:0;
  width:60px; height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.55),transparent);
  animation:scifiSweep 2.2s ease-in-out infinite;
}}
/* Checkpoint container — hidden, only bar is shown */
.scifi-cp {{
  display:none;
}}
.scifi-cp-label {{
  display:none;
}}
.scifi-cp-diamond {{
  display:none;
}}

/* Horizontal scroll — hidden Streamlit theme button sits off-screen (hidden by JS) */

/* ═══════════════════════════════════════════
   HORIZONTAL SCROLL  (Projects & Certs)
═══════════════════════════════════════════ */
.scroll-controls {{
  display:flex;
  justify-content:flex-end;
  gap:0.5rem;
  margin-bottom:0.75rem;
  padding-right:0.25rem;
}}
.scroll-arrow-btn {{
  width:34px; height:34px;
  border-radius:50%;
  background:{T['card']};
  border:1px solid {T['border']};
  color:{T['text']};
  font-size:1.3rem;
  cursor:pointer;
  display:inline-flex; align-items:center; justify-content:center;
  transition:all 0.25s ease;
  line-height:1;
  flex-shrink:0;
}}
.scroll-arrow-btn:hover {{
  background:{T['tag_bg']};
  border-color:{T['accent']};
  color:{T['accent']};
  transform:scale(1.1);
  box-shadow:0 0 0 4px {TA('accent','22')};
}}
.horiz-scroll-track {{
  display:flex;
  gap:1.25rem;
  overflow-x:auto;
  overflow-y:visible;
  padding:1rem 0.25rem 1.25rem;
  scroll-snap-type:x mandatory;
  -webkit-overflow-scrolling:touch;
  scroll-behavior:smooth;
  scrollbar-width:thin;
  scrollbar-color:{T['accent']} {T['border2']};
}}
.horiz-scroll-track::-webkit-scrollbar {{ height:4px; }}
.horiz-scroll-track::-webkit-scrollbar-track {{
  background:{T['border2']};
  border-radius:2px;
}}
.horiz-scroll-track::-webkit-scrollbar-thumb {{
  background:linear-gradient(90deg,{T['accent']},{T['accent2']});
  border-radius:2px;
}}
/* Project cards — fixed-size, flip in place (3D) on hover to reveal
   description + links on the back instead of expanding horizontally */
.proj-scroll-item {{
  flex-shrink:0;
  width:260px;
  min-width:260px;
  height:320px;
  scroll-snap-align:start;
  position:relative;
  perspective:1000px;
}}
/* Cert cards — ~3 visible per full screen width */
.cert-scroll-item {{
  flex-shrink:0;
  width:calc(33.33% - 0.84rem);
  min-width:275px;
  scroll-snap-align:start;
}}
.cert-scroll-item .cert-card {{ height:100%; }}
/* GitHub source badge */
.gh-source-badge {{
  display:inline-flex;
  align-items:center;
  gap:0.4rem;
  font-size:0.74rem;
  color:{T['muted']};
  background:{T['card']};
  border:1px solid {T['border']};
  border-radius:20px;
  padding:0.22rem 0.85rem;
  margin-top:0.5rem;
}}

/* ═══════════════════════════════════════════
   PARTICLES CANVAS (hero bg)
═══════════════════════════════════════════ */
#particles-canvas {{
  position:absolute;
  top:0; left:0; width:100%; height:100%;
  pointer-events:none;
  z-index:0;
}}

/* ═══════════════════════════════════════════
   HERO SECTION
═══════════════════════════════════════════ */
.hero {{
  background:{T['hero_grad']};
  padding:6rem max(2.5rem,7%) 5rem;
  border-bottom:1px solid {T['border']};
  position:relative;
  overflow:hidden;
  min-height:520px;
  display:flex;
  align-items:center;
  justify-content:center;
}}
/* ── Hero inner: text left, portrait right ── */
.hero-inner {{
  display:flex;
  align-items:center;
  gap:2rem;
  max-width:1260px;
  margin:0 auto;
  width:100%;
  position:relative;
  z-index:2;
}}
/* ── Hero portrait ── */
.hero-portrait-wrap {{
  flex-shrink:0;
  position:relative;
  width:540px;
  display:flex;
  align-items:flex-end;
  justify-content:center;
}}
.hero-portrait-glow {{
  position:absolute;
  bottom:-24px; left:50%;
  transform:translateX(-50%);
  width:300px; height:70px;
  background:radial-gradient(ellipse,{TA('accent','66')} 0%,{TA('accent2','22')} 55%,transparent 72%);
  filter:blur(20px);
  animation:portraitGlow 3.5s ease-in-out infinite;
  z-index:0;
  pointer-events:none;
}}
.hero-portrait-img {{
  position:relative;
  z-index:1;
  width:100%;
  max-width:540px;
  filter:drop-shadow(0 8px 28px {TA('accent','55')}) drop-shadow(0 0 70px {TA('accent2','33')});
  animation:portraitFloat 5s ease-in-out infinite, portraitReveal 1s cubic-bezier(.22,1,.36,1) 0.5s both;
  transform-origin:center bottom;
}}
@keyframes portraitFloat {{
  0%,100% {{ transform:translateY(0px) rotate(0deg); }}
  50% {{ transform:translateY(-18px) rotate(0.4deg); }}
}}
@keyframes portraitReveal {{
  from {{ opacity:0; transform:translateY(50px) scale(0.85); }}
  to   {{ opacity:1; transform:translateY(0)    scale(1);    }}
}}
@keyframes portraitGlow {{
  0%,100% {{ opacity:0.45; transform:translateX(-50%) scaleX(1);    }}
  50%     {{ opacity:0.85; transform:translateX(-50%) scaleX(1.25); }}
}}
/* Responsive: stack portrait above text on small screens */
@media(max-width:900px) {{
  .hero-inner    {{ flex-direction:column-reverse; gap:1rem; }}
  .hero-content  {{ text-align:center !important; max-width:none !important; }}
  .hero-subtitle {{ justify-content:center !important; }}
  .social-links  {{ justify-content:center !important; }}
  .tagline-box   {{ margin:0 auto 2rem !important; }}
  .hero-portrait-wrap {{ width:300px; }}
}}
.hero-orb-1 {{
  position:absolute;
  top:-10%; left:-5%;
  width:500px; height:500px;
  background:radial-gradient(ellipse,{TA('accent','18')} 0%,transparent 65%);
  animation:floatSlow 12s ease-in-out infinite;
  pointer-events:none;
}}
.hero-orb-2 {{
  position:absolute;
  bottom:-15%; right:-5%;
  width:450px; height:450px;
  background:radial-gradient(ellipse,{TA('accent2','14')} 0%,transparent 65%);
  animation:floatSlow 15s ease-in-out infinite reverse;
  pointer-events:none;
}}
.hero-orb-3 {{
  position:absolute;
  top:30%; left:50%;
  width:300px; height:300px;
  transform:translateX(-50%);
  background:radial-gradient(ellipse,{TA('accent3','08')} 0%,transparent 70%);
  animation:float 10s ease-in-out infinite;
  pointer-events:none;
}}
.hero-content {{
  position:relative;
  z-index:2;
  flex:1;
  max-width:560px;
  text-align:left;
}}
.hero-content .hero-subtitle {{ justify-content:flex-start; }}
.hero-content .social-links  {{ justify-content:flex-start; }}
.hero-content .tagline-box   {{ margin:0 0 2rem; }}
.hero-badge {{
  display:inline-flex;
  align-items:center;
  gap:0.5rem;
  padding:0.35rem 1rem;
  background:{T['tag_bg']};
  border:1px solid {TA('accent','44')};
  border-radius:30px;
  font-size:0.78rem;
  font-weight:600;
  color:{T['accent']};
  margin-bottom:1.5rem;
  animation:fadeInDown 0.6s ease 0.1s both;
  letter-spacing:0.5px;
  text-transform:uppercase;
}}
.hero-badge-dot {{
  width:7px; height:7px;
  border-radius:50%;
  background:{T['accent3']};
  animation:pulseRing 2s ease-out infinite;
}}
.hero h1 {{
  font-family:'Space Grotesk',sans-serif;
  font-size:clamp(2.5rem,6vw,4.2rem);
  font-weight:800;
  letter-spacing:-2px;
  line-height:1.05;
  color:{T['text']};
  margin:0 0 0.3rem;
  animation:fadeInUp 0.7s ease 0.2s both;
}}
.hero h1 .name-gradient {{
  background:linear-gradient(90deg,{T['accent']},{T['accent2']},{T['accent3']},{T['accent']});
  background-size:300% auto;
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
  animation:shimmer 4s linear infinite;
  display:inline-block;
}}
.hero h1 .name-gradient:hover {{
  animation:shimmer 1.5s linear infinite;
}}
.hero-subtitle {{
  font-size:1.1rem;
  color:{T['text2']};
  font-weight:400;
  margin-bottom:1.5rem;
  animation:fadeInUp 0.7s ease 0.35s both;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:0.6rem;
  flex-wrap:wrap;
}}
.hero-subtitle .dot {{ color:{T['muted']}; }}
.hero-typed-wrap {{
  font-size:1rem;
  color:{T['muted']};
  margin-bottom:2rem;
  animation:fadeInUp 0.7s ease 0.45s both;
  min-height:1.6rem;
}}
.hero-typed {{
  color:{T['accent']};
  font-weight:600;
  border-right:2px solid {T['accent']};
  padding-right:2px;
  animation:blink 0.85s step-end infinite;
  white-space:nowrap;
  overflow:hidden;
  display:inline-block;
}}
.tagline-box {{
  display:inline-flex;
  align-items:flex-start;
  gap:0.75rem;
  background:{TA('card','88')};
  border:1px solid {T['border']};
  border-left:3px solid {T['accent']};
  border-radius:0 12px 12px 0;
  padding:0.85rem 1.25rem;
  max-width:520px;
  margin:0 auto 2rem;
  text-align:left;
  font-size:0.9rem;
  font-style:italic;
  color:{T['text2']};
  animation:fadeInUp 0.7s ease 0.55s both;
}}
.tagline-box i {{ color:{T['accent']}; margin-top:2px; flex-shrink:0; }}
.social-links {{
  display:flex;
  gap:0.65rem;
  justify-content:center;
  flex-wrap:wrap;
  animation:fadeInUp 0.7s ease 0.65s both;
}}
.social-pill {{
  display:inline-flex !important;
  align-items:center !important;
  gap:0.45rem !important;
  padding:0.5rem 1.1rem !important;
  background:{T['card']} !important;
  border:1px solid {T['border']} !important;
  border-radius:30px !important;
  font-size:0.82rem !important;
  font-weight:500 !important;
  color:{T['text']} !important;
  text-decoration:none !important;
  transition:all 0.3s cubic-bezier(.22,1,.36,1) !important;
  position:relative !important;
  overflow:hidden !important;
}}
.social-pill::before {{
  content:'';
  position:absolute;
  top:0; left:-100%;
  width:100%; height:100%;
  background:linear-gradient(90deg,transparent,{TA('accent','18')},transparent);
  transition:left 0.4s ease;
}}
.social-pill:hover::before {{ left:100%; }}
.social-pill:hover {{
  border-color:{T['accent']} !important;
  color:{T['accent']} !important;
  transform:translateY(-3px) scale(1.02) !important;
  box-shadow:0 6px 20px {TA('accent','33')} !important;
}}

/* ═══════════════════════════════════════════
   SECTION COMMONS
═══════════════════════════════════════════ */
.page-section {{
  padding:5rem max(2.5rem,7%);
  border-bottom:none;
  background:{T['bg']};
  position:relative;
}}
.page-section:nth-child(even) {{
  background:{T['bg2']};
}}
.section-header {{
  text-align:center;
  margin-bottom:3.5rem;
}}
.section-eyebrow {{
  font-size:0.72rem;
  font-weight:700;
  letter-spacing:2px;
  text-transform:uppercase;
  color:{T['accent']};
  margin-bottom:0.6rem;
  animation:fadeInDown 0.5s ease both;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:0.5rem;
}}
.section-eyebrow::before, .section-eyebrow::after {{
  content:''; display:block;
  width:28px; height:1px;
  background:{TA('accent','66')};
}}
.section-title {{
  font-family:'Space Grotesk',sans-serif;
  font-size:2.2rem;
  font-weight:800;
  letter-spacing:-0.8px;
  color:{T['text']};
  margin-bottom:0.5rem;
  animation:fadeInUp 0.5s ease 0.05s both;
}}
.section-sub {{
  font-size:1rem;
  color:{T['muted']};
  animation:fadeInUp 0.5s ease 0.1s both;
}}
.accent-line {{ display:none; }}
.accent-line-left {{ display:none; }}
.section-eyebrow::before, .section-eyebrow::after {{ display:none; }}

/* ═══════════════════════════════════════════
   STAT BOXES
═══════════════════════════════════════════ */
.stats-row {{
  display:flex;
  gap:1.25rem;
  flex-wrap:wrap;
  margin-bottom:3rem;
}}
.stat-box {{
  flex:1;
  min-width:140px;
  background:{T['card']};
  border:1px solid {T['border']};
  border-radius:16px;
  padding:1.5rem;
  text-align:center;
  transition:all 0.35s cubic-bezier(.22,1,.36,1);
  position:relative;
  overflow:hidden;
}}
.stat-box::before {{
  content:'';
  position:absolute;
  top:0; left:-100%;
  width:100%; height:2px;
  background:linear-gradient(90deg,{T['accent']},{T['accent2']});
  transition:left 0.5s ease;
}}
.stat-box:hover::before {{ left:0; }}
.stat-box:hover {{
  border-color:{TA('accent','66')};
  box-shadow:0 0 0 4px {T['glow']}, {T['shadow']};
  transform:translateY(-5px);
}}
.stat-num {{
  font-family:'Space Grotesk',sans-serif;
  font-size:2.6rem;
  font-weight:800;
  background:linear-gradient(135deg,{T['accent']},{T['accent2']});
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
  line-height:1;
  display:block;
}}
.stat-label {{
  font-size:0.75rem;
  color:{T['muted']};
  font-weight:500;
  text-transform:uppercase;
  letter-spacing:0.5px;
  margin-top:0.4rem;
  color:{T['text2']};
}}

/* ═══════════════════════════════════════════
   ABOUT + TIMELINE
═══════════════════════════════════════════ */
.about-text {{
  font-size:0.95rem;
  color:{T['text2']};
  line-height:1.95;
  margin-bottom:1rem;
}}
.about-text strong {{ color:{T['text']}; font-weight:600; }}
.timeline-item {{
  display:flex;
  gap:1.25rem;
  padding-bottom:2.25rem;
  position:relative;
}}
.timeline-item:not(:last-child)::before {{
  content:'';
  position:absolute;
  left:17px; top:38px; bottom:0;
  width:2px;
  background:linear-gradient(to bottom,{TA('accent','88')},transparent);
}}
.timeline-dot {{
  width:36px; height:36px;
  border-radius:50%;
  background:linear-gradient(135deg,{T['accent']},{T['accent2']});
  display:flex; align-items:center; justify-content:center;
  font-size:1rem;
  flex-shrink:0;
  animation:pulseRing 3s ease-out infinite;
  box-shadow:0 0 0 4px {T['tag_bg']};
}}
.timeline-title {{ font-size:1rem; font-weight:700; color:{T['text']}; }}
.timeline-org   {{ font-size:0.875rem; font-weight:600; color:{T['accent']}; margin:0.15rem 0; }}
.timeline-date  {{ font-size:0.78rem; color:{T['muted']}; margin-bottom:0.4rem; }}
.timeline-desc  {{ font-size:0.86rem; color:{T['text2']}; line-height:1.75; }}

/* ═══════════════════════════════════════════
   ACHIEVEMENT
═══════════════════════════════════════════ */
.achievement {{
  display:flex; align-items:center; gap:1.25rem;
  background:linear-gradient(135deg,{T['tag_bg']},{T['card']});
  border:1px solid {TA('accent','33')};
  border-radius:16px;
  padding:1.25rem 1.5rem;
  margin-bottom:1rem;
  transition:all 0.3s ease;
  position:relative;
  overflow:hidden;
}}
.achievement::after {{
  content:'';
  position:absolute;
  inset:0;
  background:linear-gradient(135deg,{TA('accent','05')},transparent);
  animation:borderGlow 3s ease-in-out infinite;
  pointer-events:none;
}}
.achievement:hover {{ transform:translateX(8px); border-color:{TA('accent','66')}; }}
.achievement-icon {{ font-size:2rem; }}
.achievement-title {{ font-size:0.95rem; font-weight:700; color:{T['text']}; }}
.achievement-detail {{ font-size:0.82rem; color:{T['text2']}; margin-top:0.15rem; }}

/* ═══════════════════════════════════════════
   SKILLS SECTION
═══════════════════════════════════════════ */
.skills-category-label {{
  font-size:0.7rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:1.5px;
  color:{T['accent']};
  margin-bottom:1.25rem;
  display:flex;
  align-items:center;
  gap:0.5rem;
}}
.skills-category-label::after {{
  content:''; flex:1;
  height:1px;
  background:linear-gradient(90deg,{T['border']},transparent);
}}
.skill-chip-grid {{
  display:flex;
  flex-wrap:wrap;
  gap:0.65rem;
  margin-bottom:1.75rem;
}}
.skill-chip {{
  display:inline-flex;
  align-items:center;
  gap:0.55rem;
  padding:0.5rem 0.9rem;
  background:{T['card']};
  border:1px solid {T['border']};
  border-radius:10px;
  font-size:0.82rem;
  font-weight:600;
  color:{T['text']};
  cursor:default;
  transition:all 0.3s cubic-bezier(.22,1,.36,1);
  position:relative;
  overflow:hidden;
}}
.skill-chip::before {{
  content:'';
  position:absolute;
  inset:0;
  background:linear-gradient(135deg,{TA('accent','08')},{TA('accent2','08')});
  opacity:0;
  transition:opacity 0.3s ease;
}}
.skill-chip:hover::before {{ opacity:1; }}
.skill-chip:hover {{
  border-color:{TA('accent','88')};
  transform:translateY(-3px) scale(1.03);
  box-shadow:0 6px 20px {TA('accent','22')};
  color:{T['accent']};
}}
.skill-chip:hover img {{
  animation:spinIcon 0.6s ease;
}}
.skill-chip img {{
  width:20px; height:20px;
  object-fit:contain;
  flex-shrink:0;
  transition:transform 0.3s ease;
}}
.skill-chip .chip-emoji {{
  font-size:1rem;
  display:inline-block;
}}
.tools-chip {{
  display:inline-flex;
  align-items:center;
  gap:0.45rem;
  padding:0.4rem 0.8rem;
  background:{T['badge_bg']};
  border:1px solid {T['border']};
  border-radius:8px;
  font-size:0.78rem;
  font-weight:500;
  color:{T['badge_text']};
  font-family:'Fira Code',monospace;
  transition:all 0.25s ease;
}}
.tools-chip:hover {{
  border-color:{TA('accent','66')};
  color:{T['text']};
  transform:translateY(-2px);
  box-shadow:0 4px 12px {TA('accent','18')};
}}
.skill-section-card {{
  background:{T['card']};
  border:1px solid {T['border']};
  border-radius:20px;
  padding:2rem;
  height:100%;
  transition:all 0.35s ease;
  position:relative;
  overflow:hidden;
}}
.skill-section-card::after {{
  content:'';
  position:absolute;
  top:0; left:0; right:0; height:2px;
  background:linear-gradient(90deg,{T['accent']},{T['accent2']},{T['accent3']});
  transform:scaleX(0);
  transform-origin:left;
  transition:transform 0.4s ease;
}}
.skill-section-card:hover::after {{ transform:scaleX(1); }}
.skill-section-card:hover {{
  box-shadow:{T['shadow']};
  border-color:{TA('accent','44')};
}}

/* ═══════════════════════════════════════════
   PROJECT CARDS
═══════════════════════════════════════════ */
/* ── Project card: absolute within fixed-height item, expands on hover ── */
/* ── Flip card: .proj-scroll-item is the 3D stage, .proj-card is the
   rotating flipper, .proj-face/.proj-extra are its two absolutely-stacked
   faces (front/back), each with backface-visibility hidden so only one
   shows at a time. Hovering the card rotates it 180° on the Y axis. ── */
.proj-card {{
  position:absolute;
  top:0; left:0; right:0; bottom:0;
  z-index:1;
  transform-style:preserve-3d;
  transition:transform 0.5s cubic-bezier(.2,.8,.2,1);
  transform-origin:center center;
  will-change:transform;
}}
.proj-scroll-item:hover .proj-card {{
  z-index:100;
  transform:rotateY(180deg);
}}

/* ── Front face: tightly-cropped image up top, title + tech chips below ── */
.proj-face {{
  position:absolute;
  inset:0;
  backface-visibility:hidden;
  background:{T['card']};
  border:1px solid {T['border']};
  border-radius:20px;
  overflow:hidden;
  display:flex;
  flex-direction:column;
  box-shadow:{T['shadow']};
  transition:border-color 0.3s ease;
  padding:0.7rem 0.7rem 0;
}}
.proj-scroll-item:hover .proj-face {{ border-color:{TA('accent','66')}; }}
.proj-face-bg {{
  width:100%;
  height:104px;
  flex-shrink:0;
  object-fit:cover;
  border-radius:12px;
  /* favor the upper-middle of the source image, where thumbnails/logos
     tend to sit, so the card isn't mostly empty background */
  object-position:center 30%;
  display:block;
}}
.proj-face-content {{
  position:relative;
  flex:1;
  display:flex;
  flex-direction:column;
  padding:0.9rem 1rem 1rem;
}}
.proj-title {{
  font-size:1.0rem; font-weight:700;
  color:{T['text']};
  margin-bottom:0.4rem;
  line-height:1.3;
}}
.proj-stars {{
  font-size:0.7rem; color:#f0c040; margin-left:0.3rem;
}}
.proj-role {{
  display:inline-flex; align-items:center; gap:0.3rem;
  align-self:flex-start;
  font-size:0.63rem; font-weight:700; letter-spacing:0.5px;
  text-transform:uppercase;
  color:{T['accent']}; background:{TA('accent','14')};
  border:1px solid {TA('accent','40')}; border-radius:20px;
  padding:0.15rem 0.6rem;
  margin-bottom:0.7rem;
}}

/* ── Back face: description + preview/source links, revealed on flip ── */
.proj-extra {{
  position:absolute;
  inset:0;
  backface-visibility:hidden;
  transform:rotateY(180deg);
  overflow:hidden;
  display:flex;
  flex-direction:column;
  justify-content:center;
  padding:1.2rem 1.3rem;
  background:{T['card']};
  border:1px solid {TA('accent','66')};
  border-radius:20px;
  box-shadow:{T['shadow']};
}}
.proj-desc  {{ font-size:0.82rem; color:{T['text2']}; line-height:1.65; margin-bottom:0.9rem; }}
.proj-tech  {{ display:flex; flex-wrap:wrap; gap:0.3rem; margin-top:auto; }}
.tech-tag {{
  padding:0.18rem 0.5rem;
  background:{T['badge_bg']};
  color:{T['badge_text']};
  border-radius:6px;
  font-size:0.69rem;
  font-weight:500;
  border:1px solid {T['border']};
  font-family:'Fira Code',monospace;
}}
.proj-footer {{ display:flex; gap:0.55rem; flex-wrap:wrap; }}
.btn-primary {{
  display:inline-flex; align-items:center; gap:0.4rem;
  padding:0.45rem 1rem;
  background:linear-gradient(90deg,{T['accent']},{T['accent2']});
  color:#fff !important;
  border-radius:9px;
  font-size:0.8rem; font-weight:600;
  text-decoration:none;
  border:none;
  transition:all 0.3s ease;
  position:relative; overflow:hidden;
}}
.btn-primary::after {{
  content:'';
  position:absolute;
  top:50%; left:50%;
  width:0; height:0;
  background:#ffffff33;
  border-radius:50%;
  transform:translate(-50%,-50%);
  transition:width 0.4s ease, height 0.4s ease;
}}
.btn-primary:hover::after {{ width:200px; height:200px; }}
.btn-primary:hover {{ transform:scale(1.04); box-shadow:0 4px 18px {TA('accent','55')}; }}
.btn-secondary {{
  display:inline-flex; align-items:center; gap:0.4rem;
  padding:0.45rem 1rem;
  background:transparent;
  color:{T['accent']} !important;
  border:1px solid {T['accent']};
  border-radius:9px;
  font-size:0.8rem; font-weight:600;
  text-decoration:none;
  transition:all 0.3s ease;
}}
.btn-secondary:hover {{
  background:{T['accent']};
  color:#fff !important;
  transform:scale(1.04);
}}

/* ═══════════════════════════════════════════
   CERTIFICATE CARDS
═══════════════════════════════════════════ */
.cert-grid {{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
  gap:1.25rem;
}}
.cert-card {{
  background:{T['card']};
  border:1px solid {T['cert_border']};
  border-radius:20px;
  padding:1.5rem;
  position:relative;
  overflow:visible;
  transition:all 0.35s cubic-bezier(.22,1,.36,1);
  min-height:200px;
}}
.cert-card:hover {{
  transform:translateY(-6px) scale(1.01);
  box-shadow:{T['shadow']};
  border-color:{TA('accent','88')};
}}
.cert-card.featured {{
  border:2px solid {T['accent']};
  background:linear-gradient(135deg,{T['card']},{TA('tag_bg','44')});
}}
.cert-card.featured::before {{
  content:'★ Featured';
  position:absolute;
  top:-11px; left:16px;
  font-size:0.65rem; font-weight:700;
  letter-spacing:0.5px; text-transform:uppercase;
  color:#fff;
  background:linear-gradient(90deg,{T['accent']},{T['accent2']});
  padding:0.2rem 0.65rem;
  border-radius:20px;
}}
.cert-header {{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  margin-bottom:1rem;
  min-height:56px;
}}
.cert-issuer-logo {{
  display:flex; align-items:center; justify-content:center;
  width:50px; height:50px;
  border-radius:12px;
  font-size:1.7rem;
  flex-shrink:0;
  transition:transform 0.3s ease;
}}
.cert-card:hover .cert-issuer-logo {{ transform:scale(1.1) rotate(-3deg); }}
.cert-badge-img {{
  width:68px; height:68px;
  border-radius:50%;
  object-fit:cover;
  border:3px solid {T['bg']};
  box-shadow:0 4px 16px rgba(0,0,0,0.25);
  position:absolute;
  top:-14px; right:14px;
  transition:transform 0.35s cubic-bezier(.22,1,.36,1);
}}
.cert-card:hover .cert-badge-img {{ transform:rotate(8deg) scale(1.08); }}
.cert-name   {{ font-size:0.98rem; font-weight:700; color:{T['text']}; margin-bottom:0.3rem; padding-right:60px; line-height:1.4; }}
.cert-issuer {{ font-size:0.8rem; color:{T['muted']}; margin-bottom:0.15rem; }}
.cert-status {{
  display:inline-flex; align-items:center; gap:0.3rem;
  font-size:0.74rem; font-weight:600;
  color:{T['accent3']};
  margin-bottom:0.9rem;
}}
.cert-status::before {{
  content:''; width:6px; height:6px;
  border-radius:50%;
  background:{T['accent3']};
  animation:pulseRing 2s ease-out infinite;
  flex-shrink:0;
}}
.view-cert {{
  display:inline-flex; align-items:center; gap:0.35rem;
  color:{T['view_link']};
  font-size:0.84rem; font-weight:700;
  text-decoration:none; background:none;
  border:none; border-bottom:1px solid transparent;
  cursor:pointer; padding:0;
  transition:all 0.25s ease;
  font-family:inherit;
}}
.view-cert:hover {{ gap:0.6rem; border-bottom-color:{T['view_link']}; }}

/* ═══ CERTIFICATE MODAL ═══ */
.cert-modal-overlay {{
  display:none; position:fixed; inset:0;
  background:rgba(0,0,0,0.78); z-index:9999;
  align-items:center; justify-content:center;
  backdrop-filter:blur(5px);
}}
.cert-modal-box {{
  background:{T['card']}; border:1px solid {T['border']};
  border-radius:18px;
  width:min(920px,94vw); height:min(700px,90vh);
  display:flex; flex-direction:column; overflow:hidden;
  box-shadow:0 32px 100px rgba(0,0,0,0.7), 0 0 0 1px {TA('accent','22')};
  animation:scaleInModal 0.22s cubic-bezier(.22,1,.36,1) both;
}}
.cert-modal-header {{
  display:flex; align-items:center; justify-content:space-between;
  padding:0.9rem 1.3rem; border-bottom:1px solid {T['border']};
  gap:1rem; flex-shrink:0;
  background:{T['card']};
}}
.cert-modal-title {{
  font-weight:700; font-size:0.95rem; color:{T['text']};
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}}
.cert-modal-close {{
  background:none !important; border:1px solid {T['border']} !important;
  color:{T['text']} !important; border-radius:8px !important;
  width:32px !important; height:32px !important; flex-shrink:0 !important;
  display:flex !important; align-items:center !important; justify-content:center !important;
  cursor:pointer !important; font-size:1.1rem !important;
  transition:background 0.2s, border-color 0.2s !important; padding:0 !important;
}}
.cert-modal-close:hover {{ background:{T['tag_bg']} !important; border-color:{TA('accent','66')} !important; }}
.cert-modal-body {{ flex:1; overflow:hidden; position:relative; }}
.cert-modal-body iframe {{ width:100%; height:100%; border:none; display:block; }}
.cert-modal-loading {{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:0.75rem;
  color:{T['muted']}; font-size:0.9rem;
}}
@keyframes scaleInModal {{
  from {{ transform:scale(0.88); opacity:0; }}
  to   {{ transform:scale(1);    opacity:1; }}
}}

/* ═══════════════════════════════════════════
   CONTACT
═══════════════════════════════════════════ */
.contact-info-card {{
  background:{T['card']};
  border:1px solid {T['border']};
  border-radius:18px;
  padding:1.75rem;
  margin-bottom:1.5rem;
}}
.contact-item {{
  display:flex; align-items:center; gap:0.9rem;
  padding:0.75rem 0;
  border-bottom:1px solid {T['border']};
  transition:transform 0.25s ease;
}}
.contact-item:last-child {{ border-bottom:none; }}
.contact-item:hover {{ transform:translateX(4px); }}
.contact-item i {{ color:{T['accent']}; width:20px; text-align:center; font-size:1.1rem; }}
.contact-item-body {{ flex:1 1 auto; min-width:0; }}
.contact-label {{ font-size:0.73rem; color:{T['muted']}; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0.15rem; }}
.contact-link {{
  color:{T['accent']}; font-weight:600; font-size:0.9rem;
  text-decoration:none; transition:opacity 0.2s;
}}
.contact-link:hover {{ opacity:0.75; }}
.contact-val {{ color:{T['text']}; font-size:0.9rem; font-weight:500; }}
.contact-visit-btn {{
  flex:0 0 auto;
  display:inline-flex; align-items:center; gap:0.4rem;
  padding:0.4rem 0.9rem;
  border-radius:999px;
  border:1px solid {TA('accent','40')};
  background:{TA('accent','14')};
  color:{T['accent']}; font-weight:600; font-size:0.78rem;
  text-decoration:none; white-space:nowrap;
  transition:background 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
}}
.contact-visit-btn:hover {{
  background:{TA('accent','28')};
  border-color:{TA('accent','80')};
  transform:translateY(-1px);
}}
.contact-visit-btn i {{ color:inherit; width:auto; font-size:0.75rem; }}

/* ─── Streamlit form inputs ─── */
.stTextInput input, .stTextArea textarea {{
  background:{T['input_bg']} !important;
  border-color:{T['border']} !important;
  color:{T['text']} !important;
  border-radius:10px !important;
  font-size:0.9rem !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
  border-color:{T['accent']} !important;
  box-shadow:0 0 0 3px {T['glow']} !important;
}}
.stTextInput label, .stTextArea label {{ color:{T['text2']} !important; }}
.stFormSubmitButton button {{
  background:linear-gradient(90deg,{T['accent']},{T['accent2']}) !important;
  color:#fff !important; border:none !important;
  border-radius:10px !important;
  font-weight:600 !important; font-size:0.9rem !important;
  padding:0.6rem 2rem !important;
  transition:all 0.3s ease !important;
  width:100% !important;
}}
.stFormSubmitButton button:hover {{
  opacity:0.88 !important;
  transform:translateY(-2px) !important;
  box-shadow:0 8px 24px {TA('accent','44')} !important;
}}
.stAlert {{ border-radius:10px !important; }}

/* ═══════════════════════════════════════════
   FOOTER
═══════════════════════════════════════════ */
.footer {{
  text-align:center;
  padding:3rem 2rem;
  border-top:1px solid {T['border']};
  color:{T['muted']};
  font-size:0.875rem;
  background:{T['bg']};
  position:relative;
}}
.footer strong {{ color:{T['text']}; }}
.footer a {{ color:{T['accent']}; text-decoration:none; transition:opacity 0.2s; }}
.footer a:hover {{ opacity:0.75; }}
.footer-links {{ display:flex; gap:1.25rem; justify-content:center; margin-bottom:1rem; }}
.footer-link-icon {{
  width:38px; height:38px;
  border-radius:50%;
  background:{T['card']};
  border:1px solid {T['border']};
  display:inline-flex; align-items:center; justify-content:center;
  color:{T['text']};
  text-decoration:none;
  transition:all 0.25s ease;
  font-size:1rem;
}}
.footer-link-icon:hover {{
  border-color:{T['accent']};
  color:{T['accent']};
  transform:translateY(-3px);
  box-shadow:0 6px 18px {TA('accent','33')};
}}
.back-to-top {{
  position:fixed;
  bottom:1.75rem;
  right:1.75rem;
  width:44px; height:44px;
  border-radius:50%;
  background:linear-gradient(135deg,{T['accent']},{T['accent2']});
  color:#fff;
  display:flex; align-items:center; justify-content:center;
  font-size:1.1rem;
  cursor:pointer;
  opacity:0;
  transform:translateY(12px);
  transition:all 0.35s ease;
  box-shadow:0 4px 20px {TA('accent','55')};
  z-index:999;
  text-decoration:none;
}}
.back-to-top.visible {{
  opacity:1;
  transform:translateY(0);
}}
.back-to-top:hover {{ transform:translateY(-3px) scale(1.1); }}

/* Hide Streamlit elements */
div[data-testid="stRadio"] {{ display:none !important; }}
div.row-widget.stRadio {{ display:none !important; }}

</style>
"""

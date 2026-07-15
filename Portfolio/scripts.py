"""
Client-side JavaScript for the portfolio page: nav/scroll effects, theme
toggle, typing animation, particle canvas, certificate modal, etc.

Split out of app.py to keep page layout/content separate from behavior.
This is plain JS with no Python interpolation, so it is just a constant —
pass it straight to st.html(PAGE_SCRIPT, unsafe_allow_javascript=True).
"""

PAGE_SCRIPT = """
<script>
(function() {
  /* st.html() with unsafe_allow_javascript=True renders inline in the
     main page — document IS the Streamlit app's document, no parent needed. */
  var D = document;
  var W = window;

  /* Mark body so CSS can safely hide .reveal elements */
  D.body.classList.add('js-ready');

  /* ══════════════════════════════════════════════════════
     CERTIFICATE MODAL — close helper (defined early for keydown)
  ══════════════════════════════════════════════════════ */
  function _closeCertModal() {
    var m = D.getElementById('cert-modal');
    var f = D.getElementById('cert-modal-iframe');
    if (m) m.style.display = 'none';
    if (f) f.src = '';
    D.body.style.overflow = '';
  }

  /* Escape key — safe to register on document immediately */
  D.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') _closeCertModal();
  });

  /* View-certificate buttons — event delegation on document (no element lookup needed) */
  D.addEventListener('click', function(e) {
    var btn = e.target.closest('.view-cert');
    if (!btn) return;
    var m = D.getElementById('cert-modal');
    var f = D.getElementById('cert-modal-iframe');
    var t = D.getElementById('cert-modal-title');
    var l = D.getElementById('cert-modal-loading');
    if (m && f) {
      if (t) t.textContent = btn.dataset.name;
      if (l) l.style.display = 'flex';
      f.src = 'https://docs.google.com/viewer?url=' + encodeURIComponent(btn.dataset.url) + '&embedded=true';
      m.style.display = 'flex';
      D.body.style.overflow = 'hidden';
    }
  });

  /* Horizontal scroll arrows — event delegation on document */
  D.addEventListener('click', function(e) {
    var btn = e.target.closest('.scroll-arrow-btn');
    if (!btn || !btn.dataset.track) return;
    var track = D.getElementById(btn.dataset.track);
    if (!track) return;
    var item = track.querySelector('.proj-scroll-item,.cert-scroll-item');
    var cardW = item ? (item.offsetWidth + 20) : 290;
    track.scrollBy({ left: parseInt(btn.dataset.dir) * cardW * 2, behavior: 'smooth' });
  });

  /* ── Wait for Streamlit to finish mounting ── */
  function init() {

    /* ═══ 0. ELEMENT-SPECIFIC LISTENERS (need DOM to be ready) ═══ */

    /* Theme toggle */
    var _themeBtn = D.getElementById('nav-theme-btn');
    if (_themeBtn) {
      _themeBtn.addEventListener('click', function() {
        /* Instant, purely client-side theme switch: flip the data-theme
           attribute (all colors are CSS vars keyed off it — see the
           :root[data-theme] rules) and swap the icon. No Streamlit rerun,
           no navigation, no network round-trip — just a style recalc. */
        var root = D.documentElement;
        var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
        root.setAttribute('data-theme', next);
        _themeBtn.textContent = next === 'dark' ? '☀️' : '🌙';

        /* Keep the URL in sync (for shareable/refreshable links) without
           triggering any rerun or navigation. */
        var p = new URLSearchParams(location.search);
        p.set('theme', next);
        window.history.replaceState({}, '', location.pathname + '?' + p.toString());
      });
    }

    /* Modal close button */
    var _closeBtn = D.getElementById('cert-modal-close');
    if (_closeBtn) _closeBtn.addEventListener('click', _closeCertModal);

    /* Modal backdrop click */
    var _modal = D.getElementById('cert-modal');
    if (_modal) {
      _modal.addEventListener('click', function(e) {
        if (e.target === _modal) _closeCertModal();
      });
    }

    /* iframe onload — hide spinner */
    var _certIframe = D.getElementById('cert-modal-iframe');
    if (_certIframe) {
      _certIframe.addEventListener('load', function() {
        var l = D.getElementById('cert-modal-loading');
        if (l) l.style.display = 'none';
      });
    }

    /* ═══ 1. TYPING ANIMATION ═══ */
    const phrases = [
      "Building AI-powered applications",
      "Turning data into insights",
      "Creating elegant Python solutions",
      "Exploring Machine Learning",
      "Crafting seamless user experiences",
    ];
    const el = D.getElementById('typed-text');
    if (el) {
      let pi = 0, ci = 0, deleting = false;
      function typeStep() {
        const phrase = phrases[pi];
        if (!deleting) {
          el.textContent = phrase.slice(0, ++ci);
          if (ci === phrase.length) { deleting = true; setTimeout(typeStep, 1800); return; }
          setTimeout(typeStep, 55);
        } else {
          el.textContent = phrase.slice(0, --ci);
          if (ci === 0) { deleting = false; pi = (pi + 1) % phrases.length; setTimeout(typeStep, 300); return; }
          setTimeout(typeStep, 28);
        }
      }
      typeStep();
    }

    /* ═══ 2. SCROLL-REVEAL ═══ */
    const _scrollRoot = D.querySelector('[data-testid="stAppViewContainer"]') || null;
    const _revealIO = new IntersectionObserver(
      function(entries) {
        entries.forEach(function(e) {
          if (e.isIntersecting) {
            e.target.classList.add('revealed');
            _revealIO.unobserve(e.target);
          }
        });
      },
      { root: _scrollRoot, rootMargin: '0px 0px -6% 0px', threshold: 0.06 }
    );
    D.querySelectorAll('.reveal,.reveal-left,.reveal-right,.reveal-scale')
      .forEach(function(el) { _revealIO.observe(el); });

    /* ═══ 3. SCI-FI PROGRESS BAR + NAV ACTIVE ═══ */
    const SECTION_IDS    = ['home','skills','portfolio','certifications','contact'];
    const SECTION_LABELS = ['HOME','SKILLS','PROJECTS','CERTS','CONTACT'];
    const navLinks = D.querySelectorAll('.nav-link');
    const fill  = D.getElementById('scifi-bar-fill');
    const track = D.getElementById('scifi-bar-track');


    /* ── rAF progress bar: pure getBoundingClientRect — no scroll-container guessing ──
       How it works: section tops move UP (go negative) as the user scrolls DOWN.
       A section is "active" when its top <= TRIGGER px from viewport top.
       Segment progress = how far we've scrolled through the gap to the next section. ── */
    const TRIGGER    = 120;   /* px from viewport top that makes a section "active" */
    const last       = SECTION_IDS.length - 1;

    let _barTarget  = 0;
    let _barCurrent = 0;
    let _lastSec    = -1;

    function calcBar() {
      let cur = 0, seg = 0;
      for (let i = last; i >= 0; i--) {
        const el = D.getElementById(SECTION_IDS[i]);
        if (!el) continue;
        const top = el.getBoundingClientRect().top;
        if (top <= TRIGGER) {
          cur = i;
          if (i < last) {
            const nxt = D.getElementById(SECTION_IDS[i + 1]);
            if (nxt) {
              /* gap = distance between adjacent section tops (constant while scrolling) */
              const gap = Math.max(nxt.getBoundingClientRect().top - top, 1);
              seg = Math.min(Math.max((TRIGGER - top) / gap, 0), 1);
            }
          }
          break;
        }
      }
      return { pct: Math.min(Math.max((cur + seg) / last * 100, 0), 100), cur };
    }

    function barLoop() {
      if (fill) {
        const { pct, cur } = calcBar();
        _barTarget = pct;

        /* Lerp toward target — feels instant on slow scroll, smooth on fast */
        const diff = _barTarget - _barCurrent;
        _barCurrent += diff * 0.2;
        if (Math.abs(diff) < 0.01) _barCurrent = _barTarget;

        fill.style.width = _barCurrent.toFixed(3) + '%';

        /* Update nav only when section changes */
        if (cur !== _lastSec) {
          _lastSec = cur;
          navLinks.forEach(function(link) {
            link.classList.toggle('active',
              link.dataset.section === SECTION_IDS[cur]);
          });
        }
      }
      W.requestAnimationFrame(barLoop);
    }

    W.requestAnimationFrame(barLoop);

    /* ═══ 4. NAV LINK RIPPLE ═══ */
    navLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        const ripple = D.createElement('span');
        const rect = this.getBoundingClientRect();
        ripple.className = 'ripple';
        ripple.style.width = ripple.style.height = '80px';
        ripple.style.left = (e.clientX - rect.left - 40) + 'px';
        ripple.style.top  = (e.clientY - rect.top  - 40) + 'px';
        this.appendChild(ripple);
        setTimeout(() => ripple.remove(), 700);
      });
    });

    /* ═══ 5. BACK TO TOP BUTTON ═══ */
    const btt = D.getElementById('back-to-top');
    if (btt) {
      const scrollEl = D.querySelector('[data-testid="stAppViewContainer"]')
                     || D.querySelector('section.main')
                     || W;
      const checkScroll = () => {
        const st = scrollEl === W ? W.pageYOffset : scrollEl.scrollTop;
        btt.classList.toggle('visible', st > 350);
      };
      scrollEl.addEventListener('scroll', checkScroll, { passive: true });
    }

    /* ═══ 6. STAT NUMBER COUNTER ═══ */
    const statNums = D.querySelectorAll('.stat-num');
    const countObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        const el = e.target;
        const raw = el.textContent.replace(/[^0-9]/g,'');
        const target = parseInt(raw) || 0;
        const suffix = el.textContent.replace(/[0-9]/g,'');
        let current = 0;
        const step = Math.ceil(target / 40);
        const timer = setInterval(() => {
          current = Math.min(current + step, target);
          el.textContent = current + suffix;
          if (current >= target) clearInterval(timer);
        }, 30);
        countObs.unobserve(el);
      });
    }, { threshold: 0.8 });
    statNums.forEach(el => countObs.observe(el));


    /* ═══ 8. CERT CARD TILT ═══ */
    D.querySelectorAll('.cert-card').forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const dx = (e.clientX - rect.left - rect.width  / 2) / (rect.width  / 2);
        const dy = (e.clientY - rect.top  - rect.height / 2) / (rect.height / 2);
        card.style.transform = `translateY(-6px) scale(1.01) rotateX(${-dy*4}deg) rotateY(${dx*4}deg)`;
      });
      card.addEventListener('mouseleave', () => { card.style.transform = ''; });
    });

    /* ═══ 9. PARTICLE CANVAS in hero ═══ */
    const hero = D.querySelector('.hero');
    if (hero) {
      const canvas = D.createElement('canvas');
      canvas.id = 'particles-canvas';
      hero.insertBefore(canvas, hero.firstChild);
      const ctx = canvas.getContext('2d');
      const pColor = 'rgba(121,192,255,';
      let particles = [];
      function resize() { canvas.width = hero.offsetWidth; canvas.height = hero.offsetHeight; }
      resize();
      W.addEventListener('resize', () => { resize(); spawnParticles(); });
      function spawnParticles() {
        particles = [];
        const count = Math.floor(canvas.width / 18);
        for (let i = 0; i < count; i++) {
          particles.push({
            x: Math.random() * canvas.width, y: Math.random() * canvas.height,
            r: Math.random() * 2 + 0.5,
            vx: (Math.random() - 0.5) * 0.4, vy: -(Math.random() * 0.6 + 0.2),
            opacity: Math.random() * 0.5 + 0.1,
          });
        }
      }
      spawnParticles();
      function drawParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fillStyle = pColor + p.opacity + ')';
          ctx.fill();
          p.x += p.vx; p.y += p.vy;
          if (p.y < -5) { p.y = canvas.height + 5; p.x = Math.random() * canvas.width; }
          if (p.x < 0) p.x = canvas.width;
          if (p.x > canvas.width) p.x = 0;
        });
        requestAnimationFrame(drawParticles);
      }
      drawParticles();
    }
  }

  /* Run after Streamlit mounts */
  setTimeout(init, 600);
})();
</script>
"""

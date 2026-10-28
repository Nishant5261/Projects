"""
Client-side JavaScript for the portfolio page: nav/scroll effects, theme
toggle, typing animation, particle canvas, certificate modal, card tap-flip, etc.
"""

PAGE_SCRIPT = """
<script>
(function() {
  var W = (window.parent && window.parent !== window) ? window.parent : window;
  var D = W.document;
  var IO = W.IntersectionObserver || IntersectionObserver;

  /* Mark body so CSS can safely hide .reveal elements */
  if (D.body) D.body.classList.add('js-ready');

  /* Sync initial data-theme attribute on <html> from URL or theme button icon */
  (function syncInitialTheme() {
    var root = D.documentElement;
    if (!root.getAttribute('data-theme')) {
      var qp = new URLSearchParams(W.location.search).get('theme');
      if (qp === 'light' || qp === 'dark') {
        root.setAttribute('data-theme', qp);
      } else {
        var btn = D.getElementById('nav-theme-btn');
        var isDark = !btn || btn.textContent.indexOf('☀️') !== -1;
        root.setAttribute('data-theme', isDark ? 'dark' : 'light');
      }
    }
  })();

  /* ══════════════════════════════════════════════════════
     CERTIFICATE MODAL — close helper
  ══════════════════════════════════════════════════════ */
  function _closeCertModal() {
    var m = D.getElementById('cert-modal');
    var f = D.getElementById('cert-modal-iframe');
    if (m) m.style.display = 'none';
    if (f) f.src = '';
    if (D.body) D.body.style.overflow = '';
  }

  D.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      _closeCertModal();
      D.querySelectorAll('.proj-scroll-item.is-flipped').forEach(function(item) {
        item.classList.remove('is-flipped');
      });
    }
  });

  function _normalizeCertUrl(url) {
    if (!url) return '';
    url = String(url).trim();
    if (!url) return '';
    if (/^https?:\\/\\/github\\.com\\//i.test(url) && /\\/blob\\//i.test(url)) {
      return url.replace('https://github.com/', 'https://raw.githubusercontent.com/').replace('/blob/', '/');
    }
    return url;
  }

  function _setMobileMenu(open) {
    var panel = D.getElementById('mobile-nav-panel');
    var btn = D.getElementById('nav-menu-btn');
    if (!panel || !btn) return;
    panel.classList.toggle('open', open);
    panel.setAttribute('aria-hidden', open ? 'false' : 'true');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  D.addEventListener('click', function(e) {
    var menuBtn = e.target.closest('#nav-menu-btn');
    if (menuBtn) {
      var panel = D.getElementById('mobile-nav-panel');
      if (panel) {
        var open = !panel.classList.contains('open');
        _setMobileMenu(open);
      }
      return;
    }
    if (e.target.closest('.mobile-nav-link')) {
      _setMobileMenu(false);
      return;
    }
    if (D.getElementById('mobile-nav-panel') && D.getElementById('mobile-nav-panel').classList.contains('open') && !e.target.closest('.mobile-nav-panel') && !e.target.closest('.nav-bar')) {
      _setMobileMenu(false);
    }

    var projItem = e.target.closest('.proj-scroll-item');
    if (projItem && !e.target.closest('a')) {
      projItem.classList.toggle('is-flipped');
    } else if (!projItem) {
      D.querySelectorAll('.proj-scroll-item.is-flipped').forEach(function(el) {
        el.classList.remove('is-flipped');
      });
    }
  });

  W.addEventListener('resize', function() {
    if (W.innerWidth > 900) _setMobileMenu(false);
  });

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
      var certUrl = _normalizeCertUrl(btn.dataset.url);
      f.src = 'https://docs.google.com/viewer?url=' + encodeURIComponent(certUrl) + '&embedded=true';
      m.style.display = 'flex';
      if (D.body) D.body.style.overflow = 'hidden';
    }
  });

  function _updateTrackArrows(trackId) {
    var track = D.getElementById(trackId);
    if (!track) return;
    var leftBtn = D.querySelector('.scroll-arrow-btn[data-track="' + trackId + '"][data-dir="-1"]');
    var rightBtn = D.querySelector('.scroll-arrow-btn[data-track="' + trackId + '"][data-dir="1"]');
    var maxScroll = track.scrollWidth - track.clientWidth;
    if (leftBtn) leftBtn.disabled = track.scrollLeft <= 4;
    if (rightBtn) rightBtn.disabled = track.scrollLeft >= maxScroll - 4;
  }

  D.addEventListener('click', function(e) {
    var btn = e.target.closest('.scroll-arrow-btn');
    if (!btn || !btn.dataset.track) return;
    var track = D.getElementById(btn.dataset.track);
    if (!track) return;
    var item = track.querySelector('.proj-scroll-item,.cert-scroll-item');
    var cardW = item ? (item.offsetWidth + 20) : 290;
    track.scrollBy({ left: parseInt(btn.dataset.dir) * cardW * 2, behavior: 'smooth' });
  });

  /* ── Robust Initialization with Polling for Streamlit Elements ── */
  function init() {
    ['proj-track', 'cert-track'].forEach(function(tid) {
      var tr = D.getElementById(tid);
      if (tr) {
        tr.addEventListener('scroll', function() { _updateTrackArrows(tid); }, { passive: true });
        _updateTrackArrows(tid);
      }
    });
    W.addEventListener('resize', function() {
      _updateTrackArrows('proj-track');
      _updateTrackArrows('cert-track');
    });

    /* Theme toggle */
    var _themeBtn = D.getElementById('nav-theme-btn');
    if (_themeBtn && !_themeBtn.dataset.bound) {
      _themeBtn.dataset.bound = '1';
      _themeBtn.addEventListener('click', function() {
        var root = D.documentElement;
        var current = root.getAttribute('data-theme') || 'dark';
        var next = current === 'light' ? 'dark' : 'light';
        root.setAttribute('data-theme', next);
        _themeBtn.textContent = next === 'dark' ? '☀️' : '🌙';

        var p = new URLSearchParams(W.location.search);
        p.set('theme', next);
        W.history.replaceState({}, '', W.location.pathname + '?' + p.toString());
      });
    }

    var _closeBtn = D.getElementById('cert-modal-close');
    if (_closeBtn) _closeBtn.addEventListener('click', _closeCertModal);

    var _modal = D.getElementById('cert-modal');
    if (_modal) {
      _modal.addEventListener('click', function(e) {
        if (e.target === _modal) _closeCertModal();
      });
    }

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
      "Exploring Machine Learning & LLMs",
      "Crafting seamless user experiences",
    ];
    const el = D.getElementById('typed-text');
    if (el && !el.dataset.bound) {
      el.dataset.bound = '1';
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
    const _revealIO = new IO(
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

    /* ═══ 3. SCI-FI PROGRESS BAR + NAV ACTIVE (With Polling for DOM readiness) ═══ */
    const SECTION_IDS = ['home','skills','portfolio','certifications','contact'];
    const navLinks = D.querySelectorAll('.nav-link');
    const TRIGGER = 120;
    const last = SECTION_IDS.length - 1;

    let _barTarget  = 0;
    let _barCurrent = 0;
    let _lastSec    = -1;

    function calcBar() {
      let cur = 0, seg = 0;
      for (let i = last; i >= 0; i--) {
        const sectEl = D.getElementById(SECTION_IDS[i]);
        if (!sectEl) continue;
        const top = sectEl.getBoundingClientRect().top;
        if (top <= TRIGGER) {
          cur = i;
          if (i < last) {
            const nxt = D.getElementById(SECTION_IDS[i + 1]);
            if (nxt) {
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
      const fill = D.getElementById('scifi-bar-fill');
      if (fill) {
        const { pct, cur } = calcBar();
        _barTarget = pct;

        const diff = _barTarget - _barCurrent;
        _barCurrent += diff * 0.2;
        if (Math.abs(diff) < 0.01) _barCurrent = _barTarget;

        fill.style.width = _barCurrent.toFixed(3) + '%';

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
      if (link.dataset.rippleBound) return;
      link.dataset.rippleBound = '1';
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
    const countObs = new IO((entries) => {
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

    /* ═══ 7. THEME-AWARE PARTICLE CANVAS (Polling for .hero element) ═══ */
    function setupParticles() {
      const hero = D.querySelector('.hero');
      if (hero && !D.getElementById('particles-canvas')) {
        const canvas = D.createElement('canvas');
        canvas.id = 'particles-canvas';
        hero.insertBefore(canvas, hero.firstChild);
        const ctx = canvas.getContext('2d');
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
          const isLight = D.documentElement.getAttribute('data-theme') === 'light';
          const pColor = isLight ? 'rgba(79,70,229,' : 'rgba(121,192,255,';
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
          W.requestAnimationFrame(drawParticles);
        }
        drawParticles();
        return true;
      }
      return false;
    }

    /* Retry until hero renders if Streamlit delays DOM insertion */
    if (!setupParticles()) {
      var tries = 0;
      var pollInterval = setInterval(function() {
        tries++;
        if (setupParticles() || tries > 20) {
          clearInterval(pollInterval);
        }
      }, 250);
    }
  }

  /* Trigger init with multi-stage fallbacks for Streamlit render timing */
  if (D.readyState === 'complete') {
    setTimeout(init, 100);
  } else {
    W.addEventListener('load', function() { setTimeout(init, 100); });
    setTimeout(init, 600);
  }
})();
</script>
"""

/* ================================================================
   JUSTJOIN.IT — UNIFIED JAVASCRIPT  (main.js)
   Covers: job-offers page + job-detail page
   Cleaned: duplicates removed, bugs fixed
   ================================================================ */

/* ── THEME TOGGLE ── */
const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
  if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark');
    themeToggle.textContent = '🌙';
  }
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    const isDark = document.body.classList.contains('dark');
    themeToggle.textContent = isDark ? '🌙' : '☀';
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  });
}


/* ── SIGN IN DROPDOWN ── */
const signinToggle   = document.getElementById('signinToggle');
const signinDropdown = document.getElementById('signinDropdown');
const signinWrap     = document.getElementById('signinWrap');

if (signinToggle && signinDropdown) {
  signinToggle.addEventListener('click', e => {
    e.stopPropagation();
    signinDropdown.classList.toggle('open');
  });
  document.addEventListener('click', e => {
    if (signinWrap && !signinWrap.contains(e.target))
      signinDropdown.classList.remove('open');
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') signinDropdown.classList.remove('open');
  });
}


/* ── LEFT BAR ACTIVE STATE ── */
document.querySelectorAll('.lb-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.lb-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});


/* ── FILTER ACCORDION ── */
document.querySelectorAll('.f-head').forEach(head => {
  head.addEventListener('click', () => {
    const body = document.getElementById(head.dataset.target);
    const chev = head.querySelector('.chevron');
    if (!body) return;
    const hiding = !body.classList.contains('hidden');
    body.classList.toggle('hidden', hiding);
    if (chev) chev.classList.toggle('closed', hiding);
  });
});


/* ── FILTER TAGS (URL param based) ── */
function buildFilterUrl(paramName, value) {
  const params   = new URLSearchParams(window.location.search);
  const existing = params.getAll(paramName);
  params.delete(paramName);
  if (existing.includes(value)) {
    existing.filter(v => v !== value).forEach(v => params.append(paramName, v));
  } else {
    existing.forEach(v => params.append(paramName, v));
    params.append(paramName, value);
  }
  return `${window.location.pathname}?${params.toString()}`;
}

document.querySelectorAll('.f-tag').forEach(tag => {
  tag.addEventListener('click', () => {
    window.location.href = buildFilterUrl(tag.dataset.group, tag.dataset.filter);
  });
});


/* ── SALARY ONLY CHECKBOX ── */
const salaryOnlyCheck = document.getElementById('salaryOnlyCheck');
if (salaryOnlyCheck) {
  salaryOnlyCheck.addEventListener('change', () => {
    const params = new URLSearchParams(window.location.search);
    salaryOnlyCheck.checked ? params.set('salary_only', '1') : params.delete('salary_only');
    window.location.href = `${window.location.pathname}?${params.toString()}`;
  });
}


/* ── SEARCH ── */
document.querySelector('.search-btn')?.addEventListener('click', () => {
  const q   = document.getElementById('searchKeyword')?.value.trim()  || '';
  const loc = document.getElementById('searchLocation')?.value.trim() || '';
  const params = new URLSearchParams(window.location.search);
  q   ? params.set('q', q)         : params.delete('q');
  loc ? params.set('location', loc) : params.delete('location');
  window.location.href = `${window.location.pathname}?${params.toString()}`;
});

/* Enter key in search inputs */
['searchKeyword', 'searchLocation'].forEach(id => {
  document.getElementById(id)?.addEventListener('keydown', e => {
    if (e.key === 'Enter') document.querySelector('.search-btn')?.click();
  });
});


/* ── BOOKMARKS (job-offers list) ── */
document.addEventListener('click', e => {
  const btn = e.target.closest('.bm-btn');
  if (!btn) return;
  e.stopPropagation();
  btn.classList.toggle('saved');
  const path = btn.querySelector('path');
  if (path) path.setAttribute('fill', btn.classList.contains('saved') ? 'currentColor' : 'none');
  btn.style.transform = 'scale(1.3)';
  setTimeout(() => { btn.style.transform = ''; }, 180);
});


/* ── SORT (job-offers) ── */
document.getElementById('sortSelect')?.addEventListener('change', function () {
  const list = document.getElementById('jobsList');
  if (!list) return;
  const cards = [...list.querySelectorAll('.job-card')];

  if (this.value === 'Newest') {
    cards.reverse().forEach(c => list.appendChild(c));
  } else if (this.value === 'Salary: High to Low') {
    cards.sort((a, b) => {
      const getSal = el => {
        const s = el.querySelector('.salary:not(.undisclosed)');
        if (!s) return 0;
        const m = s.textContent.match(/[\d\s]+/);
        return m ? parseInt(m[0].replace(/\s/g, '')) : 0;
      };
      return getSal(b) - getSal(a);
    }).forEach(c => list.appendChild(c));
  }

  list.querySelectorAll('.job-card:not(.hidden)').forEach((card, i) => {
    card.style.animationDelay = `${i * .05}s`;
    card.style.animation = 'none';
    card.offsetHeight; // reflow
    card.style.animation = 'fadeUp .3s ease both';
  });
});


/* ── MAP BUTTON ── */
document.getElementById('mapBtn')?.addEventListener('click', () => {
  console.log('Map view requested');
});


/* ── KEYBOARD SHORTCUTS ── */
document.addEventListener('keydown', e => {
  const active = document.activeElement.tagName;
  if (active === 'INPUT' || active === 'TEXTAREA') return;

  if (e.key === '/') {
    e.preventDefault();
    document.getElementById('searchKeyword')?.focus();
  }
  // B = bookmark (detail page)
  if (e.key === 'b') {
    document.querySelector('.save-btn')?.click();
  }
});


/* ════════════════════════════════
   DETAIL PAGE SPECIFIC
════════════════════════════════ */

/* ── PROGRESS BAR ANIMATE ── */
const progressFill = document.querySelector('.progress-fill');
if (progressFill) {
  // CSS transition handles it — just trigger after paint
  requestAnimationFrame(() => {
    setTimeout(() => { progressFill.style.width = '65%'; }, 300);
  });
}


/* ── TOAST ── */
function showToast(message) {
  document.querySelectorAll('.jj-toast').forEach(t => t.remove());
  const toast = document.createElement('div');
  toast.className = 'jj-toast';
  toast.textContent = message;
  Object.assign(toast.style, {
    position: 'fixed', bottom: '28px', left: '50%',
    transform: 'translateX(-50%) translateY(12px)',
    background: '#1e1e30', color: '#f0f0ff',
    padding: '10px 20px', borderRadius: '50px',
    fontSize: '13px', fontWeight: '500', fontFamily: 'inherit',
    border: '1px solid rgba(255,255,255,.1)',
    boxShadow: '0 8px 32px rgba(0,0,0,.4)',
    zIndex: '9999', opacity: '0',
    transition: 'opacity .2s ease, transform .2s ease',
    pointerEvents: 'none', whiteSpace: 'nowrap',
  });
  document.body.appendChild(toast);
  requestAnimationFrame(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';
  });
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(-50%) translateY(8px)';
    setTimeout(() => toast.remove(), 220);
  }, 2200);
}


/* ── SAVE BUTTON (detail sidebar) ── */
const saveBtn = document.querySelector('.save-btn');
if (saveBtn) {
  saveBtn.addEventListener('click', () => {
    const saved = saveBtn.classList.toggle('saved');
    const path  = saveBtn.querySelector('path');
    if (path) path.setAttribute('fill', saved ? 'currentColor' : 'none');
    saveBtn.style.transform = 'scale(.92)';
    setTimeout(() => { saveBtn.style.transform = ''; }, 150);
    showToast(saved ? 'Saved to your list' : 'Removed from list');
  });
}


/* ── ACTION BUTTONS (Save / Share in sidebar) ── */
document.querySelectorAll('.action-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const isShare = btn.textContent.trim().startsWith('Share');
    if (isShare) { handleShare(); return; }
    const saved = btn.classList.toggle('saved');
    const icon  = btn.querySelector('path');
    if (icon) icon.setAttribute('fill', saved ? 'currentColor' : 'none');
    showToast(saved ? 'Saved to your list' : 'Removed from list');
  });
});


/* ── SIMILAR OFFERS BOOKMARK ── */
document.querySelectorAll('.sim-bm').forEach(btn => {
  btn.addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    const saved = btn.classList.toggle('saved');
    const path  = btn.querySelector('path');
    if (path) path.setAttribute('fill', saved ? 'currentColor' : 'none');
    btn.style.transform = 'scale(1.3)';
    setTimeout(() => { btn.style.transform = ''; }, 160);
  });
});


/* ── APPLY BUTTON RIPPLE ── */
document.querySelectorAll('.apply-btn, .apply-full-btn, .summary-apply-btn').forEach(btn => {
  btn.addEventListener('click', function (e) {
    const ripple = document.createElement('span');
    Object.assign(ripple.style, {
      position: 'absolute', borderRadius: '50%', transform: 'scale(0)',
      animation: 'ripple .5s linear', background: 'rgba(255,255,255,.35)',
      width: '100px', height: '100px',
      left: `${e.offsetX - 50}px`, top: `${e.offsetY - 50}px`,
      pointerEvents: 'none',
    });
    this.style.position = 'relative';
    this.style.overflow = 'hidden';
    this.appendChild(ripple);
    setTimeout(() => ripple.remove(), 500);
  });
});


/* ── SHARE ── */
function handleShare() {
  if (navigator.share) {
    navigator.share({ title: document.title, url: window.location.href }).catch(() => {});
  } else {
    navigator.clipboard.writeText(window.location.href)
      .then(() => showToast('Link copied to clipboard!'))
      .catch(() => showToast('Copy the URL from address bar'));
  }
}


/* ── SCROLL FADE IN (tech-items, pills, similar-cards) ── */
const fadeObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity  = '1';
      entry.target.style.transform = 'translateY(0)';
      fadeObserver.unobserve(entry.target);
    }
  });
}, { threshold: .1 });

document.querySelectorAll('.tech-item, .pill').forEach((el, i) => {
  el.style.cssText += 'opacity:0;transform:translateY(10px);transition:opacity .35s ease,transform .35s ease;';
  el.style.transitionDelay = `${i * .04}s`;
  fadeObserver.observe(el);
});


/* ── TECH STACK SORT (highest level first) ── */
document.addEventListener('DOMContentLoaded', () => {
  const levelOrder = { master: 5, advanced: 4, regular: 3, junior: 2, 'nice to have': 1 };
  const grid = document.querySelector('.tech-grid');
  if (!grid) return;

  const items = [...grid.querySelectorAll('.stack-item')];
  items.sort((a, b) => {
    const lvA = a.querySelector('.tech-level')?.innerText.trim().toLowerCase() || '';
    const lvB = b.querySelector('.tech-level')?.innerText.trim().toLowerCase() || '';
    return (levelOrder[lvB] || 0) - (levelOrder[lvA] || 0);
  });
  items.forEach(item => grid.appendChild(item));
});
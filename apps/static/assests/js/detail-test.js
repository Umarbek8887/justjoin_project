

const themeToggleBtn = document.getElementById('themeToggle');
if (themeToggleBtn) {
  if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark');
    themeToggleBtn.textContent = '🌙';
  }
  themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    const isDark = document.body.classList.contains('dark');
    themeToggleBtn.textContent = isDark ? '🌙' : '☀';
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  });
}

// ── LEFT BAR ACTIVE STATE ─────────────────────────
document.querySelectorAll('.lb-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.lb-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});


// ── SAVE / BOOKMARK (sticky bar) ─────────────────
const saveBtn = document.querySelector('.save-btn');
if (saveBtn) {
  saveBtn.addEventListener('click', () => {
    const saved = saveBtn.classList.toggle('saved');
    const path = saveBtn.querySelector('path');
    if (path) path.setAttribute('fill', saved ? 'currentColor' : 'none');

    // Ripple bounce
    saveBtn.style.transform = 'scale(0.92)';
    setTimeout(() => { saveBtn.style.transform = ''; }, 150);

    showToast(saved ? 'Saved to your list' : 'Removed from list');
  });
}


// ── ACTION SAVE BUTTON (sidebar) ─────────────────
const actionBtns = document.querySelectorAll('.action-btn');
actionBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const icon = btn.querySelector('path');
    if (btn.title === 'Share' || btn.textContent.trim().startsWith('Share')) {
      handleShare();
      return;
    }
    const saved = btn.classList.toggle('saved');
    if (icon) icon.setAttribute('fill', saved ? 'currentColor' : 'none');
    showToast(saved ? 'Saved to your list' : 'Removed from list');
  });
});


// ── SIMILAR OFFERS BOOKMARK ───────────────────────
document.querySelectorAll('.sim-bm').forEach(btn => {
  btn.addEventListener('click', e => {
    e.stopPropagation();
    const saved = btn.classList.toggle('saved');
    const path = btn.querySelector('path');
    if (path) path.setAttribute('fill', saved ? 'currentColor' : 'none');

    btn.style.transform = 'scale(1.25)';
    setTimeout(() => { btn.style.transform = ''; }, 160);
  });
});


// ── SIMILAR CARD CLICK ────────────────────────────
document.querySelectorAll('.similar-card').forEach(card => {
  card.addEventListener('click', e => {
    if (e.target.closest('.sim-bm')) return;
    // Ripple before navigate (in real app link href would be used)
    card.style.opacity = '0.7';
    setTimeout(() => { card.style.opacity = ''; }, 200);
  });
});


// ── APPLY BUTTON RIPPLE ───────────────────────────
document.querySelectorAll('.apply-btn, .apply-full-btn').forEach(btn => {
  btn.addEventListener('click', function (e) {
    const ripple = document.createElement('span');
    ripple.style.cssText = `
      position:absolute; border-radius:50%; transform:scale(0);
      animation:ripple .5s linear; background:rgba(255,255,255,0.35);
      width:100px; height:100px;
      left:${e.offsetX - 50}px; top:${e.offsetY - 50}px; pointer-events:none;
    `;
    this.style.position = 'relative';
    this.style.overflow = 'hidden';
    this.appendChild(ripple);
    setTimeout(() => ripple.remove(), 500);
  });
});

// Inject ripple keyframe
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
  @keyframes ripple { to { transform:scale(3); opacity:0; } }
`;
document.head.appendChild(rippleStyle);


// ── PROGRESS BAR ANIMATE ──────────────────────────
const fill = document.querySelector('.progress-fill');
if (fill) {
  fill.style.width = '0';
  setTimeout(() => {
    fill.style.transition = 'width 1.2s cubic-bezier(0.4,0,0.2,1)';
    fill.style.width = '65%';
  }, 300);
}


// ── SHARE HANDLER ─────────────────────────────────
function handleShare() {
  if (navigator.share) {
    navigator.share({
      title: document.title,
      url: window.location.href,
    }).catch(() => { });
  } else {
    navigator.clipboard.writeText(window.location.href)
      .then(() => showToast('Link copied to clipboard!'))
      .catch(() => showToast('Copy the URL from address bar'));
  }
}

// Wire share button
const shareBtn = document.querySelector('.action-btn:last-child');
if (shareBtn) {
  shareBtn.addEventListener('click', handleShare);
}


// ── TOAST NOTIFICATION ────────────────────────────
function showToast(message) {
  // Remove existing
  document.querySelectorAll('.jj-toast').forEach(t => t.remove());

  const toast = document.createElement('div');
  toast.className = 'jj-toast';
  toast.textContent = message;
  toast.style.cssText = `
    position:fixed; bottom:28px; left:50%; transform:translateX(-50%) translateY(12px);
    background:#1e1e30; color:#f0f0ff;
    padding:10px 20px; border-radius:50px;
    font-size:13px; font-weight:500; font-family:inherit;
    border:1px solid rgba(255,255,255,0.1);
    box-shadow:0 8px 32px rgba(0,0,0,0.4);
    z-index:9999; opacity:0;
    transition:opacity 0.2s ease, transform 0.2s ease;
    pointer-events:none; white-space:nowrap;
  `;
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


// ── SCROLL FADE IN (tech items, similar cards) ────
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.tech-item, .similar-card, .pill').forEach((el, i) => {
  el.style.cssText += 'opacity:0; transform:translateY(10px); transition:opacity 0.35s ease, transform 0.35s ease;';
  el.style.transitionDelay = `${i * 0.04}s`;
  observer.observe(el);
});


// ── KEYBOARD SHORTCUT ─────────────────────────────
document.addEventListener('keydown', e => {
  // Escape: do nothing special (could hide modal in future)
  if (e.key === 'Escape') return;
  // B: toggle bookmark
  if (e.key === 'b' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
    saveBtn?.click();
  }
});

/* ==============================================
   TECH STACK SORTING (Eng yuqori darajalar tepaga)
   ============================================== */
document.addEventListener("DOMContentLoaded", function () {

    const order = {
        "master": 5,
        "advanced": 4,
        "regular": 3,
        "junior": 2,
        "nice to have": 1
    };

    const grid = document.querySelector(".tech-grid");

    // FAQAT tech stack elementlari
    const items = Array.from(grid.querySelectorAll(".stack-item"));

    items.sort((a, b) => {
        const levelA = a.querySelector(".tech-level")?.innerText.trim().toLowerCase();
        const levelB = b.querySelector(".tech-level")?.innerText.trim().toLowerCase();

        return (order[levelB] || 0) - (order[levelA] || 0);
    });

    items.forEach(item => grid.appendChild(item));
});

const signinToggle   = document.getElementById('signinToggle');
const signinDropdown = document.getElementById('signinDropdown');
const signinWrap     = document.getElementById('signinWrap');

if (signinToggle && signinDropdown) {
  signinToggle.addEventListener('click', (e) => {
    e.stopPropagation();
    signinDropdown.classList.toggle('open');
  });

  document.addEventListener('click', (e) => {
    if (signinWrap && !signinWrap.contains(e.target)) {
      signinDropdown.classList.remove('open');
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') signinDropdown.classList.remove('open');
  });
}
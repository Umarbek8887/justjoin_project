// ===== THEME TOGGLE =====
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


// ===== CATEGORY TABS =====
const catBtns = document.querySelectorAll('.cat');
catBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    catBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});


// ===== FILTER ACCORDION =====
document.querySelectorAll('.f-head').forEach(head => {
  head.addEventListener('click', () => {
    const id     = head.dataset.target;
    const body   = document.getElementById(id);
    const chev   = head.querySelector('.chevron');
    if (!body) return;

    const hiding = !body.classList.contains('hidden');
    body.classList.toggle('hidden', hiding);
    chev.classList.toggle('closed', hiding);
  });
});


/// ===== FILTER TAGS — URL param based =====
/**
 * Build a new URL by toggling a multi-value query param.
 * If the value already exists it is removed, otherwise it is added.
 * The `category` param is always preserved.
 */
function buildFilterUrl(paramName, value) {
  const params = new URLSearchParams(window.location.search);
  const existing = params.getAll(paramName);

  if (existing.includes(value)) {
    // Remove this value
    params.delete(paramName);
    existing.filter(v => v !== value).forEach(v => params.append(paramName, v));
  } else {
    params.append(paramName, value);
  }

  return `${window.location.pathname}?${params.toString()}`;
}

document.querySelectorAll('.f-tag').forEach(tag => {
  tag.addEventListener('click', () => {
    const group  = tag.dataset.group;   // e.g. "working_mode"
    const filter = tag.dataset.filter;  // e.g. "remote"
    window.location.href = buildFilterUrl(group, filter);
  });
});


// ===== SALARY CHECKBOX =====
const salaryOnlyCheck = document.getElementById('salaryOnlyCheck');
if (salaryOnlyCheck) {
  salaryOnlyCheck.addEventListener('change', () => {
    const params = new URLSearchParams(window.location.search);
    if (salaryOnlyCheck.checked) {
      params.set('salary_only', '1');
    } else {
      params.delete('salary_only');
    }
    window.location.href = `${window.location.pathname}?${params.toString()}`;
  });
}


// ===== SEARCH =====
document.querySelector('.search-btn')?.addEventListener('click', () => {
  const q   = document.getElementById('searchKeyword')?.value.trim()  || '';
  const loc = document.getElementById('searchLocation')?.value.trim() || '';
  const params = new URLSearchParams(window.location.search);
  if (q)   params.set('q', q); else params.delete('q');
  if (loc) params.set('location', loc); else params.delete('location');
  window.location.href = `${window.location.pathname}?${params.toString()}`;
});


// ===== BOOKMARKS =====
document.addEventListener('click', e => {
  const btn = e.target.closest('.bm-btn');
  if (!btn) return;

  e.stopPropagation();
  btn.classList.toggle('saved');

  // Fill/unfill icon
  const path = btn.querySelector('path');
  if (path) {
    path.setAttribute('fill', btn.classList.contains('saved') ? 'currentColor' : 'none');
  }

  // Bounce animation
  btn.style.transform = 'scale(1.3)';
  setTimeout(() => { btn.style.transform = ''; }, 180);
});


// ===== LEFT BAR ICON ACTIVE =====
document.querySelectorAll('.lb-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.lb-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});


// ===== SORT =====
document.getElementById('sortSelect')?.addEventListener('change', function () {
  const list  = document.getElementById('jobsList');
  if (!list) return;

  const cards = [...list.querySelectorAll('.job-card')];

  if (this.value === 'Newest') {
    cards.reverse().forEach(c => list.appendChild(c));
  } else if (this.value === 'Salary: High to Low') {
    cards.sort((a, b) => {
      const getSalary = el => {
        const s = el.querySelector('.salary:not(.undisclosed)');
        if (!s) return 0;
        const m = s.textContent.match(/[\d\s]+/);
        return m ? parseInt(m[0].replace(/\s/g, '')) : 0;
      };
      return getSalary(b) - getSalary(a);
    }).forEach(c => list.appendChild(c));
  }

  // Re-animate
  list.querySelectorAll('.job-card:not(.hidden)').forEach((card, i) => {
    card.style.animationDelay = `${i * 0.05}s`;
    card.style.animation = 'none';
    card.offsetHeight;
    card.style.animation = 'fadeUp 0.3s ease both';
  });
});


// ===== MAP BUTTON =====
document.getElementById('mapBtn')?.addEventListener('click', () => {
  // placeholder — Django view bilan integratsiya qilinadi
  console.log('Map view requested');
});


// ===== KEYBOARD SHORTCUT: / = focus search =====
document.addEventListener('keydown', e => {
  if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
    e.preventDefault();
    document.getElementById('searchKeyword')?.focus();
  }
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
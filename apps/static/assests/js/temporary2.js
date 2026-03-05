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


// ===== FILTER TAGS (multi-group single-select) =====
const activeFilters = {};

document.querySelectorAll('.f-tag').forEach(tag => {
  tag.addEventListener('click', () => {
    const group     = tag.dataset.group;
    const filter    = tag.dataset.filter;
    const wasActive = tag.classList.contains('active');

    // Deactivate all in same group
    document.querySelectorAll(`.f-tag[data-group="${group}"]`).forEach(t => t.classList.remove('active'));

    if (!wasActive) {
      tag.classList.add('active');
      activeFilters[group] = filter;
    } else {
      delete activeFilters[group];
    }

    applyFilters();
  });
});


// ===== SEARCH INPUT =====
const searchInput = document.getElementById('searchKeyword');
const locationInput = document.getElementById('searchLocation');

if (searchInput) searchInput.addEventListener('input', () => {
  clearTimeout(searchInput._timer);
  searchInput._timer = setTimeout(applyFilters, 200);
});

if (locationInput) locationInput.addEventListener('input', () => {
  clearTimeout(locationInput._timer);
  locationInput._timer = setTimeout(applyFilters, 200);
});

document.querySelector('.search-btn')?.addEventListener('click', applyFilters);


// ===== SALARY FILTER =====
const salaryOnly = document.getElementById('salaryOnly');
const salaryMin  = document.querySelector('.f-input');

if (salaryOnly) salaryOnly.addEventListener('change', applyFilters);
if (salaryMin)  salaryMin.addEventListener('input',   () => {
  clearTimeout(salaryMin._timer);
  salaryMin._timer = setTimeout(applyFilters, 300);
});


// ===== APPLY ALL FILTERS =====
function applyFilters() {
  const cards    = document.querySelectorAll('.job-card');
  const query    = searchInput?.value.toLowerCase().trim()    || '';
  const location = locationInput?.value.toLowerCase().trim()  || '';
  const onlySalary = salaryOnly?.checked || false;
  let visible = 0;

  cards.forEach((card, i) => {
    const mode     = card.dataset.mode     || '';
    const contract = card.dataset.contract || '';
    const text     = card.textContent.toLowerCase();

    const modeOk     = !activeFilters.mode     || mode === activeFilters.mode;
    const contractOk = !activeFilters.contract || contract === activeFilters.contract;
    const queryOk    = !query    || text.includes(query);
    const locOk      = !location || text.includes(location);

    // Salary: hide undisclosed if checkbox on
    const salaryEl  = card.querySelector('.salary');
    const hassalary = salaryEl && !salaryEl.classList.contains('undisclosed');
    const salaryOk  = !onlySalary || hassalary;

    const show = modeOk && contractOk && queryOk && locOk && salaryOk;

    if (show) {
      card.classList.remove('hidden');
      // Re-trigger fade animation
      card.style.animationDelay = `${visible * 0.04}s`;
      card.style.animation = 'none';
      card.offsetHeight; // reflow
      card.style.animation = '';
      visible++;
    } else {
      card.classList.add('hidden');
    }
  });

  updateCount(visible);
  showEmptyState(visible === 0);
}


// ===== UPDATE OFFER COUNT =====
function updateCount(n) {
  const el = document.getElementById('jobCount');
  if (!el) return;
  el.textContent = `${n.toLocaleString()} offers`;
}


// ===== EMPTY STATE =====
function showEmptyState(show) {
  let el = document.getElementById('emptyState');
  const list = document.getElementById('jobsList');
  if (!list) return;

  if (show && !el) {
    el = document.createElement('div');
    el.id = 'emptyState';
    el.className = 'empty-state';
    el.innerHTML = `
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
      <h3>No offers found</h3>
      <p>Try adjusting your filters or search terms to see more results.</p>
    `;
    list.after(el);
  } else if (!show && el) {
    el.remove();
  }
}


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
    searchInput?.focus();
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
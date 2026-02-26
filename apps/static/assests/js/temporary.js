// THEME
const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
  if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark');
    themeToggle.textContent = '🌙';
  }
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    const dark = document.body.classList.contains('dark');
    themeToggle.textContent = dark ? '🌙' : '☀';
    localStorage.setItem('theme', dark ? 'dark' : 'light');
  });
}

// CATEGORIES
document.querySelectorAll('.cat').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.cat').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

// FILTER ACCORDION
document.querySelectorAll('.f-head').forEach(head => {
  head.addEventListener('click', () => {
    const id = head.dataset.target;
    const body = document.getElementById(id);
    const chevron = head.querySelector('.chevron');
    if (!body) return;
    const hidden = body.classList.toggle('hidden');
    chevron.classList.toggle('closed', hidden);
  });
});

// FILTER TAGS
const active = {};
document.querySelectorAll('.f-tag').forEach(tag => {
  tag.addEventListener('click', () => {
    const group = tag.dataset.group;
    const filter = tag.dataset.filter;
    const wasActive = tag.classList.contains('active');

    document.querySelectorAll(`.f-tag[data-group="${group}"]`).forEach(t => t.classList.remove('active'));

    if (!wasActive) {
      tag.classList.add('active');
      active[group] = filter;
    } else {
      delete active[group];
    }
    applyFilters();
  });
});

// SEARCH
const searchKeyword = document.getElementById('searchKeyword');
if (searchKeyword) searchKeyword.addEventListener('input', applyFilters);

// APPLY FILTERS
function applyFilters() {
  const cards = document.querySelectorAll('.job-card');
  const query = searchKeyword?.value.toLowerCase().trim() || '';
  let count = 0;

  cards.forEach(card => {
    const mode = card.dataset.mode;
    const contract = card.dataset.contract;
    const text = card.textContent.toLowerCase();

    const modeOk = !active.mode || mode === active.mode;
    const contractOk = !active.contract || contract === active.contract;
    const queryOk = !query || text.includes(query);

    const show = modeOk && contractOk && queryOk;
    card.classList.toggle('hidden', !show);
    if (show) count++;
  });

  const countEl = document.getElementById('jobCount');
  if (countEl) countEl.textContent = count.toLocaleString() + ' offers';
}

// BOOKMARKS
document.querySelectorAll('.bm-btn').forEach(btn => {
  btn.addEventListener('click', e => {
    e.stopPropagation();
    btn.classList.toggle('saved');
    const path = btn.querySelector('path');
    if (path) path.setAttribute('fill', btn.classList.contains('saved') ? 'currentColor' : 'none');
  });
});

// LEFT BAR ICONS
document.querySelectorAll('.lb-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.lb-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});
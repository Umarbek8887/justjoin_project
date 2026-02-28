// THEME TOGGLE
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

// LEFT BAR ACTIVE STATE
document.querySelectorAll('.lb-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.lb-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

// BOOKMARK BUTTONS (similar offers)
document.querySelectorAll('.sim-bm').forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    btn.classList.toggle('saved');
    const path = btn.querySelector('path');
    if (path) path.setAttribute('fill', btn.classList.contains('saved') ? 'currentColor' : 'none');
    if (btn.classList.contains('saved')) {
      btn.style.color = 'var(--accent2)';
      btn.style.borderColor = 'var(--accent2)';
    } else {
      btn.style.color = '';
      btn.style.borderColor = '';
    }
  });
});

// SAVE BUTTON (sticky bar)
const saveBtn = document.querySelector('.save-btn');
if (saveBtn) {
  saveBtn.addEventListener('click', () => {
    saveBtn.classList.toggle('saved');
    const svg = saveBtn.querySelector('path');
    if (svg) svg.setAttribute('fill', saveBtn.classList.contains('saved') ? 'currentColor' : 'none');
  });
}

// ACTION SAVE BUTTON (sidebar)
const actionSave = document.querySelector('.action-btn');
if (actionSave) {
  actionSave.addEventListener('click', () => {
    actionSave.classList.toggle('saved');
  });
}

// ONE CLICK POPUP CLOSE
const closePopup = document.getElementById('closePopup');
if (closePopup) {
  closePopup.addEventListener('click', () => {
    const popup = document.getElementById('oneClickPopup');
    if (popup) popup.style.display = 'none';
  });
}
(function () {
  'use strict';

  // ── ELEMENTS ───────────────────────────────────────────
  var overlay     = document.getElementById('modal-overlay');
  var openBtn     = document.getElementById('open-modal');
  var closeBtn    = document.getElementById('close-modal');
  var themeToggle = document.getElementById('theme-toggle');
  var photoInput  = document.getElementById('photo-input');
  var cvInput     = document.getElementById('cv-input');

  var modalPhotoPreview = document.getElementById('modal-photo-preview');
  var photoPlaceholder  = document.getElementById('photo-placeholder');
  var cvPlaceholder     = document.getElementById('cv-placeholder');
  var cvFilename        = document.getElementById('cv-filename');

  // ── THEME TOGGLE ───────────────────────────────────────
  var isDark = true;
  themeToggle.addEventListener('click', function () {
    isDark = !isDark;
    document.documentElement.setAttribute('data-theme', isDark ? '' : 'light');
    themeToggle.innerHTML = isDark
      ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
      : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
  });

  // ── MODAL OPEN / CLOSE ─────────────────────────────────
  function openModal() {
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    document.getElementById('modal-body').scrollTop = 0;
  }

  function closeModal() {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  openBtn.addEventListener('click', openModal);
  closeBtn.addEventListener('click', closeModal);

  // Close on backdrop click
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeModal();
  });

  // Close on Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && overlay.classList.contains('open')) closeModal();
  });

  // ── PHOTO PREVIEW ──────────────────────────────────────
  // (Only previews the new selection; actual save goes via form POST)
  if (photoInput) {
    photoInput.addEventListener('change', function () {
      var file = photoInput.files[0];
      if (!file) return;
      if (file.size > 5 * 1024 * 1024) {
        alert('Max photo size is 5 MB.');
        photoInput.value = '';
        return;
      }
      var reader = new FileReader();
      reader.onload = function (e) {
        modalPhotoPreview.src           = e.target.result;
        modalPhotoPreview.style.display = 'block';
        photoPlaceholder.style.display  = 'none';
      };
      reader.readAsDataURL(file);
    });
  }

  // ── CV FILE NAME PREVIEW ───────────────────────────────
  // (Only shows the filename; actual upload goes via form POST)
  if (cvInput) {
    cvInput.addEventListener('change', function () {
      var file = cvInput.files[0];
      if (!file) return;
      if (file.size > 5 * 1024 * 1024) {
        alert('Max CV size is 5 MB.');
        cvInput.value = '';
        return;
      }
      cvPlaceholder.style.display = 'none';
      cvFilename.textContent      = '📄 ' + file.name;
      cvFilename.style.display    = 'block';
    });
  }

  // ── RE-OPEN MODAL IF FORM ERRORS RETURNED ─────────────
  // If Django returns the page with form errors, keep modal open
  var hasFormErrors = document.querySelector('.modal-form-error');
  if (hasFormErrors) {
    openModal();
  }

})();
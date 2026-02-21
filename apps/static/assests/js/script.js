// ===== TOAST =====
function showToast(msg) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.style.cssText = `
      position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%);
      background: #1a1a2e; color: #fff; padding: 0.65rem 1.4rem;
      border-radius: 50px; font-size: 0.85rem; font-family: 'DM Sans', sans-serif;
      box-shadow: 0 4px 20px rgba(0,0,0,0.2); z-index: 999;
    `;
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.display = 'block';
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => { toast.style.display = 'none'; }, 2500);
}


// ===== THEME TOGGLE =====
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


// ===== SOCIAL BUTTONS (landing.html + register.html) =====
const googleBtn = document.getElementById('googleBtn');
if (googleBtn) googleBtn.addEventListener('click', () => showToast('Redirecting to Google…'));

const linkedinBtn = document.getElementById('linkedinBtn');
if (linkedinBtn) linkedinBtn.addEventListener('click', () => showToast('Redirecting to LinkedIn…'));

const githubBtn = document.getElementById('githubBtn');
if (githubBtn) githubBtn.addEventListener('click', () => showToast('Redirecting to GitHub…'));


// ===== EMAIL BUTTON → login page (landing.html) =====
const emailBtn = document.getElementById('emailBtn');
if (emailBtn) {
  emailBtn.addEventListener('click', () => {
    window.location.href = 'index.html';
  });
}


// ===== PASSWORD TOGGLE — login.html (eyeBtn, name="password") =====
const eyeBtn = document.getElementById('eyeBtn');
if (eyeBtn) {
  const pwInput = document.querySelector('input[name="password"]');
  const eyeIcon = document.getElementById('eyeIcon');
  let visible = false;

  const eyeOpenSVG = `
    <circle cx="12" cy="12" r="3"/>
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
  `;
  const eyeClosedSVG = `
    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
    <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
    <line x1="1" y1="1" x2="23" y2="23"/>
  `;

  eyeBtn.addEventListener('click', () => {
    visible = !visible;
    pwInput.type = visible ? 'text' : 'password';
    eyeIcon.innerHTML = visible ? eyeOpenSVG : eyeClosedSVG;
  });

  // Submit button color — login.html
  const loginEmail  = document.querySelector('input[name="email"]');
  const loginSubmit = document.getElementById('submit');
  if (loginEmail && loginSubmit) {
    function updateLoginBtn() {
      const hasInput = loginEmail.value.length > 0 || pwInput.value.length > 0;
      loginSubmit.classList.toggle('active', hasInput);
    }
    loginEmail.addEventListener('input', updateLoginBtn);
    pwInput.addEventListener('input', updateLoginBtn);
  }
}


// ===== REGISTER PAGE (register.html) =====
const eyeBtn1 = document.getElementById('eyeBtn1');
if (eyeBtn1) {

  const eyeOpenHTML = `
    <circle cx="12" cy="12" r="3"/>
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
  `;
  const eyeClosedHTML = `
    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
    <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
    <line x1="1" y1="1" x2="23" y2="23"/>
  `;

  function setupPasswordToggle(inputId, btnId, iconId) {
    const input = document.getElementById(inputId);
    const btn   = document.getElementById(btnId);
    const icon  = document.getElementById(iconId);
    if (!input || !btn || !icon) return;
    let vis = false;
    btn.addEventListener('click', () => {
      vis = !vis;
      input.type = vis ? 'text' : 'password';
      icon.innerHTML = vis ? eyeOpenHTML : eyeClosedHTML;
    });
  }

  setupPasswordToggle('password', 'eyeBtn1', 'eyeIcon1');
  setupPasswordToggle('repeatPassword', 'eyeBtn2', 'eyeIcon2');

  // Password rules
  const passwordInput = document.getElementById('password');
  const repeatInput   = document.getElementById('repeatPassword');
  const repeatError   = document.getElementById('repeatError');
  const emailInput    = document.getElementById('email');
  const emailError    = document.getElementById('emailError');
  const termsCheck    = document.getElementById('termsCheck');
  const submitBtn     = document.getElementById('submitBtn');

  const rules = {
    'rule-length':  v => v.length >= 8,
    'rule-number':  v => /[0-9]/.test(v),
    'rule-upper':   v => /[A-Z]/.test(v),
    'rule-lower':   v => /[a-z]/.test(v),
    'rule-special': v => /[!@#$%^&*]/.test(v),
  };

  function checkRules(val) {
    let allValid = true;
    for (const [id, fn] of Object.entries(rules)) {
      const li   = document.getElementById(id);
      if (!li) continue;
      const icon = li.querySelector('.rule-icon');
      const ok   = fn(val);
      li.classList.toggle('valid', ok);
      icon.textContent = ok ? '✓' : '✕';
      if (!ok) allValid = false;
    }
    return allValid;
  }

  function isValidEmail(val) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val.trim());
  }

  function updateSubmit() {
    if (!submitBtn) return;
    const emailOk  = isValidEmail(emailInput.value);
    const passOk   = Object.values(rules).every(fn => fn(passwordInput.value));
    const repeatOk = repeatInput.value === passwordInput.value && repeatInput.value.length > 0;
    const termsOk  = termsCheck.checked;
    submitBtn.disabled = !(emailOk && passOk && repeatOk && termsOk);
  }

  if (passwordInput) {
    passwordInput.addEventListener('input', () => {
      checkRules(passwordInput.value);
      if (repeatInput.value) {
        const match = repeatInput.value === passwordInput.value;
        repeatError.textContent = match ? '' : 'Passwords do not match.';
        repeatInput.classList.toggle('error-input', !match);
      }
      updateSubmit();
    });
  }

  if (repeatInput) {
    repeatInput.addEventListener('input', () => {
      const match = repeatInput.value === passwordInput.value;
      repeatError.textContent = repeatInput.value && !match ? 'Passwords do not match.' : '';
      repeatInput.classList.toggle('error-input', repeatInput.value && !match);
      updateSubmit();
    });
  }

  if (emailInput) {
    emailInput.addEventListener('blur', () => {
      const ok = isValidEmail(emailInput.value);
      emailError.textContent = emailInput.value && !ok ? 'Please enter a valid email address.' : '';
      emailInput.classList.toggle('error-input', emailInput.value && !ok);
      updateSubmit();
    });
    emailInput.addEventListener('input', () => {
      if (isValidEmail(emailInput.value)) {
        emailError.textContent = '';
        emailInput.classList.remove('error-input');
      }
      updateSubmit();
    });
  }

  if (termsCheck) termsCheck.addEventListener('change', updateSubmit);

  // Show more toggles
  function setupShowMore(btnId, extraId) {
    const btn   = document.getElementById(btnId);
    const extra = document.getElementById(extraId);
    if (!btn || !extra) return;
    let open = false;
    btn.addEventListener('click', () => {
      open = !open;
      extra.style.display = open ? 'block' : 'none';
      btn.textContent = open ? 'Show less' : 'Show more';
    });
  }
  setupShowMore('showMore1', 'extra1');
  setupShowMore('showMore2', 'extra2');

  // Submit
  if (submitBtn) {
    submitBtn.addEventListener('click', () => {
      const emailOk  = isValidEmail(emailInput.value);
      const passOk   = Object.values(rules).every(fn => fn(passwordInput.value));
      const repeatOk = repeatInput.value === passwordInput.value && repeatInput.value.length > 0;

      if (!emailOk) {
        emailError.textContent = 'Please enter a valid email address.';
        emailInput.classList.add('error-input');
        emailInput.focus();
        return;
      }
      if (!passOk) { passwordInput.focus(); return; }
      if (!repeatOk) {
        repeatError.textContent = 'Passwords do not match.';
        repeatInput.classList.add('error-input');
        repeatInput.focus();
        return;
      }
      if (!termsCheck.checked) { showToast('Please accept the Terms of Service.'); return; }

      submitBtn.textContent = 'Creating account…';
      submitBtn.disabled = true;
      setTimeout(() => {
        submitBtn.textContent = '✓ Account created!';
        setTimeout(() => {
          submitBtn.textContent = 'Create account';
          submitBtn.disabled = false;
        }, 2500);
      }, 1400);
    });
  }
}

const resetBtn = document.getElementById('resetBtn');
if (resetBtn) {
  const resetEmail = document.getElementById('resetEmail');
  const resetEmailError = document.getElementById('resetEmailError');

  function isValidEmail(val) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val.trim());
  }

  resetEmail.addEventListener('blur', () => {
    if (resetEmail.value && !isValidEmail(resetEmail.value)) {
      resetEmailError.textContent = 'Please enter a valid email address.';
      resetEmail.classList.add('error-input');
    } else {
      resetEmailError.textContent = '';
      resetEmail.classList.remove('error-input');
    }
  });

  resetBtn.addEventListener('click', () => {
    if (!resetEmail.value) {
      resetEmailError.textContent = 'Email is required.';
      resetEmail.classList.add('error-input');
      resetEmail.focus();
      return;
    }
    if (!isValidEmail(resetEmail.value)) {
      resetEmailError.textContent = 'Please enter a valid email address.';
      resetEmail.classList.add('error-input');
      resetEmail.focus();
      return;
    }

    resetBtn.textContent = 'Sending…';
    resetBtn.disabled = true;

    setTimeout(() => {
      resetBtn.textContent = '✓ Reset link sent!';
      setTimeout(() => {
        resetBtn.textContent = 'Reset password';
        resetBtn.disabled = false;
        resetEmail.value = '';
        resetEmailError.textContent = '';
        resetEmail.classList.remove('error-input');
      }, 2500);
    }, 1200);
  });
}
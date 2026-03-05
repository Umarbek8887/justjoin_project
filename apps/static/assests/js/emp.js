// Tab switching
function switchTab(tab) {
    const tabCreate = document.getElementById('tab-create');
    const tabSignin = document.getElementById('tab-signin');
    const formCreate = document.getElementById('form-create');
    const formSignin = document.getElementById('form-signin');

    if (tab === 'create') {
        tabCreate.classList.add('active');
        tabSignin.classList.remove('active');
        formCreate.classList.remove('hidden');
        formSignin.classList.add('hidden');
    } else {
        tabSignin.classList.add('active');
        tabCreate.classList.remove('active');
        formSignin.classList.remove('hidden');
        formCreate.classList.add('hidden');
    }
}

// Toggle password visibility
function togglePass(inputId) {
    const input = document.getElementById(inputId);
    input.type = input.type === 'password' ? 'text' : 'password';
}

// Init: set default active tab
document.addEventListener('DOMContentLoaded', () => {
    switchTab('create');
});

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

function clearError() {
    const input = document.getElementById('email-input');
    const msg = document.getElementById('error-msg');
    input.classList.remove('input-error');
    msg.classList.remove('show');
}

function handleSubmit() {
    const input = document.getElementById('email-input');
    const msg = document.getElementById('error-msg');
    const val = input.value.trim();

    if (!val) {
        msg.textContent = 'E-mail address is required.';
        input.classList.add('input-error');
        msg.classList.add('show');
        input.focus();
        return;
    }
    if (!isValidEmail(val)) {
        msg.textContent = 'Please enter a valid e-mail address.';
        input.classList.add('input-error');
        msg.classList.add('show');
        input.focus();
        return;
    }

    // Show success
    document.getElementById('sent-email').textContent = val;
    document.getElementById('forgot-form').style.display = 'none';
    document.getElementById('success-box').classList.add('show');
}

function resend() {
    document.getElementById('forgot-form').style.display = 'block';
    document.getElementById('success-box').classList.remove('show');
    document.getElementById('email-input').focus();
}

// Enter key support
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('email-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') handleSubmit();
    });
});

// ── REGISTER FORM VALIDATION ──────────────────────────────────────────────────

var VALIDATORS = {
    full_name: {
        el: function () {
            return document.querySelector('input[name="full_name"]');
        },
        validate: function (val) {
            if (!val) return 'Name and surname is required.';
            if (val.trim().split(/\s+/).length < 2) return 'Please enter both first and last name.';
            return null;
        }
    },
    country: {
        el: function () {
            return document.querySelector('input[name="country"]');
        },
        validate: function (val) {
            if (!val) return 'Country is required.';
            return null;
        }
    },
    phone_number: {
        el: function () {
            return document.querySelector('input[name="phone_number"]');
        },
        validate: function (val) {
            if (!val) return 'Phone number is required.';
            if (!/^\+?[\d\s\-()]{7,20}$/.test(val)) return 'Enter a valid phone number.';
            return null;
        }
    },
    email: {
        el: function () {
            return document.querySelector('input[name="email"]');
        },
        validate: function (val) {
            if (!val) return 'E-mail address is required.';
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) return 'Enter a valid e-mail address.';
            return null;
        }
    },
    password: {
        el: function () {
            return document.querySelector('input[name="password"]');
        },
        validate: function (val) {
            if (!val) return 'Password is required.';
            if (val.length < 8) return 'Password must be at least 8 characters.';
            if (!/[0-9]/.test(val)) return 'Must include at least 1 number.';
            if (!/[a-z]/.test(val)) return 'Must include at least 1 lowercase letter.';
            if (!/[A-Z]/.test(val)) return 'Must include at least 1 uppercase letter.';
            if (!/[^a-zA-Z0-9]/.test(val)) return 'Must include at least 1 special character.';
            return null;
        }
    },
    confirm_password: {
        el: function () {
            return document.querySelector('input[name="confirm_password"]');
        },
        validate: function (val) {
            if (!val) return 'Please repeat your password.';
            var pass = document.querySelector('input[name="password"]');
            if (pass && val !== pass.value) return 'Passwords do not match.';
            return null;
        }
    }
};

function getOrCreateErrorEl(input, fieldName) {
    var fg = input.closest('.form-group') || input.parentElement;
    var cls = 'js-err-' + fieldName;
    var err = fg.querySelector('.' + cls);
    if (!err) {
        err = document.createElement('span');
        err.className = 'field-error ' + cls;
        var wrap = fg.querySelector('.pass-wrap') || input;
        wrap.insertAdjacentElement('afterend', err);
    }
    return err;
}

function showFieldError(fieldName, message) {
    var cfg = VALIDATORS[fieldName];
    if (!cfg) return;
    var input = cfg.el();
    if (!input) return;
    input.classList.add('input-error');
    getOrCreateErrorEl(input, fieldName).textContent = message;
}

function clearFieldError(fieldName) {
    var cfg = VALIDATORS[fieldName];
    if (!cfg) return;
    var input = cfg.el();
    if (!input) return;
    input.classList.remove('input-error');
    var fg = input.closest('.form-group') || input.parentElement;
    var err = fg.querySelector('.js-err-' + fieldName);
    if (err) err.textContent = '';
}

function validateField(fieldName) {
    var cfg = VALIDATORS[fieldName];
    var input = cfg.el();
    if (!input) return true;
    var error = cfg.validate(input.value.trim());
    if (error) {
        showFieldError(fieldName, error);
        return false;
    }
    clearFieldError(fieldName);
    return true;
}

function validateAll() {
    var valid = true;
    Object.keys(VALIDATORS).forEach(function (f) {
        if (!validateField(f)) valid = false;
    });
    return valid;
}

document.addEventListener('DOMContentLoaded', function () {
    Object.keys(VALIDATORS).forEach(function (fieldName) {
        var input = VALIDATORS[fieldName].el();
        if (!input) return;
        // Validate on blur (field tashlab ketganda)
        input.addEventListener('blur', function () {
            validateField(fieldName);
        });
        // Yozayotganda xato bo'lsa, real-time tozalash
        input.addEventListener('input', function () {
            if (input.classList.contains('input-error')) validateField(fieldName);
        });
    });

    // Form submit bloklash
    var form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (e) {
            if (!validateAll()) {
                e.preventDefault();
                var first = form.querySelector('.input-error');
                if (first) first.scrollIntoView({behavior: 'smooth', block: 'center'});
            }
        });
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
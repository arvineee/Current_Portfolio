/* ── Navbar scroll effect ──────────────────────────────────────────────────── */
window.addEventListener('scroll', () => {
  const navbar = document.getElementById('navbar');
  if (navbar) {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }
});

/* ── Mobile menu ───────────────────────────────────────────────────────────── */
const menuBtn = document.getElementById('menuBtn');
const mobileMenu = document.getElementById('mobileMenu');
const hamburgerIcon = document.getElementById('hamburgerIcon');

if (menuBtn && mobileMenu && hamburgerIcon) {
  menuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
    
    if (!mobileMenu.classList.contains('hidden')) {
      hamburgerIcon.innerHTML = `
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6h12v12" />
      `;
    } else {
      hamburgerIcon.innerHTML = `
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
      `;
    }
  });
}

// Close mobile menu on link click
document.querySelectorAll('.mobile-link').forEach(link => {
  link.addEventListener('click', () => {
    if (mobileMenu && hamburgerIcon) {
      mobileMenu.classList.add('hidden');
      hamburgerIcon.innerHTML = `
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
      `;
    }
  });
});

/* ── Smooth Scroll for All Anchor Links ────────────────────────────────────── */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    if (this.getAttribute('href') === '#') return;
    
    e.preventDefault();
    const targetId = this.getAttribute('href');
    const targetElement = document.querySelector(targetId);
    
    if (targetElement) {
      const navbarHeight = 80; 
      const elementPosition = targetElement.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.scrollY - navbarHeight;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  });
});

/* ── High Conversion Typewriter Engineering phrases ───────────────────────── */
const phrases = [
  'ship optimized multi-tenant SaaS tools inside rigid deadlines',
  'wire flawless automated M-Pesa STK payment gateways',
  'dominate organic search indexing visibility curves',
  'build reliable relational databases that never crash under load',
  'integrate advanced generative AI features into simple services',
  'write strict, human-readable Python code architectures',
  'provision high-performance WSGI server setups cleanly'
];

let phraseIndex = 0;
let charIndex = 0;
let isDeleting = false;
const typeEl = document.getElementById('typewriter');

function type() {
  if (!typeEl) return;
  const current = phrases[phraseIndex];
  if (isDeleting) {
    typeEl.textContent = current.substring(0, charIndex - 1);
    charIndex--;
  } else {
    typeEl.textContent = current.substring(0, charIndex + 1);
    charIndex++;
  }

  let delay = isDeleting ? 30 : 60;

  if (!isDeleting && charIndex === current.length) {
    delay = 2500;
    isDeleting = true;
  } else if (isDeleting && charIndex === 0) {
    isDeleting = false;
    phraseIndex = (phraseIndex + 1) % phrases.length;
    delay = 400;
  }

  setTimeout(type, delay);
}

// Start execution safely on layout instantiation
document.addEventListener('DOMContentLoaded', () => {
  type();
});

/* ── Scroll reveal observer pipeline ─────────────────────────────────────── */
const reveals = document.querySelectorAll('.reveal');
if (reveals.length > 0) {
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.classList.add('visible');
        }, i * 60);
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05, rootMargin: '0px 0px -20px 0px' });

  reveals.forEach(el => revealObserver.observe(el));
}

/* ── Contact form processing (Asynchronous AJAX Engine) ──────────────────── */
async function submitContact() {
  const name = document.getElementById('fname') ? document.getElementById('fname').value.trim() : '';
  const email = document.getElementById('femail') ? document.getElementById('femail').value.trim() : '';
  const subject = document.getElementById('fsubject') ? document.getElementById('fsubject').value.trim() : '';
  const message = document.getElementById('fmessage') ? document.getElementById('fmessage').value.trim() : '';
  const alert = document.getElementById('formAlert');
  const btn = document.getElementById('submitBtn');
  const btnText = document.getElementById('btnText');
  const btnSpinner = document.getElementById('btnSpinner');

  if (!name || !email || !message) {
    showAlert('Please supply all mandatory input values before submitting.', 'error');
    return;
  }
  if (!isValidEmail(email)) {
    showAlert('The target communication endpoint structure is invalid.', 'error');
    return;
  }

  if (btn && btnText && btnSpinner && alert) {
    btn.disabled = true;
    btnText.textContent = 'Transmitting Metrics...';
    btnSpinner.classList.remove('hidden');
    alert.classList.add('hidden');

    try {
      const response = await fetch('/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, subject, message }),
      });

      const data = await response.json();

      if (data.success) {
        showAlert(data.message, 'success');
        document.getElementById('fname').value = '';
        document.getElementById('femail').value = '';
        document.getElementById('fsubject').value = '';
        document.getElementById('fmessage').value = '';
      } else {
        showAlert(data.error || 'A processing fault structural error occurred.', 'error');
      }
    } catch (err) {
      showAlert('Network layer interruption. Please connect immediately using the instant WhatsApp backup link.', 'error');
    } finally {
      btn.disabled = false;
      btnText.textContent = 'Transmit Architecture Briefing';
      btnSpinner.classList.add('hidden');
    }
  }
}

function showAlert(msg, type) {
  const alert = document.getElementById('formAlert');
  if (alert) {
    alert.textContent = msg;
    alert.className = type === 'success' ? 'alert-success' : 'alert-error';
    alert.classList.remove('hidden');
  }
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}



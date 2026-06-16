/* ── Navbar scroll effect ─────────────────────────────────────────────────── */
window.addEventListener('scroll', () => {
  const navbar = document.getElementById('navbar');
  if (navbar) {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  }
});

/* ── Mobile menu (hamburger) ──────────────────────────────────────────────── */
const menuBtn      = document.getElementById('menuBtn');
const mobileMenu   = document.getElementById('mobileMenu');
const hamburgerIcon = document.getElementById('hamburgerIcon');

const HAMBURGER = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>`;
const CLOSE     = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>`;

if (menuBtn && mobileMenu) {
  menuBtn.addEventListener('click', () => {
    const isOpen = mobileMenu.style.display === 'flex';
    mobileMenu.style.display = isOpen ? 'none' : 'flex';
    if (hamburgerIcon) hamburgerIcon.innerHTML = isOpen ? HAMBURGER : CLOSE;
  });
}

/* Close menu when any mobile link is tapped */
document.querySelectorAll('.mobile-link').forEach(link => {
  link.addEventListener('click', () => {
    if (mobileMenu) mobileMenu.style.display = 'none';
    if (hamburgerIcon) hamburgerIcon.innerHTML = HAMBURGER;
  });
});

/* ── Smooth scroll ────────────────────────────────────────────────────────── */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const href = this.getAttribute('href');
    if (href === '#') return;
    e.preventDefault();
    const target = document.querySelector(href);
    if (target) {
      window.scrollTo({
        top: target.getBoundingClientRect().top + window.scrollY - 80,
        behavior: 'smooth'
      });
    }
  });
});

/* ── Typewriter ───────────────────────────────────────────────────────────── */
const phrases = [
  'ship optimized multi-tenant SaaS tools inside rigid deadlines',
  'wire flawless M-Pesa STK payment gateways',
  'dominate organic search indexing visibility curves',
  'build reliable relational databases that never crash under load',
  'integrate advanced generative AI features into simple services',
  'write strict, human-readable Python code architectures',
  'provision high-performance WSGI server setups cleanly',
];

let phraseIndex = 0, charIndex = 0, isDeleting = false;
const typeEl = document.getElementById('typewriter');

function type() {
  if (!typeEl) return;
  const current = phrases[phraseIndex];
  typeEl.textContent = isDeleting
    ? current.substring(0, charIndex - 1)
    : current.substring(0, charIndex + 1);
  isDeleting ? charIndex-- : charIndex++;

  let delay = isDeleting ? 30 : 60;
  if (!isDeleting && charIndex === current.length) { delay = 2500; isDeleting = true; }
  else if (isDeleting && charIndex === 0) { isDeleting = false; phraseIndex = (phraseIndex + 1) % phrases.length; delay = 400; }
  setTimeout(type, delay);
}
document.addEventListener('DOMContentLoaded', type);

/* ── Scroll reveal ────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  const reveals = document.querySelectorAll('.reveal');
  if (!reveals.length) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('visible'), i * 60);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05, rootMargin: '0px 0px -20px 0px' });
  reveals.forEach(el => observer.observe(el));
});

/* ── Contact form ─────────────────────────────────────────────────────────── */
async function submitContact() {
  const name    = document.getElementById('fname')?.value.trim()    || '';
  const email   = document.getElementById('femail')?.value.trim()   || '';
  const subject = document.getElementById('fsubject')?.value.trim() || '';
  const message = document.getElementById('fmessage')?.value.trim() || '';
  const btn     = document.getElementById('submitBtn');
  const btnText = document.getElementById('btnText');
  const spinner = document.getElementById('btnSpinner');

  if (!name || !email || !message) { showAlert('Please fill in all required fields.', 'error'); return; }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { showAlert('Please enter a valid email address.', 'error'); return; }

  btn.disabled = true;
  btnText.textContent = 'Sending...';
  spinner.style.display = 'inline-block';

  try {
    const res  = await fetch('/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, email, subject, message }) });
    const data = await res.json();
    if (data.success) {
      showAlert(data.message, 'success');
      ['fname','femail','fsubject','fmessage'].forEach(id => { const el = document.getElementById(id); if (el) el.value = ''; });
    } else {
      showAlert(data.error || 'Something went wrong. Please try WhatsApp.', 'error');
    }
  } catch {
    showAlert('Network error. Please use WhatsApp directly.', 'error');
  } finally {
    btn.disabled = false;
    btnText.textContent = 'Send Project Brief';
    spinner.style.display = 'none';
  }
}

function showAlert(msg, type) {
  const el = document.getElementById('formAlert');
  if (!el) return;
  el.textContent = msg;
  el.className   = type === 'success' ? 'alert-success' : 'alert-error';
  el.style.display = 'block';
}


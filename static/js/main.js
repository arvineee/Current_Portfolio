/* ── Navbar scroll effect ──────────────────────────────────────────────────── */
window.addEventListener('scroll', () => {
  const navbar = document.getElementById('navbar');
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

/* ── Mobile menu ───────────────────────────────────────────────────────────── */
const menuBtn = document.getElementById('menuBtn');
const mobileMenu = document.getElementById('mobileMenu');
const hamburgerIcon = document.getElementById('hamburgerIcon');

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

// Close mobile menu on link click
document.querySelectorAll('.mobile-link').forEach(link => {
  link.addEventListener('click', () => {
    mobileMenu.classList.add('hidden');
    hamburgerIcon.innerHTML = `
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
    `;
  });
});

/* ── Smooth Scroll for All Anchor Links ────────────────────────────────────── */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    // Only handle internal hash links
    if (this.getAttribute('href') === '#') return;
    
    e.preventDefault();
    const targetId = this.getAttribute('href');
    const targetElement = document.querySelector(targetId);
    
    if (targetElement) {
      const navbarHeight = 80; // Adjust based on your navbar height
      const elementPosition = targetElement.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.scrollY - navbarHeight;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  });
});

/* ── Typewriter ────────────────────────────────────────────────────────────── */
const phrases = [
  'ship your MVP in weeks, not months',
  'wire in M-Pesa without the headaches',
  'get you ranking on Google News',
  'build backends that don\'t break at 2am',
  'integrate AI where it actually matters',
  'write code your next dev won\'t curse',
  'deploy it, configure it, hand it over',
];

let phraseIndex = 0;
let charIndex = 0;
let isDeleting = false;
const typeEl = document.getElementById('typewriter');

function type() {
  const current = phrases[phraseIndex];
  if (isDeleting) {
    typeEl.textContent = current.substring(0, charIndex - 1);
    charIndex--;
  } else {
    typeEl.textContent = current.substring(0, charIndex + 1);
    charIndex++;
  }

  let delay = isDeleting ? 40 : 80;

  if (!isDeleting && charIndex === current.length) {
    delay = 2000;
    isDeleting = true;
  } else if (isDeleting && charIndex === 0) {
    isDeleting = false;
    phraseIndex = (phraseIndex + 1) % phrases.length;
    delay = 400;
  }

  setTimeout(type, delay);
}

type();

/* ── Scroll reveal ─────────────────────────────────────────────────────────── */
const reveals = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.classList.add('visible');
      }, i * 80);
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

reveals.forEach(el => revealObserver.observe(el));

/* ── Contact form (AJAX) ───────────────────────────────────────────────────── */
async function submitContact() {
  const name = document.getElementById('fname').value.trim();
  const email = document.getElementById('femail').value.trim();
  const subject = document.getElementById('fsubject').value.trim();
  const message = document.getElementById('fmessage').value.trim();
  const alert = document.getElementById('formAlert');
  const btn = document.getElementById('submitBtn');
  const btnText = document.getElementById('btnText');
  const btnSpinner = document.getElementById('btnSpinner');

  if (!name || !email || !message) {
    showAlert('Please fill in all required fields.', 'error');
    return;
  }
  if (!isValidEmail(email)) {
    showAlert('Please enter a valid email address.', 'error');
    return;
  }

  btn.disabled = true;
  btnText.textContent = 'Sending...';
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
      showAlert(data.error || 'Something went wrong. Please try again.', 'error');
    }
  } catch (err) {
    showAlert('Network error. Please try WhatsApp instead.', 'error');
  } finally {
    btn.disabled = false;
    btnText.textContent = 'Send Message';
    btnSpinner.classList.add('hidden');
  }
}

function showAlert(msg, type) {
  const alert = document.getElementById('formAlert');
  alert.textContent = msg;
  alert.className = `mb-6 p-4 rounded-2xl text-sm font-medium ${
    type === 'success' 
      ? 'bg-green-900/50 text-green-300 border border-green-500/30' 
      : 'bg-red-900/50 text-red-300 border border-red-500/30'
  }`;
  alert.classList.remove('hidden');
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

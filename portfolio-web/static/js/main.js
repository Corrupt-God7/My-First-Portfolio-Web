/* ── Scroll fade-in ─────────────────────────────────────────────────────────── */
const observer = new IntersectionObserver(
  (entries) => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
  { threshold: 0.1 }
);
document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));


/* ── Mobile nav toggle ──────────────────────────────────────────────────────── */
const toggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
toggle.addEventListener('click', () => navLinks.classList.toggle('open'));
navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));


/* ── Active nav highlight on scroll ────────────────────────────────────────── */
const sections = document.querySelectorAll('section[id]');
const navAnchors = document.querySelectorAll('.nav-links a');
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(s => { if (window.scrollY >= s.offsetTop - 80) current = s.id; });
  navAnchors.forEach(a => {
    a.style.color = a.getAttribute('href') === '#' + current ? 'var(--accent2)' : '';
  });
}, { passive: true });


/* ── Contact Form ───────────────────────────────────────────────────────────── */
const form      = document.getElementById('contactForm');
const submitBtn = document.getElementById('submitBtn');
const btnText   = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');
const formMsg   = document.getElementById('formMsg');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  // Loading state
  submitBtn.disabled = true;
  btnText.style.display  = 'none';
  btnLoader.style.display = 'inline';
  formMsg.style.display  = 'none';

  const payload = {
    name:    document.getElementById('name').value,
    email:   document.getElementById('email').value,
    subject: document.getElementById('subject').value,
    message: document.getElementById('message').value,
  };

  try {
    const res  = await fetch('/send-message', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });
    const data = await res.json();

    formMsg.style.display = 'block';
    if (data.success) {
      formMsg.className = 'form-feedback success';
      formMsg.textContent = '✓ ' + data.message;
      form.reset();
    } else {
      formMsg.className = 'form-feedback error';
      formMsg.textContent = '✗ ' + (data.error || 'Something went wrong.');
    }
  } catch {
    formMsg.style.display = 'block';
    formMsg.className = 'form-feedback error';
    formMsg.textContent = '✗ Network error. Please email me directly.';
  } finally {
    submitBtn.disabled = false;
    btnText.style.display  = 'inline';
    btnLoader.style.display = 'none';
  }
});

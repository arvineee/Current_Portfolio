/* Contact page form submission. */
function submitContactForm() {
  const name    = document.getElementById('fname').value.trim();
  const email   = document.getElementById('femail').value.trim();
  const subject = document.getElementById('fsubject').value.trim() || 'Contact Page Lead';
  const message = document.getElementById('fmessage').value.trim();
  const alertBox = document.getElementById('formAlert');
  const btn = document.getElementById('submitBtn');
  const btnText = document.getElementById('btnText');
  const btnSpinner = document.getElementById('btnSpinner');

  alertBox.style.display = 'none';

  if (!name || !email || !message) {
    alertBox.textContent = 'Please fill in your name, contact info, and details.';
    alertBox.style.cssText = 'display:block;background:#FBEAEA;color:#B3261E;padding:.85rem 1rem;border-radius:6px;font-size:.85rem;margin-bottom:1.25rem;';
    return;
  }

  btn.disabled = true;
  btnText.style.display = 'none';
  btnSpinner.style.display = 'inline-flex';

  fetch('/contact', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, subject, message })
  })
    .then(res => res.json())
    .then(data => {
      btn.disabled = false;
      btnText.style.display = 'inline';
      btnSpinner.style.display = 'none';

      if (data.success) {
        alertBox.textContent = data.message || 'Thanks! We will respond within 24 hours.';
        alertBox.style.cssText = 'display:block;background:#E8F5E9;color:#1B5E20;padding:.85rem 1rem;border-radius:6px;font-size:.85rem;margin-bottom:1.25rem;';
        document.getElementById('fname').value = '';
        document.getElementById('femail').value = '';
        document.getElementById('fsubject').value = '';
        document.getElementById('fmessage').value = '';
      } else {
        alertBox.textContent = data.error || 'Something went wrong. Please try WhatsApp instead.';
        alertBox.style.cssText = 'display:block;background:#FBEAEA;color:#B3261E;padding:.85rem 1rem;border-radius:6px;font-size:.85rem;margin-bottom:1.25rem;';
      }
    })
    .catch(() => {
      btn.disabled = false;
      btnText.style.display = 'inline';
      btnSpinner.style.display = 'none';
      alertBox.textContent = 'Could not send. Please try WhatsApp instead.';
      alertBox.style.cssText = 'display:block;background:#FBEAEA;color:#B3261E;padding:.85rem 1rem;border-radius:6px;font-size:.85rem;margin-bottom:1.25rem;';
    });
}

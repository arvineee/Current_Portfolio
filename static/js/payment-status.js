/* Payment status page: shows the current state and polls until the webhook settles the order. */
(function () {
  var root = document.getElementById('payStatus');
  if (!root) return;
  var tries = 0, MAX_TRIES = 60;           // ~3 minutes at 3s intervals

  function show(state) {
    root.querySelectorAll('[data-state]').forEach(function (el) {
      el.style.display = el.dataset.state === state ? 'block' : 'none';
    });
  }

  function poll() {
    fetch(root.dataset.url, { headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        show(d.status);
        if (d.status !== 'pending') return;
        if (++tries < MAX_TRIES) { setTimeout(poll, 3000); return; }
        var slow = root.querySelector('[data-state-slow]');
        if (slow) slow.style.display = 'block';
      })
      .catch(function () { if (++tries < MAX_TRIES) setTimeout(poll, 5000); });
  }

  show(root.dataset.initial);
  if (root.dataset.initial === 'pending') poll();
})();

/* Offer countdown (loaded only while an offer is live). */
(function () {
  var els = document.querySelectorAll('.offer-countdown');
  if (!els.length) return;
  var end = new Date(els[0].dataset.end).getTime();
  function pad(n) { return n < 10 ? '0' + n : n; }
  function tick() {
    var left = end - Date.now();
    if (left <= 0) {
      els.forEach(function (e) { e.textContent = 'offer ended'; });
      try {  // reload once so the server drops the offer and normal prices return
        if (!sessionStorage.getItem('offerReload')) { sessionStorage.setItem('offerReload', '1'); location.reload(); }
      } catch (e) {}
      return;
    }
    var d = Math.floor(left / 864e5), h = Math.floor(left % 864e5 / 36e5),
        m = Math.floor(left % 36e5 / 6e4), s = Math.floor(left % 6e4 / 1e3);
    var t = (d ? d + 'd ' : '') + pad(h) + 'h ' + pad(m) + 'm ' + pad(s) + 's';
    els.forEach(function (e) { e.textContent = t; });
    setTimeout(tick, 1000);
  }
  tick();
})();

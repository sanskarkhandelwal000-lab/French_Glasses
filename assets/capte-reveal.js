/* Capté — motion layer: reveal-on-scroll, word-by-word manifesto, image parallax.
   Everything degrades to a static, fully visible page without JS or with reduced motion. */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Pause decorative background video when the visitor prefers reduced motion. */
  if (reduce) {
    document.querySelectorAll('.capte-hero__media video').forEach(function (v) {
      v.removeAttribute('autoplay');
      v.pause();
    });
  }

  /* Reveal on scroll. */
  var items = document.querySelectorAll('.capte-reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
    );
    items.forEach(function (el) { io.observe(el); });
  }

  /* Manifesto: split into words that light up as the paragraph crosses the viewport. */
  var statements = document.querySelectorAll('[data-capte-words]');
  statements.forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.setAttribute('aria-label', el.textContent.trim());
    el.innerHTML = words
      .map(function (w) { return '<span class="capte-word" aria-hidden="true">' + w + '</span>'; })
      .join(' ');
  });

  var parallax = document.querySelectorAll('.capte-story__media img');

  function onScroll() {
    var vh = window.innerHeight;
    statements.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var progress = (vh * 0.85 - r.top) / (r.height + vh * 0.35);
      var spans = el.querySelectorAll('.capte-word');
      var lit = Math.round(Math.max(0, Math.min(1, progress)) * spans.length);
      spans.forEach(function (s, i) { s.classList.toggle('is-lit', i < lit); });
    });
    parallax.forEach(function (img) {
      var r = img.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var p = (r.top + r.height / 2 - vh / 2) / vh;
      img.style.setProperty('--capte-parallax', (p * -6).toFixed(2) + '%');
    });
  }

  if (reduce) {
    document.querySelectorAll('.capte-word').forEach(function (s) { s.classList.add('is-lit'); });
    return;
  }

  /* Horizon scrolls inside .page-wrapper rather than the window. */
  var scroller = document.querySelector('.page-wrapper');
  (scroller || window).addEventListener('scroll', onScroll, { passive: true });
  if (scroller) window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
})();

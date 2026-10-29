/* Capté — motion layer: reveal-on-scroll, viewfinder timecode, image parallax.
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

  /* Manifesto viewfinder: a running timecode while it is on screen. */
  var tcs = document.querySelectorAll('[data-capte-timecode]');
  if (tcs.length && !reduce && 'IntersectionObserver' in window) {
    tcs.forEach(function (tc) {
      var start = null, frame = null;
      var pad = function (n) { return (n < 10 ? '0' : '') + n; };
      var tick = function (t) {
        if (start === null) start = t;
        var ms = t - start;
        tc.textContent = pad(Math.floor(ms / 60000) % 60) + ':' + pad(Math.floor(ms / 1000) % 60) + ':' + pad(Math.floor((ms % 1000) / 40));
        frame = requestAnimationFrame(tick);
      };
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting && frame === null) frame = requestAnimationFrame(tick);
          if (!e.isIntersecting && frame !== null) { cancelAnimationFrame(frame); frame = null; }
        });
      }).observe(tc);
    });
  }

  var parallax = document.querySelectorAll('.capte-story__media img');

  function onScroll() {
    var vh = window.innerHeight;
    parallax.forEach(function (img) {
      var r = img.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var p = (r.top + r.height / 2 - vh / 2) / vh;
      img.style.setProperty('--capte-parallax', (p * -6).toFixed(2) + '%');
    });
  }

  if (reduce) return;

  /* Horizon scrolls inside .page-wrapper rather than the window. */
  var scroller = document.querySelector('.page-wrapper');
  (scroller || window).addEventListener('scroll', onScroll, { passive: true });
  if (scroller) window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
})();

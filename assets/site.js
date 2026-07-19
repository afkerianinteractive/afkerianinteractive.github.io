(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;

  /* Mobile navigation: progressive enhancement over native <details> */
  var navToggle = document.querySelector('.nav-toggle');
  if (navToggle) {
    navToggle.addEventListener('toggle', function () {
      document.body.classList.toggle('nav-open', navToggle.open);
    });
    var navLinks = navToggle.querySelectorAll('a');
    for (var i = 0; i < navLinks.length; i++) {
      navLinks[i].addEventListener('click', function () {
        navToggle.open = false;
      });
    }
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && navToggle.open) {
        navToggle.open = false;
        var summary = navToggle.querySelector('summary');
        if (summary) { summary.focus(); }
      }
    });
  }

  /* Scroll reveal: pure progressive enhancement, no-JS baseline is fully visible */
  if (!reduceMotion && 'IntersectionObserver' in window) {
    root.classList.add('js-reveal');
    var targets = document.querySelectorAll('[data-reveal]');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    targets.forEach(function (t) { io.observe(t); });
  }
})();

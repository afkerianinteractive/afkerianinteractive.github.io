# Official Sources — web-performance-core-web-vitals

Documentation verified: 2026-07-17. Primary sources only.

- web.dev Core Web Vitals — https://web.dev/articles/vitals
- LCP — https://web.dev/articles/lcp
- CLS — https://web.dev/articles/cls
- INP — https://web.dev/articles/inp
- Optimize images — https://web.dev/articles/fast#optimize-your-images
- Font best practices — https://web.dev/articles/font-best-practices
- Lighthouse — https://developer.chrome.com/docs/lighthouse/overview
- MDN loading=lazy — https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#loading

Notes:
- Set explicit image width/height to avoid CLS.
- Preload the LCP image/font; use font-display for non-blocking fonts.
- Measure before and after; avoid framework migration for a static site.

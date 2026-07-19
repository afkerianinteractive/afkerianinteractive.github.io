---
name: web-performance-core-web-vitals
description: Core Web Vitals performance for the static AFKERIAN INTERACTIVE website — static resource loading, image sizing and modern formats, font loading, render-blocking resources, CLS, LCP, INP relevance, and caching assumptions, evidenced with Lighthouse. Activate when reviewing or improving static-site loading performance and Web Vitals. Do not activate for Android, Unity, or migrating to a framework/build tool.
---

# Web Performance & Core Web Vitals

## 1. Purpose
Improve the static site's Core Web Vitals (LCP, CLS, INP) through disciplined resource
loading, correctly sized/modern images, non-blocking fonts/CSS, and sensible caching —
evidenced by Lighthouse, without adding a framework.

## 2. Activate When
- Reviewing/improving page load, LCP, CLS, or INP on the static site.
- Optimizing images, fonts, or render-blocking resources.
- Interpreting Lighthouse results.

## 3. Do Not Activate When
- The target is Android or Unity.
- The task implies a framework/bundler migration (needs approval).

## 4. Scope and Authority
Obey the active CLAUDE.md and project governance. This skill provides technical expertise only and grants no independent execution authority.
No premature framework migration.

## 5. Required Evidence
- A Lighthouse (or field) measurement, or a plan to capture one.
- The page's assets and `<head>` loading order.

## 6. Current Documentation Verification
Confirm current Web Vitals thresholds and techniques against primary sources (web.dev).
See `references/official-sources.md`.

## 7. Inspection Workflow
1. Measure with Lighthouse; identify LCP element and layout-shift sources.
2. Check image dimensions set (prevent CLS), modern formats (AVIF/WebP), and lazy-loading.
3. Check fonts (`font-display`, preconnect/preload of the LCP font/image).
4. Identify render-blocking CSS/JS; defer/inline critical CSS minimally.
5. Note caching/headers assumptions (GitHub Pages defaults).

## 8. Implementation Workflow
- Set explicit image width/height; serve appropriately sized modern formats.
- Preload the LCP resource; make fonts non-blocking.
- Reduce/defer render-blocking resources without a build step.

## 9. Validation Workflow
- Re-run Lighthouse; compare LCP/CLS/INP before/after.
- Confirm no layout shift on load.

## 10. Delegation and Overlap
- Responsive layout → `web-responsive-design-system`.
- Security headers/CSP → `web-static-security-content-policy`.

## 11. Stop Conditions
- Only a framework/build tool could achieve the goal (needs approval).
- No measurement is available and changes would be speculative.

## 12. Final Report
State: measurements (before/after), image/font/render fixes, residual risks, blocked steps.

---
name: web-responsive-design-system
description: Responsive design-system engineering for the static AFKERIAN INTERACTIVE website (HTML5 + CSS, no framework) — mobile-first behavior, fluid sizing and typography, spacing and layout constraints, content-based breakpoints, reduced motion, contrast, focus states, touch targets, and avoiding horizontal overflow. Activate when building or reviewing responsive CSS/layout on the static website. Do not activate for Android, Unity, or introducing a CSS/JS framework.
---

# Web Responsive Design System

## 1. Purpose
Keep the static website responsive and consistent across viewports using mobile-first,
content-driven CSS: fluid type/spacing, sane breakpoints, and no horizontal overflow —
without introducing a framework.

## 2. Activate When
- Building or reviewing responsive layout/CSS on the static site.
- Fixing overflow, breakpoint, or scaling issues.
- Establishing spacing/type scales and reduced-motion support.

## 3. Do Not Activate When
- The target is an Android app or Unity.
- The task implies adopting a CSS/JS framework (not authorized without user approval).

## 4. Scope and Authority
Obey the active CLAUDE.md and project governance. This skill provides technical expertise only and grants no independent execution authority.
Preserve the static HTML5 + CSS architecture; preserve brand consistency.

## 5. Required Evidence
- The actual HTML/CSS under review.
- Observed rendering at representative widths (screenshots as evidence).

## 6. Current Documentation Verification
Confirm modern CSS features against primary sources (MDN, W3C, web.dev).
See `references/official-sources.md`.

## 7. Inspection Workflow
1. Confirm mobile-first base styles with `min-width` media queries.
2. Check fluid sizing (clamp/relative units) and readable line lengths.
3. Verify no fixed widths cause horizontal overflow (`overflow-x`), images `max-width:100%`.
4. Check breakpoints are content-driven, not device-specific.
5. Verify visible focus states, adequate touch targets, and `prefers-reduced-motion`.

## 8. Implementation Workflow
- Use relative units and `clamp()` for fluid type/spacing.
- Add content-based breakpoints; keep one spacing/type scale.
- Ensure media and tables never overflow the viewport.

## 9. Validation Workflow
- Capture screenshots at narrow/medium/wide widths.
- Confirm no horizontal scroll and consistent spacing/typography.

## 10. Delegation and Overlap
- Accessibility conformance → `web-accessibility-wcag`.
- Loading performance → `web-performance-core-web-vitals`.

## 11. Stop Conditions
- A change would require a framework or build tooling (needs approval).
- Brand/design language would change without approval.

## 12. Final Report
State: files changed, widths validated (screenshots), overflow/scaling fixes, residual
risks, blocked steps.

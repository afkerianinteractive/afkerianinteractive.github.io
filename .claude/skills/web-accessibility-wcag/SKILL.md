---
name: web-accessibility-wcag
description: WCAG accessibility engineering for the static AFKERIAN INTERACTIVE website — semantic HTML, landmarks, heading hierarchy, links vs buttons, keyboard navigation, visible focus, color contrast, text alternatives, reduced motion, zoom and reflow, and forms only if later added. Activate when auditing or implementing web accessibility on the static site and gathering WCAG conformance evidence. Do not activate for Android accessibility, Unity, or SEO-only work.
---

# Web Accessibility (WCAG)

## 1. Purpose
Make the static website conform to WCAG: correct semantics and landmarks, full keyboard
operability with visible focus, sufficient contrast, meaningful text alternatives, and
robust zoom/reflow.

## 2. Activate When
- Auditing or fixing accessibility on the static site.
- Reviewing semantics, keyboard access, focus, contrast, or alt text.
- Gathering WCAG conformance evidence.

## 3. Do Not Activate When
- The target is an Android app (use `android-accessibility-quality`) or Unity.
- The task is purely SEO or visual styling unrelated to a11y.

## 4. Scope and Authority
Obey the active CLAUDE.md and project governance. This skill provides technical expertise only and grants no independent execution authority.

## 5. Required Evidence
- The HTML under review.
- Keyboard/screen-reader observations or automated checker output.

## 6. Current Documentation Verification
Confirm WCAG success criteria and ARIA usage against primary sources (W3C/WAI, MDN).
See `references/official-sources.md`.

## 7. Inspection Workflow
1. Verify semantic structure: landmarks (`header/nav/main/footer`), single logical `h1`, ordered headings.
2. Verify links vs buttons used for their correct purpose.
3. Check full keyboard operability and visible focus (`:focus-visible`).
4. Check text/UI contrast ratios and non-color cues.
5. Verify `alt` text (empty for decorative), and reduced-motion support.
6. Verify 200% zoom and reflow without loss of content.

## 8. Implementation Workflow
- Prefer native semantic elements over ARIA; add ARIA only to fill gaps.
- Ensure focus order matches visual order; add skip links if needed.
- Fix contrast and alt text with minimal markup changes.

## 9. Validation Workflow
- Keyboard-only pass; automated checker (e.g. axe) evidence.
- Confirm zoom/reflow and reduced-motion behavior.

## 10. Delegation and Overlap
- Responsive/reflow layout → `web-responsive-design-system`.
- Metadata/SEO → `web-seo-metadata-structured-data`.

## 11. Stop Conditions
- Forms/complex widgets are added that require new interaction patterns beyond scope.
- Conformance cannot be evidenced.

## 12. Final Report
State: pages audited, WCAG issues (evidence vs assumption), fixes, keyboard/contrast/zoom
validation, residual risks, blocked steps.

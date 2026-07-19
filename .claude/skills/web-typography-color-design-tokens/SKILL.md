---
name: web-typography-color-design-tokens
description: Advanced typography, color, and design-token systems for the static AFKERIAN INTERACTIVE website (HTML5 + CSS, no framework) — modular type scale and vertical rhythm, font loading and fallbacks, measure and leading, accessible color systems in modern color spaces, and a coherent CSS custom-property token system. Activate when building or reviewing the type/color system or design tokens. Do not activate for Android, Unity, layout-grid architecture, or pure WCAG audits.
---

# Web Typography, Color & Design Tokens

## 1. Purpose
Turn creative direction into a precise, reusable visual system: a typographic scale with
real rhythm, an accessible color system, and CSS custom-property tokens that keep every
page consistent.

## 2. Activate When
- Designing or reviewing the type scale, font stack, measure/leading, or hierarchy.
- Building an accessible color system or theming with tokens.
- Establishing CSS custom-property design tokens (space, size, color, type).

## 3. Do Not Activate When
- The task is Android or Unity.
- The task is page-level layout/grid architecture (`web-layout-composition-grids`).
- The task is only a WCAG audit (`web-accessibility-wcag`) or fluid-sizing mechanics
  (`web-responsive-design-system`).

## 4. Scope and Authority
Obey the active CLAUDE.md / AGENTS.md / GEMINI.md and project governance. This skill
provides technical expertise only and grants no independent execution authority.

## 5. Required Evidence
- The approved creative direction (from `web-creative-direction-visual-language`).
- The current CSS, font assets, and brand color values.

## 6. Current Documentation Verification
Confirm CSS font/text/color behavior and token conventions against primary sources
(W3C CSS specs, MDN, WCAG, Design Tokens Community Group). See `references/official-sources.md`.

## 7. Type System Workflow
1. Define a modular scale (ratio-based) with `rem`; set base size and line-height for rhythm.
2. Constrain measure (~45–75ch) for body text; set heading leading tighter than body.
3. Build a resilient font stack with sensible fallbacks; load webfonts without blocking
   (delegate loading performance to `web-performance-core-web-vitals`).
4. Map roles (display/heading/body/caption) to tokens, not ad-hoc values.

## 8. Color & Token Workflow
- Define color by role (surface, text, accent, state) in tokens; use modern color spaces
  (e.g. `oklch`) with fallbacks where support requires.
- Verify text and non-text contrast against WCAG 2.2 (1.4.3 / 1.4.11); never rely on color
  alone (delegate conformance evidence to `web-accessibility-wcag`).
- Express the whole system as `:root` CSS custom properties (`--space-*`, `--size-*`,
  `--color-*`, `--font-*`); reference tokens everywhere, hardcode nowhere.

## 9. Validation Workflow
- Confirm scale, rhythm, and measure render as intended across sizes.
- Confirm contrast ratios pass; confirm tokens are the single source of truth.

## 10. Delegation and Overlap
- Direction/intent → `web-creative-direction-visual-language`.
- Layout/grids/composition → `web-layout-composition-grids`.
- Fluid sizing/breakpoint mechanics, touch targets → `web-responsive-design-system`.
- Contrast conformance evidence → `web-accessibility-wcag`.
- Font-loading performance (CLS/LCP, `font-display`) → `web-performance-core-web-vitals`.

## 11. Stop Conditions
- New font dependencies or licenses are required without OWNER approval.
- The color system cannot meet the contrast floor within the approved direction.

## 12. Final Report
State: type scale and rhythm, font stack and loading approach, color system and contrast
evidence, the token set, delegations, residual risks, and blocked steps.

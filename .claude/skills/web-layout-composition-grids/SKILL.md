---
name: web-layout-composition-grids
description: Complex responsive page architecture and compositional layout for the static AFKERIAN INTERACTIVE website (HTML5 + CSS, no framework) — page structure and section rhythm, CSS Grid/Flexbox composition, editorial and asymmetric layouts, container queries for component-level responsiveness, cascade layers for architecture, and intrinsic layout that avoids overflow. Activate when architecting or reviewing page-level layout and grids. Do not activate for Android, Unity, or fluid-sizing/breakpoint mechanics owned by the responsive skill.
---

# Web Layout, Composition & Grids

## 1. Purpose
Architect page-level composition: a deliberate grid, section rhythm, and layout system
(including editorial/asymmetric structures) that hold together responsively and stay
maintainable — the spatial counterpart to the type/color system.

## 2. Activate When
- Architecting a page's structure, grid, and section rhythm.
- Building complex or editorial layouts with CSS Grid/Flexbox.
- Introducing container queries or cascade layers for layout architecture.

## 3. Do Not Activate When
- The task is Android or Unity.
- The task is fluid sizing, breakpoint tokens, touch targets, or overflow mechanics
  (`web-responsive-design-system`).
- The task is only type/color/token work (`web-typography-color-design-tokens`).

## 4. Scope and Authority
Obey the active CLAUDE.md / AGENTS.md / GEMINI.md and project governance. This skill
provides technical expertise only and grants no independent execution authority.

## 5. Required Evidence
- The approved direction and token system.
- The current HTML structure and CSS layout.

## 6. Current Documentation Verification
Confirm Grid, Flexbox, container queries, and cascade-layer behavior against primary
sources (W3C CSS specs, MDN, web.dev). See `references/official-sources.md`.

## 7. Composition Workflow
1. Define the page's structural grid (columns, gutters, max content measure) with CSS Grid.
2. Set vertical rhythm between sections using space tokens; make spacing intentional, not
   uniform-by-default.
3. Compose distinctive structure (asymmetry, overlap, editorial emphasis) where the
   direction calls for it, keeping a clear reading order.
4. Use Flexbox for one-dimensional component alignment; Grid for two-dimensional structure.

## 8. Architecture Guidance
- Prefer intrinsic, content-driven layout (`min()`, `max()`, `clamp()`, `minmax()`,
  `auto-fit`/`auto-fill`) so layouts adapt without a breakpoint per case.
- Use container queries for component-level responsiveness; use cascade layers to order
  layout, components, and utilities predictably.
- Never introduce horizontal overflow; keep source order and DOM/visual order aligned.

## 9. Validation Workflow
- Verify structure holds from small to large viewports and at 200% zoom/reflow.
- Confirm no horizontal scroll; confirm reading order matches visual order.
- Hand responsive-mechanics evidence to `web-responsive-design-system`.

## 10. Delegation and Overlap
- Fluid sizing, breakpoint tokens, touch targets, overflow rules → `web-responsive-design-system`.
- Type/color/tokens → `web-typography-color-design-tokens`.
- Direction → `web-creative-direction-visual-language`.
- Reflow/reading-order conformance → `web-accessibility-wcag`; layout shift (CLS) →
  `web-performance-core-web-vitals`.

## 11. Stop Conditions
- The desired composition would require a framework, build step, or new dependency
  (needs OWNER approval).
- Structure cannot preserve reading order or avoid overflow within scope.

## 12. Final Report
State: grid and structure, section rhythm, distinctive compositional choices, container/
layer architecture used, reflow/overflow checks, delegations, and blocked steps.

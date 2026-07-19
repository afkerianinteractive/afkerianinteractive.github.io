---
name: web-visual-critique-quality-gates
description: Visual critique, refinement, and anti-generic-AI quality gates for the static AFKERIAN INTERACTIVE website — structured design review, distinctiveness and consistency checks, spacing/alignment/hierarchy scrutiny, and objective gates (contrast, reflow, Core Web Vitals, console) before sign-off. Activate to critique or gate a design's quality and distinctiveness. Do not activate for Android, Unity, or as authorization to implement changes.
---

# Web Visual Critique & Quality Gates

## 1. Purpose
Provide a repeatable critique and a set of pass/fail gates that catch generic, inconsistent,
or unpolished output before it ships — combining subjective design judgment with objective,
measurable thresholds.

## 2. Activate When
- Reviewing a page or component for visual quality and distinctiveness.
- Refining spacing, alignment, hierarchy, and consistency.
- Gating a change before OWNER sign-off.

## 3. Do Not Activate When
- The task is Android or Unity review.
- The activity is implementing features/redesign (this skill critiques; it does not
  authorize work).

## 4. Scope and Authority
Obey the active CLAUDE.md / AGENTS.md / GEMINI.md and project governance. This skill
provides technical expertise only and grants no independent execution authority. Findings
are recommendations for the OWNER.

## 5. Required Evidence
- The rendered page (or preview) and its CSS.
- Objective outputs where available: contrast checks, Lighthouse/CWV, console log.

## 6. Current Documentation Verification
Anchor objective gates in primary sources (WCAG, web.dev/Core Web Vitals, MDN).
See `references/official-sources.md`.

## 7. Critique Workflow (subjective)
1. Distinctiveness: does it read as specific to this subject, or as a generic template?
   Name the templated tells (default fonts, single accent on white, evenly-centered hero,
   uniform spacing) and whether they are deliberate.
2. Hierarchy: is the primary action/message unmistakable? Is scale/contrast used with intent?
3. Consistency: are type, color, spacing, and radii driven by tokens? Flag one-off values.
4. Craft: alignment, optical spacing, rhythm, and edge cases (long text, empty states).

## 8. Quality Gates (objective — must pass)
- Contrast meets WCAG 2.2 AA (1.4.3 / 1.4.11) — evidence via `web-accessibility-wcag`.
- Keyboard operable with visible focus; reduced-motion respected.
- No horizontal overflow; content survives 200% zoom/reflow.
- Core Web Vitals within targets — evidence via `web-performance-core-web-vitals`.
- Clean browser console (no errors) on the reviewed page.

## 9. Refinement Workflow
- Prioritize findings by severity; propose the smallest diffs that raise distinctiveness or
  fix a failed gate. Separate "evidence" from "assumption" in every finding.

## 10. Delegation and Overlap
- Direction disputes → `web-creative-direction-visual-language`.
- Token/type/color fixes → `web-typography-color-design-tokens`.
- Layout fixes → `web-layout-composition-grids`; interaction/motion → `web-interaction-motion-design`.
- Conformance evidence → `web-accessibility-wcag`; performance evidence →
  `web-performance-core-web-vitals`; security review → `web-static-security-content-policy`.

## 11. Stop Conditions
- A gate fails and cannot be fixed within approved scope — report, do not bypass.
- Fixes would require redesign or dependencies beyond OWNER approval.

## 12. Final Report
State: distinctiveness verdict with named tells, hierarchy/consistency/craft findings
(evidence vs assumption), gate results (pass/fail with source), prioritized fixes, and
blocked steps.

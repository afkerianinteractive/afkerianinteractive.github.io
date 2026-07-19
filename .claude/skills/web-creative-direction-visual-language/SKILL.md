---
name: web-creative-direction-visual-language
description: Creative direction and distinctive visual language for the static AFKERIAN INTERACTIVE website — brief and subject grounding, a defensible art direction, brand voice expressed visually, deliberate palette/type/imagery direction, and moodboard-to-page translation that avoids generic AI-template output. Activate when setting or reviewing the visual direction, identity, or distinctiveness of a page. Do not activate for Android, Unity, pure WCAG conformance, or SEO-only work.
---

# Web Creative Direction & Visual Language

## 1. Purpose
Give each page a deliberate, defensible visual identity that is specific to AFKERIAN
INTERACTIVE and its subject — not a templated default. Establish the direction (mood,
voice, references, one justified aesthetic risk) that the typography, color, layout, and
motion skills then execute.

## 2. Activate When
- Setting or revising the art direction / visual language of a page or the site.
- A design reads as generic, templated, or interchangeable and needs a point of view.
- Translating a brief, brand voice, or subject matter into concrete visual direction.

## 3. Do Not Activate When
- The task is Android or Unity visual work.
- The task is purely WCAG conformance (`web-accessibility-wcag`) or SEO metadata
  (`web-seo-metadata-structured-data`) with no direction decision.
- Execution-level type/color/layout/motion is already directed — use the specialist skill.

## 4. Scope and Authority
Obey the active CLAUDE.md / AGENTS.md / GEMINI.md and project governance. This skill
provides technical expertise only and grants no independent execution authority. The OWNER
approves direction, redesign, and scope.

## 5. Required Evidence
- The brief or, if absent, an explicitly stated subject: what the product/page is, its
  audience, and the page's single job.
- Existing brand assets, the current page, and any OWNER preferences.

## 6. Current Documentation Verification
Ground direction in current primary web/design documentation, not trends alone. See
`references/official-sources.md`.

## 7. Direction Workflow
1. Pin the subject: name the product/page, audience, and its one job; state it plainly.
2. Derive material: draw distinctive cues from the subject's own world (its artifacts,
   vocabulary, textures), not from stock "modern SaaS" tropes.
3. Choose a stance: define 3–5 adjectives for the intended feel and one anti-goal.
4. Commit direction: set palette intent, type personality, imagery/iconography stance,
   density, and one justified aesthetic risk. Record the rationale.
5. Establish reference points and non-negotiables (contrast, brand marks, legibility).

## 8. Implementation Guidance
- Express brand voice through concrete, coherent choices; avoid defaulting to system fonts,
  center-everything hero, and a single accent on white unless that is a deliberate choice.
- Keep the direction internally consistent and reusable as tokens (hand off to
  `web-typography-color-design-tokens`).
- Every distinctive choice must survive the accessibility floor; never trade conformance
  for style.

## 9. Validation Workflow
- Restate the direction in one paragraph; confirm it is specific to this subject and could
  not be swapped onto an unrelated site.
- Sanity-check against the anti-generic gates in `web-visual-critique-quality-gates`.

## 10. Delegation and Overlap
- Type/color/token execution → `web-typography-color-design-tokens`.
- Page composition/grids → `web-layout-composition-grids`.
- Interaction/motion feel → `web-interaction-motion-design`.
- Conformance floor → `web-accessibility-wcag`; measured quality → `web-visual-critique-quality-gates`.

## 11. Stop Conditions
- The subject/brief cannot be pinned and the OWNER has not chosen one.
- The direction would require redesign, new dependencies, or scope beyond OWNER approval.

## 12. Final Report
State: subject and job, chosen direction and rationale, the one aesthetic risk, how it
stays distinctive and accessible, hand-offs to specialist skills, and blocked steps.

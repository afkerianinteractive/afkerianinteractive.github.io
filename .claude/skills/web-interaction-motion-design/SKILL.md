---
name: web-interaction-motion-design
description: Production interaction and motion design for the static AFKERIAN INTERACTIVE website (HTML5 + CSS, minimal JS) — purposeful transitions and animation, interaction states (hover/focus/active/disabled), easing and duration systems, scroll/reveal restraint, and full accessibility (prefers-reduced-motion, no motion traps, keyboard parity). Activate when designing or reviewing interaction and motion. Do not activate for Android, Unity, framework animation libraries, or pure WCAG audits.
---

# Web Interaction & Motion Design

## 1. Purpose
Design interaction and motion that add clarity and character without harming usability,
performance, or accessibility — coherent states, purposeful transitions, and motion that
every user can opt out of.

## 2. Activate When
- Designing interaction states and feedback (hover/focus/active/disabled/loading).
- Adding transitions, animation, or scroll-triggered reveals.
- Establishing an easing/duration system or reviewing motion accessibility.

## 3. Do Not Activate When
- The task is Android or Unity motion.
- The task requires a JS animation framework or build tooling (needs OWNER approval;
  preserve the static, minimal-JS architecture).
- The task is only a WCAG audit (`web-accessibility-wcag`).

## 4. Scope and Authority
Obey the active CLAUDE.md / AGENTS.md / GEMINI.md and project governance. This skill
provides technical expertise only and grants no independent execution authority.

## 5. Required Evidence
- The approved direction, token system, and current interactive elements.
- Keyboard and reduced-motion observations.

## 6. Current Documentation Verification
Confirm transitions, animations, the Web Animations API, and reduced-motion/WCAG behavior
against primary sources (MDN, W3C, WCAG). See `references/official-sources.md`.

## 7. Interaction Workflow
1. Define every interactive state, including visible `:focus-visible`, active, and disabled.
2. Ensure pointer and keyboard parity; never rely on hover alone to reveal essential content.
3. Give feedback for asynchronous or state changes (loading, success, error) accessibly.

## 8. Motion Workflow
- Use motion purposefully (orientation, continuity, feedback); prefer CSS transitions/
  animations; keep durations short and easing consistent as tokens.
- Respect `prefers-reduced-motion: reduce` — remove or substitute non-essential motion.
- Avoid content that auto-moves/blinks without a pause/stop control (WCAG 2.2.2) and avoid
  motion triggered by interaction that cannot be disabled (WCAG 2.3.3); avoid flashing
  (WCAG 2.3.1).
- Keep animation cheap (transform/opacity) to protect INP/CLS (delegate measurement to
  `web-performance-core-web-vitals`).

## 9. Validation Workflow
- Keyboard-only pass: all interactions reachable and operable with visible focus.
- Toggle reduced-motion and confirm essential meaning survives without motion.
- Confirm no layout thrash or jank on interaction.

## 10. Delegation and Overlap
- Focus/keyboard/reduced-motion conformance evidence → `web-accessibility-wcag`.
- INP/CLS and animation cost measurement → `web-performance-core-web-vitals`.
- Visual style of states → `web-typography-color-design-tokens` / `web-creative-direction-visual-language`.

## 11. Stop Conditions
- The interaction needs a framework, library, or build step without OWNER approval.
- Motion cannot be made reduced-motion-safe within scope.

## 12. Final Report
State: interaction states and parity, motion system (easing/duration), reduced-motion
handling, keyboard and performance checks, delegations, residual risks, and blocked steps.

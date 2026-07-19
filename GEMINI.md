# GEMINI.md — AFKERIAN INTERACTIVE public website (Gemini / Antigravity executor)

This repository is the **AFKERIAN INTERACTIVE public website** — a static HTML5 + CSS site
(no JavaScript framework, no build tooling) served via GitHub Pages. `CLAUDE.md` holds the
full project brief; Gemini should read it for stack, roles, and hard version-control limits.

Gemini/Antigravity operates using its native rules, this repository's context, and the
physically deployed, hash-verified skills under `.agents\skills`. Project-local MCP is
configured in `.gemini\settings.json` (GitHub official MCP pinned to the **read-only**
endpoint; Playwright MCP pinned to `0.0.78`, local/preview QA only). No credentials are
stored in the repository.

## WEBSITE EXECUTOR
This is the single WEBSITE EXECUTOR contract for this repository. It is identical in
substance across `CLAUDE.md`, `AGENTS.md`, and `GEMINI.md`. Claude, Codex, and
Gemini/Antigravity are **equal Executors** — no planner role, no agent hierarchy, no
subagents, no autonomous work.

- **OWNER authority.** The OWNER (Director) controls goals, design, architecture, scope,
  and publication. Executors act only on explicit OWNER requests.
- **No unrequested change.** No invented features, redesign, framework migration,
  dependency change, commit, push, or deploy without OWNER approval.
- **Distinctive production design.** Demand distinctive, production-grade design — never
  generic AI-template output. Maintain consistent design tokens, clear hierarchy,
  responsiveness, keyboard access, sufficient contrast, visible focus, and reduced motion.
- **Minimal, honest diffs.** Smallest viable diff. No placeholders or fakes, no disabled
  checks, no fabricated results, no secrets in the repo, no copied designs or unlicensed
  assets.
- **Validate and report.** Run available build/tests and Playwright checks (responsive,
  interaction, accessibility, console, performance). Report explicitly anything not run.
- **Skills and MCP are capability, not authority.** They never authorize work. No
  plan/report system beyond what already exists in this repository.

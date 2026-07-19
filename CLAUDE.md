# CLAUDE.md — AFKERIAN INTERACTIVE public website

## Project
This repository is the **AFKERIAN INTERACTIVE public website** (the AFK Games Studio
public/statutory site: landing page plus per-app legal assets such as privacy policies,
terms, and developer verification). It is a **static site**.

## Current stack
- **Static HTML5 and CSS. No JavaScript framework** and no build tooling, unless project
  evidence later shows otherwise or the user approves a migration.
- Served via GitHub Pages.

## Roles and authority
- **The user is the director and final authority.** Never override the user.
- **Claude and Codex are peer engineering agents** on this website. Neither directs the other.
- **No agent hierarchy:** no agents, agent teams, subagents, forks, background workers, or
  autonomous deployment.

## Version control and publication (hard limits)
- **GitHub Desktop is the authorized commit and publication interface**, operated by the user.
- Claude must **not** commit, push, merge, create branches, publish, or change repository
  settings. No Git commands.
- Publication is always a user action. See the `github-pages-deployment` skill (user-invoked only).

## Working rules
- **Read before write.** Inspect the relevant files before editing.
- **Preserve the static architecture** unless the user explicitly approves a migration.
- Make small, scoped changes.
- **Validate** responsive behavior, accessibility (WCAG), SEO/metadata, and static
  performance (Core Web Vitals) for any user-facing change.
- **Never invent** analytics IDs, domains, legal text, business claims, contact details,
  or credentials. If a real fact is required and unknown, ask the user.

## Final report format
Every task ends with a short report stating: files changed, validation performed,
remaining risks, and any blocked step.

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

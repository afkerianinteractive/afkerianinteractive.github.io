---
name: github-pages-deployment
disable-model-invocation: true
description: Manual, user-invoked GitHub Pages deployment workflow for the static AFKERIAN INTERACTIVE website — branch-served Pages architecture, repository status inspection, CNAME/custom-domain readiness, static path correctness, 404 behavior, cache/propagation expectations, and an explicit pre-publication checklist. Publication is performed by the user via GitHub Desktop; this skill runs no Git commands and mutates no repository settings. Invoke explicitly before or after a manual publish.
---

# GitHub Pages Deployment (Manual, User-Invoked)

## 1. Purpose
Provide a safe, explicit pre-publication checklist and post-publication verification for
the branch-served GitHub Pages site. This skill never runs Git or changes repository
settings; the user publishes via GitHub Desktop.

## 2. Activate When
- The user explicitly invokes this skill before or after a manual publish.
- Preparing a pre-publication checklist or verifying a completed publish.

## 3. Do Not Activate When
- Any automatic/model-triggered activation (this skill is user-invocation only).
- The target is Android or Unity.
- The request is to commit, push, merge, or change repo settings (never do this).

## 4. Scope and Authority
Obey the active CLAUDE.md and project governance. This skill provides technical expertise only and grants no independent execution authority.
No Git commands. No commit/push/merge/branch. No repository-settings changes.
GitHub Desktop is the publication mechanism, operated by the user.

## 5. Required Evidence
- Repository working-tree status (read-only inspection).
- Pages configuration facts (which branch/path serves Pages) as stated by the user or read-only.
- CNAME/custom-domain intent from the user.

## 6. Current Documentation Verification
Confirm current GitHub Pages behavior against primary sources.
See `references/official-sources.md`.

## 7. Inspection Workflow
1. Review the working tree for intended vs unintended changes (read-only).
2. Confirm the Pages source branch/path and that built output paths are correct/relative.
3. Check CNAME file matches the intended custom domain (if any).
4. Confirm a 404 page exists and links/assets use correct static paths.

## 8. Implementation Workflow (checklist only)
- Produce an explicit pre-publication checklist for the user.
- Do NOT execute any Git or deployment action.
- Hand off to the user to publish via GitHub Desktop.

## 9. Validation Workflow (after user publishes)
- After the user confirms publication, verify the live site (links, assets, 404).
- Note cache/propagation delay (changes may take minutes to appear).

## 10. Delegation and Overlap
- Metadata correctness → `web-seo-metadata-structured-data`.
- Security headers → `web-static-security-content-policy`.
- Performance → `web-performance-core-web-vitals`.

## 11. Stop Conditions
- Any step would require a Git command or repo-settings change (stop; hand to user).
- Custom-domain or Pages facts cannot be confirmed.

## 12. Final Report
State: checklist produced, items verified (pre), and — after user publish — live
verification results, cache/propagation notes, residual risks, blocked steps.
Never state that Claude published or ran Git.

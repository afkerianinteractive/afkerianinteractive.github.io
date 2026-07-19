---
name: web-static-security-content-policy
description: Static-site security and content policy for the AFKERIAN INTERACTIVE website — static-site threat model, external resource inventory, Content-Security-Policy design, referrer and permissions policy relevance, integrity/crossorigin attributes, unsafe-inline-style constraints, mixed content, and link safety. Activate when reviewing or hardening the static site's security headers and content policy. Do not activate for Android, Unity, or server-side controls the static host does not provide.
---

# Web Static Security & Content Policy

## 1. Purpose
Harden the static website within the limits of static hosting: an accurate threat model,
a tight Content-Security-Policy grounded in the real external-resource inventory, safe
referrer/permissions posture, subresource integrity, and no mixed content.

## 2. Activate When
- Reviewing/adding CSP or other security headers/meta.
- Inventorying external resources and link safety.
- Assessing mixed content or integrity/crossorigin needs.

## 3. Do Not Activate When
- The target is Android or Unity.
- The control requires server-side capability the static host lacks.

## 4. Scope and Authority
Obey the active CLAUDE.md and project governance. This skill provides technical expertise only and grants no independent execution authority.
Do not claim server-side controls that do not exist on the static host.

## 5. Required Evidence
- The actual external resources referenced (scripts, styles, fonts, images, links).
- How headers can be delivered on the host (meta vs true headers; GitHub Pages limits).

## 6. Current Documentation Verification
Confirm CSP directives and header support against primary sources (MDN, web.dev).
See `references/official-sources.md`.

## 7. Inspection Workflow
1. Inventory all external origins the site loads.
2. Draft a CSP allowing only those origins; avoid `unsafe-inline` where feasible.
3. Check referrer policy and permissions-policy relevance.
4. Add `integrity`+`crossorigin` for third-party scripts/styles where applicable.
5. Check for mixed content and `rel="noopener noreferrer"` on external links.

## 8. Implementation Workflow
- Apply the least-privilege CSP that matches the inventory.
- Add link safety attributes and integrity where possible.
- Note which headers require host support vs `<meta http-equiv>`.

## 9. Validation Workflow
- Verify the site still functions under the CSP (no blocked required resources).
- Confirm no mixed content and safe external links.

## 10. Delegation and Overlap
- Asset performance → `web-performance-core-web-vitals`.
- Publication → `github-pages-deployment`.

## 11. Stop Conditions
- A required control needs server capabilities unavailable on the host.
- CSP cannot be validated without breaking the site.

## 12. Final Report
State: external inventory, CSP/headers applied, link-safety/integrity fixes, host
limitations, residual risks, blocked steps.

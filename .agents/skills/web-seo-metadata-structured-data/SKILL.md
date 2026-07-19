---
name: web-seo-metadata-structured-data
description: SEO metadata and structured data for the static AFKERIAN INTERACTIVE website — title and meta description, canonical URL, Open Graph and Twitter cards, robots and sitemap, favicon and social image references, and Organization/WebSite JSON-LD validated against schema.org. Activate when reviewing or implementing on-page SEO metadata or structured data on the static site. Do not activate for Android, Unity, or content that would fabricate business or domain data.
---

# Web SEO Metadata & Structured Data

## 1. Purpose
Give the static site accurate, non-duplicated on-page SEO metadata and valid structured
data: titles/descriptions, canonical URLs, social cards, robots/sitemap, and schema.org
JSON-LD — without fabricating business facts.

## 2. Activate When
- Reviewing/adding `<title>`, meta description, canonical, OG/Twitter tags.
- Adding robots/sitemap references or Organization/WebSite JSON-LD.
- Validating structured data.

## 3. Do Not Activate When
- The target is Android or Unity.
- The task would require inventing business data, a domain, or analytics IDs.

## 4. Scope and Authority
Obey the active CLAUDE.md and project governance. This skill provides technical expertise only and grants no independent execution authority.
Never fabricate business names, domains, addresses, or IDs.

## 5. Required Evidence
- The page `<head>` content and existing metadata.
- The real, confirmed domain/brand facts (from the user; never invented).

## 6. Current Documentation Verification
Confirm metadata/structured-data requirements against primary sources (Google Search
Central, schema.org, MDN). See `references/official-sources.md`.

## 7. Inspection Workflow
1. Check unique title + meta description per page.
2. Check canonical URL and absence of conflicting/duplicate metadata.
3. Check Open Graph + Twitter card tags and social image references.
4. Check robots meta / robots.txt and sitemap presence.
5. Validate JSON-LD (Organization, WebSite) types against schema.org.

## 8. Implementation Workflow
- Add/correct metadata using only confirmed facts.
- Add valid JSON-LD; keep one canonical per page.
- Reference real favicon/social image assets that exist.

## 9. Validation Workflow
- Validate structured data with the Rich Results/schema validators.
- Confirm no duplicate/conflicting tags remain.

## 10. Delegation and Overlap
- Performance of assets → `web-performance-core-web-vitals`.
- Accessibility → `web-accessibility-wcag`.
- Publication → `github-pages-deployment`.

## 11. Stop Conditions
- Required business/domain facts are unknown (ask the user; do not invent).
- Structured data cannot be validated.

## 12. Final Report
State: pages reviewed, metadata/JSON-LD changes, validation results, any facts needed
from the user, residual risks, blocked steps.

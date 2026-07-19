# Official Sources — web-static-security-content-policy

Documentation verified: 2026-07-17. Primary sources only.

- MDN Content Security Policy (CSP) — https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
- MDN CSP directives — https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
- MDN Referrer-Policy — https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
- MDN Permissions-Policy — https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy
- MDN Subresource Integrity — https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity
- MDN Mixed content — https://developer.mozilla.org/en-US/docs/Web/Security/Mixed_content
- web.dev CSP — https://web.dev/articles/csp

Notes:
- GitHub Pages cannot set arbitrary response headers; some controls only work via <meta http-equiv> and have limits (e.g. frame-ancestors requires a real header).
- Use rel="noopener noreferrer" on target=_blank links.
- Base CSP on the real external-resource inventory (least privilege).

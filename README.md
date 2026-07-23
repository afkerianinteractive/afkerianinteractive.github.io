# Jesus Afkerian

Public website and canonical legal-document repository for software published by Jesus Afkerian.

## Legal document maintenance

Canonical legal text lives in UTF-8 `.txt` files under each product's `legal/` directory and in the root `legal/` directory. HTML legal routes are presentation shells that load the corresponding same-origin TXT. The viewer creates semantic elements with `createElement` and assigns untrusted text through `textContent`; it does not interpret TXT content as HTML.

Use `python tools/legal_docs.py refresh` after an authorized TXT change, then run `python tools/legal_docs.py validate`. To compare a product with its Android offline assets without writing to that repository, run `python tools/legal_docs.py compare --product <product-slug> --android-root <absolute-android-repository-path>`.

`legal/android-copy-map.json` is generated from the manifest and contains all 20 modified English documents that would require an owner-controlled copy into the three read-only Android repositories: nine main documents and eleven individual notices. The historical 15-file request and the five additional consistency documents remain separately identified inside the map for traceability. Its status remains blocked until owner-controlled creative-rights evidence and final review are complete. Notices are editable first-party summaries; only authentic license texts marked `protected_upstream` are byte-protected.

`legal/dependency-license-bom.json` records the resolved release runtime components and their license or governing-terms evidence. Regenerate it with `python tools/license_audit.py`; any unresolved or ambiguous classification blocks license sign-off.

Publishing, Android asset synchronization, Google Play configuration and legal approval remain owner-controlled actions.

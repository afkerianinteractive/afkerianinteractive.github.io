# Jesus Afkerian

Public website and canonical legal-document repository for software published by Jesus Afkerian.

## Legal document maintenance

Canonical legal text lives in UTF-8 `.txt` files under each product's `legal/` directory and in the root `legal/` directory. HTML legal routes are presentation shells that load the corresponding same-origin TXT without interpreting it as markup.

Use `python tools/legal_docs.py refresh` after an authorized TXT change, then run `python tools/legal_docs.py validate`. To compare a product with its Android offline assets without writing to that repository, run `python tools/legal_docs.py compare --product <product-slug> --android-root <absolute-android-repository-path>`.

Publishing, Android asset synchronization, Google Play configuration and legal approval remain owner-controlled actions.

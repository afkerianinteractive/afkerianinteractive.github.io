#!/usr/bin/env python3
"""Validate and compare Jesus Afkerian canonical legal TXT files.

Normalization is intentionally narrow:
1. remove one optional UTF-8 BOM;
2. convert CRLF and bare CR to LF;
3. preserve everything else, including a terminal newline.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "legal" / "manifest.json"
QR_BASELINE_PATH = ROOT / "legal" / "qr-regression-baseline.json"
MARKET_PATH = ROOT / "legal" / "market-review.json"
MARKET_REPORT_PATH = ROOT / "legal" / "MARKET_REVIEW.md"
COPY_MAP_PATH = ROOT / "legal" / "android-copy-map.json"
ALLOWED_MARKET_STATUSES = {
    "APPROVED_FOR_OWNER_ENABLEMENT",
    "DOCUMENT_READY_CONSOLE_UNVERIFIED",
    "MARKET_HOLD_LEGAL_INPUT",
    "MARKET_HOLD_LANGUAGE",
    "MARKET_HOLD_PRODUCT_CHANGE",
    "MARKET_HOLD_SOURCE_UNAVAILABLE",
    "NOT_SUPPORTED_OR_SANCTIONS_REVIEW",
    "MARKET_HOLD_PLATFORM_IDENTITY",
    "EXCLUDED_BY_OWNER",
    "EXCLUDED_BY_OWNER_PRIVACY_REQUIREMENT",
    "OUT_OF_SCOPE_EUROPEAN_OR_UK_TERRITORY",
}
CORE_IDS = {
    "PRIVACY_POLICY",
    "TERMS_OF_SERVICE",
    "THIRD_PARTY_NOTICES",
    "WEBSITE_PRIVACY_POLICY",
    "WEBSITE_TERMS_OF_SERVICE",
    "PERMITTED_TERRITORY",
}
DISPLAY_DATES = {
    "2026-07-22": {
        "en-US": "July 22, 2026",
        "es-419": "22 de julio de 2026",
    },
    "2026-07-23": {
        "en-US": "July 23, 2026",
        "es-419": "23 de julio de 2026",
    },
    "2026-07-24": {
        "en-US": "July 24, 2026",
        "es-419": "24 de julio de 2026",
    },
}
LEGACY_PUBLIC_IDENTITIES = re.compile(
    r"\b(?:AFKERIAN\s+INTERACTIVE|AFK\s+GAMES\s+STUDIO|JAfkerian)\b",
    flags=re.I,
)
# Identities that may never appear in any first-party presentation.
BANNED_PUBLIC_IDENTITIES = re.compile(
    r"\b(?:AFK\s+GAMES\s+STUDIO|JAfkerian)\b",
    flags=re.I,
)
# AFKERIAN INTERACTIVE is a brand, never a legal person. First-party TXT may use
# it only when the document also states, verbatim, that Jesus Afkerian is the
# operator behind it. HTML keeps the unconditional LEGACY_PUBLIC_IDENTITIES ban.
OPERATOR_BRAND = re.compile(r"\bAFKERIAN\s+INTERACTIVE\b", flags=re.I)
# A first-party document may use the AFKERIAN INTERACTIVE brand only when it also
# ties the brand to Jesus Afkerian as its operator. Any of these verbatim ties
# satisfies the guard; the OWNER-approved policy opening uses the "persona física
# que opera" / "a natural person operating" wording.
OPERATOR_BRAND_FORMULAS = {
    "en-US": (
        "Jesus Afkerian, a natural person operating under the AFKERIAN INTERACTIVE brand",
        "Jesus Afkerian, operating under the AFKERIAN INTERACTIVE brand",
        "Jesus Afkerian, an individual who operates and publishes the Game under the AFKERIAN INTERACTIVE brand",
    ),
    "es-419": (
        "Jesus Afkerian, persona física que opera bajo la marca AFKERIAN INTERACTIVE",
        "Jesus Afkerian, operando bajo la marca AFKERIAN INTERACTIVE",
        "Jesus Afkerian, persona física que opera y publica el Juego bajo la marca AFKERIAN INTERACTIVE",
    ),
}
REQUESTED_COPY_PATHS = {
    "xo-arcade/legal/PRIVACY_POLICY.txt",
    "xo-arcade/legal/TERMS_OF_SERVICE.txt",
    "xo-arcade/legal/THIRD_PARTY_NOTICES.txt",
    "xo-arcade/legal/ELEVENLABS_NOTICE.txt",
    "xo-arcade/legal/KENNEY_NOTICE.txt",
    "xo-arcade/legal/SUNO_NOTICE.txt",
    "air-strike-arcade/legal/PRIVACY_POLICY.txt",
    "air-strike-arcade/legal/TERMS_OF_SERVICE.txt",
    "air-strike-arcade/legal/THIRD_PARTY_NOTICES.txt",
    "air-strike-arcade/legal/SUNO_NOTICE.txt",
    "tap-odyssey/legal/PRIVACY_POLICY.txt",
    "tap-odyssey/legal/TERMS_OF_SERVICE.txt",
    "tap-odyssey/legal/THIRD_PARTY_NOTICES.txt",
    "tap-odyssey/legal/OPENAI_CHATGPT_NOTICE.txt",
    "tap-odyssey/legal/SUNO_NOTICE.txt",
}
OWNER_AUTHORED_NOTICE_PATHS = {
    "xo-arcade/legal/AD_SERVICES_NOTICE.txt",
    "xo-arcade/legal/ELEVENLABS_NOTICE.txt",
    "xo-arcade/legal/KENNEY_NOTICE.txt",
    "xo-arcade/legal/SUNO_NOTICE.txt",
    "air-strike-arcade/legal/AD_SERVICES_NOTICE.txt",
    "air-strike-arcade/legal/PIXABAY_NOTICE.txt",
    "air-strike-arcade/legal/SUNO_NOTICE.txt",
    "tap-odyssey/legal/AD_SERVICES_NOTICE.txt",
    "tap-odyssey/legal/OPENAI_CHATGPT_NOTICE.txt",
    "tap-odyssey/legal/PIXABAY_NOTICE.txt",
    "tap-odyssey/legal/SUNO_NOTICE.txt",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def safe_repo_path(relative: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or not pure.parts:
        raise ValueError(f"unsafe repository path: {relative!r}")
    resolved = (ROOT / Path(*pure.parts)).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {relative!r}") from exc
    return resolved


def normalized_bytes(raw: bytes) -> bytes:
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    text = raw.decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def hashes(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    normalized = normalized_bytes(raw)
    return {
        "size_bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest().upper(),
        "normalized_sha256": hashlib.sha256(normalized).hexdigest().upper(),
    }


def text_for(entry: dict[str, Any]) -> str:
    return normalized_bytes(safe_repo_path(entry["canonical_path"]).read_bytes()).decode("utf-8")


def metadata_value(text: str, language: str, key_en: str, key_es: str) -> str | None:
    key = key_es if language == "es-419" else key_en
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    return match.group(1) if match else None


def route_expected_source(entry: dict[str, Any]) -> str:
    route = PurePosixPath(entry["html_route"])
    start = str(route.parent)
    if start == ".":
        start = ""
    return posixpath.relpath(entry["canonical_path"], start=start or ".")


def market_report_text(market: dict[str, Any]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "# Americas market review",
        "",
        f"Reviewed: {market.get('reviewed_on', 'UNVERIFIED')}",
        "",
        "This generated review aid is not legal advice, country approval, console evidence, or a launch authorization. The machine-readable source is `legal/market-review.json`.",
        "",
        f"Google Play public profile: `{market.get('google_play_public_profile_status', 'UNVERIFIED')}`",
        f"Cross-market platform identity gate: `{market.get('platform_identity_gate', 'UNVERIFIED')}`",
        "",
        "All rows inherit the cross-market evidence and unresolved fields in the JSON source. A hold or exclusion is not cured by this report.",
        "",
        "| Market / region | Languages | Disposition | Public permitted list | Exact blocker or gate | Official sources |",
        "|---|---|---|---:|---|---|",
    ]
    for row in market.get("markets", []):
        sources = "<br>".join(f"<{url}>" for url in row.get("official_sources", []))
        lines.append(
            "| "
            + " | ".join(
                [
                    cell(row.get("market", "")),
                    cell(", ".join(row.get("languages", []))),
                    f"`{cell(row.get('status', ''))}`",
                    "yes" if row.get("permitted") else "no",
                    cell(row.get("gate", "")),
                    sources,
                ]
            )
            + " |"
        )
    lines.extend(["", "Generated deterministically by `python tools/legal_docs.py refresh`.", ""])
    return "\n".join(lines)


def copy_map_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "product_id": entry["product_id"],
        "source_path": entry["canonical_path"],
        "android_repository": entry["android_repository"],
        "android_destination": entry["android_destination"],
        "size_bytes": entry["size_bytes"],
        "sha256": entry["sha256"],
        "normalized_sha256": entry["normalized_sha256"],
    }


def copy_map_value(manifest: dict[str, Any]) -> dict[str, Any]:
    entries = [
        entry
        for entry in manifest["documents"]
        if entry.get("manual_copy_required") and entry.get("android_destination")
    ]
    requested = [
        copy_map_entry(entry)
        for entry in entries
        if entry["canonical_path"] in REQUESTED_COPY_PATHS
    ]
    additional = [
        copy_map_entry(entry)
        for entry in entries
        if entry["canonical_path"] not in REQUESTED_COPY_PATHS
    ]
    return {
        "schema_version": 1,
        "generated_on": manifest.get("generated_on"),
        "status": "BLOCKED_PENDING_OWNER_CREATIVE_RIGHTS_EVIDENCE_AND_FINAL_REVIEW",
        "requested_copy_count": len(requested),
        "additional_consistency_copy_count": len(additional),
        "total_copy_count": len(requested) + len(additional),
        "requested_copy_entries": requested,
        "additional_consistency_entries": additional,
    }


def refresh() -> int:
    manifest = load_json(MANIFEST_PATH)
    failures: list[str] = []
    for entry in manifest["documents"]:
        canonical = entry["canonical_path"]
        if (
            entry["product_id"] in {"xo-arcade", "air-strike-arcade", "tap-odyssey"}
            and entry["document_id"] in {
                "PRIVACY_POLICY",
                "TERMS_OF_SERVICE",
                "THIRD_PARTY_NOTICES",
            }
            and entry["language"] == "es-419"
        ):
            entry["manual_copy_required"] = False
        if canonical in OWNER_AUTHORED_NOTICE_PATHS:
            entry.update(
                {
                    "version": "2026-07-22",
                    "effective_date": "2026-07-22",
                    "last_updated": "2026-07-22",
                    "manual_copy_required": True,
                    "protected_upstream": False,
                    "byte_preserved_from_android": False,
                    "first_party": True,
                }
            )
        try:
            path = safe_repo_path(canonical)
        except ValueError as exc:
            failures.append(str(exc))
            continue
        if not path.is_file():
            failures.append(f"missing canonical file: {entry['canonical_path']}")
            continue
        current = hashes(path)
        expected = entry.get("protected_expected_sha256")
        if entry.get("protected_upstream") and expected and current["sha256"] != expected:
            failures.append(
                f"protected upstream bytes changed: {entry['canonical_path']} "
                f"expected {expected}, got {current['sha256']}"
            )
            continue
        entry.update(current)
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1
    dates = [d.get("last_updated") for d in manifest["documents"] if d.get("last_updated")]
    manifest["generated_on"] = max(dates) if dates else None
    write_json(MANIFEST_PATH, manifest)
    write_json(COPY_MAP_PATH, copy_map_value(manifest))
    market = load_json(MARKET_PATH)
    MARKET_REPORT_PATH.write_text(
        market_report_text(market), encoding="utf-8", newline="\n"
    )
    print(f"Refreshed {len(manifest['documents'])} manifest entries.")
    print(f"Refreshed {COPY_MAP_PATH.relative_to(ROOT).as_posix()}.")
    print(f"Refreshed {MARKET_REPORT_PATH.relative_to(ROOT).as_posix()}.")
    return 0


def validate() -> int:
    manifest = load_json(MANIFEST_PATH)
    errors: list[str] = []
    seen_identity: set[tuple[str, str, str]] = set()
    seen_paths: set[str] = set()
    seen_android: set[tuple[str, str]] = set()
    bilingual: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}

    if manifest.get("schema_version") != 1:
        errors.append("manifest schema_version must be 1")
    if manifest.get("operator") != {
        "legal_name": "Jesus Afkerian",
        "publishing_name": "Jesus Afkerian",
        "contact": "afkerian.support@gmail.com",
    }:
        errors.append("manifest operator identity must identify only Jesus Afkerian")
    if len(manifest.get("documents", [])) != 38:
        errors.append(
            f"manifest expected 38 canonical TXT documents, "
            f"found {len(manifest.get('documents', []))}"
        )

    for entry in manifest.get("documents", []):
        identity = (entry["product_id"], entry["document_id"], entry["language"])
        if identity in seen_identity:
            errors.append(f"duplicate document identity: {identity}")
        seen_identity.add(identity)

        canonical = entry["canonical_path"]
        if canonical in seen_paths:
            errors.append(f"duplicate canonical path: {canonical}")
        seen_paths.add(canonical)

        try:
            path = safe_repo_path(canonical)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not path.is_file():
            errors.append(f"missing canonical file: {canonical}")
            continue

        try:
            current = hashes(path)
        except (UnicodeDecodeError, OSError) as exc:
            errors.append(f"cannot hash/decode {canonical}: {exc}")
            continue
        for key in ("size_bytes", "sha256", "normalized_sha256"):
            if entry.get(key) != current[key]:
                errors.append(
                    f"stale manifest {key} for {canonical}: "
                    f"manifest={entry.get(key)!r}, actual={current[key]!r}"
                )

        if entry.get("protected_upstream"):
            if entry.get("category") != "license":
                errors.append(f"only authentic license text may be protected upstream: {canonical}")
            expected = entry.get("protected_expected_sha256")
            if not expected or current["sha256"] != expected:
                errors.append(f"protected upstream baseline mismatch: {canonical}")

        destination = entry.get("android_destination")
        repository = entry.get("android_repository")
        if destination:
            if PurePosixPath(destination).is_absolute() or ".." in PurePosixPath(destination).parts:
                errors.append(f"unsafe Android destination: {destination}")
            key = (repository, destination)
            if key in seen_android:
                errors.append(f"duplicate Android destination: {key}")
            seen_android.add(key)

        if entry.get("first_party"):
            for key in ("version", "effective_date", "last_updated"):
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(entry.get(key) or "")):
                    errors.append(f"{canonical}: {key} must be YYYY-MM-DD")
            try:
                content = text_for(entry)
            except UnicodeDecodeError as exc:
                errors.append(f"{canonical}: invalid UTF-8: {exc}")
                continue
            language = entry["language"]
            lines = content.replace("\r\n", "\n").replace("\r", "\n").splitlines()
            if len(lines) < 7:
                errors.append(f"{canonical}: incomplete first-party presentation header")
                continue
            if not lines[0].strip() or not lines[1].strip():
                errors.append(f"{canonical}: title and product name must be the first two lines")
            if lines[2].strip() or lines[5].strip():
                errors.append(f"{canonical}: presentation header spacing is not canonical")
            forbidden_metadata = re.compile(
                r"(?mi)^(?:Product|Producto|Document ID|ID del documento|"
                r"Language|Idioma|Version|Versión|Operator|Operador|Contact|Contacto):"
            )
            if forbidden_metadata.search(content):
                errors.append(f"{canonical}: technical body metadata is prohibited")
            declared_updated = metadata_value(
                content, language, "Last Updated", "Última actualización"
            )
            # The OWNER-approved privacy policies label the effective date
            # "Fecha de entrada en vigor" in Spanish; all other ES documents keep
            # the "Fecha efectiva" label.
            es_effective_key = (
                "Fecha de entrada en vigor"
                if entry["document_id"] == "PRIVACY_POLICY" or (entry["document_id"] == "TERMS_OF_SERVICE" and entry["product_id"] == "tap-odyssey")
                else "Fecha efectiva"
            )
            declared_effective = metadata_value(
                content, language, "Effective Date", es_effective_key
            )
            expected_effective = DISPLAY_DATES.get(entry["effective_date"], {}).get(language)
            if declared_effective != expected_effective:
                errors.append(f"{canonical}: effective-date presentation mismatch")
            expected_updated = DISPLAY_DATES.get(entry["last_updated"], {}).get(language)
            if declared_updated != expected_updated:
                errors.append(f"{canonical}: last-updated presentation mismatch")
            if BANNED_PUBLIC_IDENTITIES.search(content):
                errors.append(f"{canonical}: legacy public identity in first-party text")
            if OPERATOR_BRAND.search(content):
                formulas = OPERATOR_BRAND_FORMULAS.get(language, ())
                if not any(formula in content for formula in formulas):
                    errors.append(
                        f"{canonical}: AFKERIAN INTERACTIVE used without the verbatim "
                        f"operator formula naming Jesus Afkerian"
                    )
            if entry["product_id"] in {
                "xo-arcade",
                "air-strike-arcade",
                "tap-odyssey",
            }:
                # "App Set ID" is Google's proper identifier name; "App Open" is a
                # Google ad-format name. Neither is a product term, so strip both
                # before enforcing Game/Juego over a bare "App".
                product_term_scan = content.replace("App Open", "").replace("App Set ID", "")
                if re.search(r"\b(?:App|APP)\b", product_term_scan):
                    errors.append(f"{canonical}: product term must be Game/Juego, not App")
            if entry["product_id"] in {
                "xo-arcade",
                "air-strike-arcade",
                "tap-odyssey",
            }:
                # Privacy policies follow the OWNER-approved base text verbatim.
                if entry["document_id"] == "PRIVACY_POLICY":
                    if language == "en-US":
                        identity_sentence = (
                            "This Privacy Policy explains how Jesus Afkerian, a natural "
                            "person operating under the AFKERIAN INTERACTIVE brand"
                        )
                        if identity_sentence not in content:
                            errors.append(f"{canonical}: missing exact Privacy identity opening")
                        if not (("is offered without a purchase price and is funded through advertising." in content and
                                 "AFKERIAN INTERACTIVE may receive advertising revenue through Google AdMob." in content) or
                                ("is funded wholly or partly through advertising." in content and
                                 "Jesus Afkerian may receive advertising revenue under the AFKERIAN INTERACTIVE brand through Google AdMob." in content)):
                            errors.append(f"{canonical}: missing approved monetization text")
                    if language == "es-419":
                        identity_sentence = (
                            "Esta Política de Privacidad explica cómo Jesus Afkerian, "
                            "persona física que opera bajo la marca AFKERIAN INTERACTIVE"
                        )
                        if identity_sentence not in content:
                            errors.append(f"{canonical}: falta apertura de identidad de Privacidad")
                        if not (("se ofrece sin precio de compra y se financia mediante publicidad." in content and
                                 "AFKERIAN INTERACTIVE puede recibir ingresos publicitarios mediante Google AdMob." in content) or
                                ("se financia total o parcialmente mediante publicidad." in content and
                                 "Jesus Afkerian puede recibir ingresos publicitarios bajo la marca AFKERIAN INTERACTIVE mediante Google AdMob." in content)):
                            errors.append(f"{canonical}: falta declaración de monetización")
                # Terms of Service keep their existing first-person identity and
                # monetization wording (out of scope for this change).
                if entry["document_id"] == "TERMS_OF_SERVICE":
                    if language == "en-US":
                        if entry["product_id"] == "tap-odyssey":
                            identity_sentence = (
                                "These Terms form an agreement between the user and Jesus "
                                "Afkerian, an individual who operates and publishes the Game"
                            )
                        else:
                            identity_sentence = (
                                "These Terms of Service are an agreement between you and Jesus "
                                "Afkerian, an individual who publishes and operates the Game."
                            )
                        if identity_sentence not in content:
                            errors.append(f"{canonical}: missing exact Terms identity opening")
                        if entry["product_id"] == "tap-odyssey":
                            monetization = (
                                "Tap Odyssey is funded in whole or in part by advertising"
                            )
                        else:
                            monetization = (
                                "The Game is currently offered without a purchase price and is "
                                "supported by advertising. Jesus Afkerian may receive advertising "
                                "revenue through Google AdMob. Advertising revenue is not an amount "
                                "paid by the user."
                            )
                        if monetization not in content:
                            errors.append(f"{canonical}: missing exact monetization statement")
                    if language == "es-419":
                        if entry["product_id"] == "tap-odyssey":
                            monetization = (
                                "Tap Odyssey se financia total o parcialmente mediante publicidad"
                            )
                        else:
                            monetization = (
                                "El Juego se ofrece actualmente sin precio de compra y se financia "
                                "mediante publicidad. Jesus Afkerian puede recibir ingresos "
                                "publicitarios a través de Google AdMob. Los ingresos publicitarios "
                                "no son una cantidad pagada por el usuario."
                            )
                        if monetization not in content:
                            errors.append(f"{canonical}: falta declaración de monetización")
                if language == "en-US" and entry["document_id"] == "TERMS_OF_SERVICE":
                    assent = (
                        "Publication alone, silence, inaction, or keeping the Game installed "
                        "does not constitute acceptance of updated Terms. Continued access or "
                        "use after reasonably conspicuous notice and the stated effective date "
                        "is the conduct relied upon as assent, to the maximum extent permitted "
                        "by law."
                    )
                    assent_new = (
                        "To the maximum extent permitted by law, accessing or using the Game "
                        "after the notice and effective date manifests acceptance of the updated Terms."
                    )
                    if assent not in content and assent_new not in content:
                        errors.append(f"{canonical}: missing exact updated-Terms assent language")

            if entry.get("requires_bilingual"):
                bilingual.setdefault(
                    (entry["product_id"], entry["document_id"]), {}
                )[language] = entry

        route = entry.get("html_route")
        if route:
            try:
                route_path = safe_repo_path(route)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if not route_path.is_file():
                errors.append(f"missing HTML route: {route}")
            else:
                html = route_path.read_text(encoding="utf-8")
                source = route_expected_source(entry)
                if f'data-legal-src="{source}"' not in html:
                    errors.append(f"{route}: loader source does not map to {canonical}")
                if not re.search(
                    rf'id="raw-document-link"\s+href="{re.escape(source)}"', html
                ):
                    errors.append(f"{route}: raw TXT link does not map to {canonical}")
                if '<article id="legal-document" class="legal-document" tabindex="0"></article>' not in html:
                    errors.append(f"{route}: legal body host must be an empty article")
                if re.search(r'<pre\b[^>]*id="legal-document"', html, flags=re.I):
                    errors.append(f"{route}: first-party viewer must not use a pre body host")
                if ">Plain-text version</a>" not in html and ">Versión de texto</a>" not in html:
                    errors.append(f"{route}: missing plain-text version label")
                canonical_url = (
                    "https://afkerianinteractive.github.io/" + route
                )
                if f'rel="canonical" href="{canonical_url}"' not in html:
                    errors.append(f"{route}: canonical URL mismatch")

        for alias in entry.get("aliases", []):
            try:
                alias_path = safe_repo_path(alias)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if not alias_path.is_file():
                errors.append(f"missing alias route: {alias}")
                continue
            html = alias_path.read_text(encoding="utf-8")
            source = posixpath.relpath(
                canonical, start=str(PurePosixPath(alias).parent)
            )
            if f'data-legal-src="{source}"' not in html:
                errors.append(f"{alias}: alias does not render canonical TXT")
            expected_url = (
                "https://afkerianinteractive.github.io/" + entry["html_route"]
            )
            if f'rel="canonical" href="{expected_url}"' not in html:
                errors.append(f"{alias}: compatibility canonical mismatch")

    for key, languages in bilingual.items():
        if set(languages) != {"en-US", "es-419"}:
            errors.append(f"missing bilingual counterpart for {key}: {sorted(languages)}")
            continue
        en = languages["en-US"]
        es = languages["es-419"]
        if (en["version"], en["effective_date"]) != (
            es["version"],
            es["effective_date"],
        ):
            errors.append(f"bilingual version/date mismatch for {key}")
        sections_en = re.findall(r"(?m)^(\d+)\.\s", text_for(en))
        sections_es = re.findall(r"(?m)^(\d+)\.\s", text_for(es))
        if sections_en != sections_es:
            errors.append(
                f"bilingual section parity mismatch for {key}: "
                f"en={sections_en}, es={sections_es}"
            )

    tracked = set(seen_paths)
    actual: set[str] = set()
    for legal_dir in [ROOT / "legal"] + [
        ROOT / name / "legal"
        for name in ("xo-arcade", "air-strike-arcade", "tap-odyssey")
    ]:
        if legal_dir.is_dir():
            for path in legal_dir.glob("*.txt"):
                actual.add(path.relative_to(ROOT).as_posix())
    for path in sorted(actual - tracked):
        errors.append(f"untracked canonical TXT: {path}")
    for path in sorted(tracked - actual):
        errors.append(f"manifest points to absent TXT: {path}")

    canonical_routes = [
        entry["html_route"]
        for entry in manifest["documents"]
        if entry.get("html_route")
    ]
    alias_routes = [
        alias
        for entry in manifest["documents"]
        for alias in entry.get("aliases", [])
    ]
    if len(canonical_routes) != 36 or len(alias_routes) != 3:
        errors.append(
            "legal route inventory must contain 36 canonical routes and 3 aliases "
            f"(found {len(canonical_routes)} and {len(alias_routes)})"
        )

    copy_map = copy_map_value(manifest)
    if copy_map["requested_copy_count"] != 15:
        errors.append(
            "requested Android copy set must contain the nine main TXT and six named "
            f"notices (found {copy_map['requested_copy_count']})"
        )
    if copy_map["additional_consistency_copy_count"] != 5:
        errors.append(
            "evidence-required consistency copy set must contain three AdMob and two "
            f"Pixabay notices (found {copy_map['additional_consistency_copy_count']})"
        )
    if copy_map["total_copy_count"] != 20:
        errors.append(
            f"complete Android copy set must contain 20 entries, found {copy_map['total_copy_count']}"
        )
    if not COPY_MAP_PATH.is_file():
        errors.append("missing legal/android-copy-map.json")
    else:
        try:
            stored_copy_map = load_json(COPY_MAP_PATH)
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"cannot read legal/android-copy-map.json: {exc}")
        else:
            if stored_copy_map != copy_map:
                errors.append("stale legal/android-copy-map.json")

    duplicate_names = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and re.search(r"\(\d+\)", path.name)
    ]
    for path in duplicate_names:
        errors.append(f"duplicate-style filename: {path}")

    if not MARKET_PATH.is_file():
        errors.append("missing legal/market-review.json")
    else:
        market = load_json(MARKET_PATH)
        rows = market.get("markets", [])
        if market.get("schema_version") != 1:
            errors.append("market-review schema_version must be 1")
        if len(rows) != 42:
            errors.append(f"market-review expected 42 rows, found {len(rows)}")
        names = [row.get("market") for row in rows]
        if len(names) != len(set(names)):
            errors.append("market-review contains duplicate market names")
        for row in rows:
            missing = [
                key
                for key in ("market", "languages", "status", "permitted", "gate", "official_sources")
                if key not in row
            ]
            if missing:
                errors.append(f"market-review row {row.get('market')!r} missing {missing}")
            if row.get("status") not in ALLOWED_MARKET_STATUSES:
                errors.append(
                    f"market-review row {row.get('market')!r} has invalid status {row.get('status')!r}"
                )
            if row.get("permitted") and row.get("status") not in {
                "APPROVED_FOR_OWNER_ENABLEMENT",
                "DOCUMENT_READY_CONSOLE_UNVERIFIED",
            }:
                errors.append(
                    f"market-review row {row.get('market')!r} is permitted with blocking status"
                )
            for source in row.get("official_sources", []):
                if not isinstance(source, str) or not source.startswith("https://"):
                    errors.append(
                        f"market-review row {row.get('market')!r} has invalid official source"
                    )
        permitted = [row["market"] for row in market.get("markets", []) if row.get("permitted")]
        if permitted != ["United States (50 states and District of Columbia)"]:
            errors.append(f"public permitted market set is not exact: {permitted}")
        expected_report = market_report_text(market)
        if not MARKET_REPORT_PATH.is_file():
            errors.append("missing generated legal/MARKET_REVIEW.md")
        elif MARKET_REPORT_PATH.read_text(encoding="utf-8") != expected_report:
            errors.append("stale generated legal/MARKET_REVIEW.md")

    for territory_name in ("PERMITTED_TERRITORY.txt", "PERMITTED_TERRITORY_ES.txt"):
        territory = (ROOT / "legal" / territory_name).read_text(encoding="utf-8")
        bullet_count = len(re.findall(r"(?m)^- ", territory.split("Excluded")[0].split("Quedan fuera")[0]))
        if bullet_count != 51:
            errors.append(f"{territory_name}: expected 51 permitted subjurisdictions, found {bullet_count}")

    for entry in manifest["documents"]:
        if entry["document_id"] == "TERMS_OF_SERVICE":
            content = text_for(entry)
            expected = (
                "PERMITTED_TERRITORY_ES.txt"
                if entry["language"] == "es-419"
                else "PERMITTED_TERRITORY.txt"
            )
            if expected not in content:
                errors.append(f"{entry['canonical_path']}: missing canonical market-list reference")

    forbidden_patterns = {
        "legacy under-13 rule": r"(?i)under\s+13|13\s+years\s+old",
        "legacy guardian permission": r"(?i)permission\s+from\s+(?:a\s+)?parent|parent\s+or\s+legal\s+guardian",
        "false offline absolute": r"(?i)(?<!not\s)completely\s+offline|nothing\s+leaves\s+the\s+device",
        "false no-data absolute": r"(?i)we\s+(?:do\s+not|don['’]t)\s+collect\s+(?:any\s+)?data|no\s+data\s+is\s+collected",
        "false ad-free absolute": r"(?i)completely\s+ad[- ]free",
        "false entity suffix": (
            r"(?i)AFKERIAN\s+INTERACTIVE\s+"
            r"(?:LLC|INC\.?|CORP\.?|CORPORATION|COMPANY|CO\.|LTD\.?|LP|LLP|PARTNERSHIP"
            r"|S\.?A\.?|S\.?L\.?|GMBH|B\.?V\.?)"
        ),
        "false AFKERIAN INTERACTIVE registration claim": (
            r"(?i)AFKERIAN\s+INTERACTIVE[^.\n]{0,80}?"
            r"(?:registered\s+(?:DBA|trade\s+name|trademark|company|entity)"
            r"|DBA\s+registrad[oa]|nombre\s+comercial\s+registrado"
            r"|marca\s+registrada|entidad\s+(?:jurídica|legal)\s+separada"
            r"|separate\s+legal\s+entity)"
        ),
    }
    scan_paths = []
    for base in [ROOT, ROOT / "xo-arcade", ROOT / "air-strike-arcade", ROOT / "tap-odyssey"]:
        if base == ROOT:
            scan_paths.extend(ROOT.glob("*.html"))
            scan_paths.extend((ROOT / "legal").glob("*.txt"))
        else:
            scan_paths.extend(base.glob("*.html"))
            scan_paths.extend((base / "legal").glob("*.txt"))
    # The OWNER-approved policies carry a specific children's-privacy clause that
    # legitimately references "under 13 years of age" (an actual-knowledge / COPPA
    # style statement, not a legacy age gate). Allow that exact phrasing only.
    allowed_under_13_context = "under 13 years of age"
    for path in scan_paths:
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        for label, pattern in forbidden_patterns.items():
            probe = content
            if label == "legacy under-13 rule":
                probe = content.replace(allowed_under_13_context, "")
            if re.search(pattern, probe):
                errors.append(f"{path.relative_to(ROOT).as_posix()}: {label}")
        if path.suffix.lower() == ".html" and LEGACY_PUBLIC_IDENTITIES.search(content):
            errors.append(
                f"{path.relative_to(ROOT).as_posix()}: legacy public identity in HTML"
            )

    home_html = (ROOT / "index.html").read_text(encoding="utf-8")
    json_ld_blocks = re.findall(
        r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>',
        home_html,
        flags=re.I | re.S,
    )
    if len(json_ld_blocks) != 1:
        errors.append(f"index.html must expose exactly one JSON-LD block, found {len(json_ld_blocks)}")
    else:
        try:
            json_ld = json.loads(json_ld_blocks[0])
        except json.JSONDecodeError as exc:
            errors.append(f"index.html JSON-LD is invalid: {exc}")
        else:
            if json_ld.get("@type") != "Person" or json_ld.get("name") != "Jesus Afkerian":
                errors.append("index.html JSON-LD must identify Jesus Afkerian as Person")
            if "alternateName" in json_ld:
                errors.append("index.html JSON-LD must not expose a commercial alternate name")
    if re.search(r'"@type"\s*:\s*"Organization"', home_html):
        errors.append("index.html must not expose Organization JSON-LD")

    if QR_BASELINE_PATH.is_file():
        baseline = load_json(QR_BASELINE_PATH)
        expected_files = baseline.get("files", {})
        actual_files = {}
        for path in sorted((ROOT / "qr-decoder").rglob("*")):
            if path.is_file():
                actual_files[path.relative_to(ROOT).as_posix()] = hashlib.sha256(
                    path.read_bytes()
                ).hexdigest().upper()
        if expected_files != actual_files:
            missing = sorted(set(expected_files) - set(actual_files))
            added = sorted(set(actual_files) - set(expected_files))
            changed = sorted(
                key for key in set(expected_files) & set(actual_files)
                if expected_files[key] != actual_files[key]
            )
            errors.append(
                f"QR regression baseline mismatch: missing={missing}, added={added}, changed={changed}"
            )
    else:
        errors.append("missing QR regression baseline")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(
        f"Validation passed: {len(manifest['documents'])} canonical TXT documents, "
        f"{len(seen_identity)} unique identities, "
        f"{len(canonical_routes) + len(alias_routes)} legal routes."
    )
    return 0


def compare(product: str, android_root: Path) -> int:
    manifest = load_json(MANIFEST_PATH)
    entries = [d for d in manifest["documents"] if d["product_id"] == product]
    if not entries:
        print(f"Unknown product: {product}", file=sys.stderr)
        return 2
    android_root = android_root.resolve()
    results = []
    differences = False
    for entry in entries:
        web_path = safe_repo_path(entry["canonical_path"])
        destination = entry.get("android_destination")
        result = {
            "document_id": entry["document_id"],
            "language": entry["language"],
            "website": entry["canonical_path"],
            "android_destination": destination or "UNVERIFIED",
            "status": None,
        }
        if not destination:
            result["status"] = "UNMAPPED"
            differences = True
        else:
            android_path = (android_root / Path(*PurePosixPath(destination).parts)).resolve()
            try:
                android_path.relative_to(android_root)
            except ValueError:
                result["status"] = "UNSAFE_ANDROID_DESTINATION"
                differences = True
            else:
                if not android_path.is_file():
                    result["status"] = "MISSING_ANDROID"
                    differences = True
                else:
                    web_raw = web_path.read_bytes()
                    android_raw = android_path.read_bytes()
                    result["website_sha256"] = hashlib.sha256(web_raw).hexdigest().upper()
                    result["android_sha256"] = hashlib.sha256(android_raw).hexdigest().upper()
                    if web_raw == android_raw:
                        result["status"] = "BYTE_EQUAL"
                    elif normalized_bytes(web_raw) == normalized_bytes(android_raw):
                        result["status"] = "NORMALIZED_EQUAL"
                        differences = True
                    else:
                        result["status"] = "SUBSTANTIVE_DIFFERENCE"
                        differences = True
        results.append(result)

    print(json.dumps({"product": product, "android_root": str(android_root), "results": results}, indent=2))
    return 1 if differences else 0


def snapshot_qr() -> int:
    files = {}
    for path in sorted((ROOT / "qr-decoder").rglob("*")):
        if path.is_file():
            files[path.relative_to(ROOT).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest().upper()
    write_json(
        QR_BASELINE_PATH,
        {
            "schema_version": 1,
            "captured_on": "2026-07-22",
            "purpose": "Regression guard only; QR Decoder legal content is outside this migration scope.",
            "files": files,
        },
    )
    print(f"Captured {len(files)} QR Decoder files.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("refresh")
    sub.add_parser("validate")
    compare_parser = sub.add_parser("compare")
    compare_parser.add_argument("--product", required=True)
    compare_parser.add_argument("--android-root", type=Path, required=True)
    sub.add_parser("snapshot-qr")
    args = parser.parse_args()
    if args.command == "refresh":
        return refresh()
    if args.command == "validate":
        return validate()
    if args.command == "compare":
        return compare(args.product, args.android_root)
    if args.command == "snapshot-qr":
        return snapshot_qr()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

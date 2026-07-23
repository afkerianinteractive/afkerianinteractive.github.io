#!/usr/bin/env python3
"""Validate and compare AFKERIAN INTERACTIVE canonical legal TXT files.

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


def refresh() -> int:
    manifest = load_json(MANIFEST_PATH)
    failures: list[str] = []
    for entry in manifest["documents"]:
        try:
            path = safe_repo_path(entry["canonical_path"])
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
    market = load_json(MARKET_PATH)
    MARKET_REPORT_PATH.write_text(
        market_report_text(market), encoding="utf-8", newline="\n"
    )
    print(f"Refreshed {len(manifest['documents'])} manifest entries.")
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
            declared_language = metadata_value(content, language, "Language", "Idioma")
            declared_version = metadata_value(content, language, "Version", "Versión")
            declared_effective = metadata_value(
                content, language, "Effective date", "Fecha de entrada en vigor"
            )
            declared_updated = metadata_value(
                content, language, "Last updated", "Última actualización"
            )
            expected_language = language
            if declared_language != expected_language:
                errors.append(
                    f"{canonical}: declared language {declared_language!r}, "
                    f"expected {expected_language!r}"
                )
            if declared_version != entry["version"]:
                errors.append(f"{canonical}: version metadata mismatch")
            if declared_effective != entry["effective_date"]:
                errors.append(f"{canonical}: effective-date metadata mismatch")
            if declared_updated != entry["last_updated"]:
                errors.append(f"{canonical}: last-updated metadata mismatch")

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
                for pre_body in re.findall(
                    r"<pre\b[^>]*>(.*?)</pre>", html, flags=re.I | re.S
                ):
                    if pre_body.strip():
                        errors.append(f"{route}: independently maintained legal body in HTML")
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
        "false entity suffix": r"(?i)AFKERIAN\s+INTERACTIVE\s+(?:LLC|INC\.?|CORPORATION|LTD\.?)",
    }
    scan_paths = []
    for base in [ROOT, ROOT / "xo-arcade", ROOT / "air-strike-arcade", ROOT / "tap-odyssey"]:
        if base == ROOT:
            scan_paths.extend(ROOT.glob("*.html"))
            scan_paths.extend((ROOT / "legal").glob("*.txt"))
        else:
            scan_paths.extend(base.glob("*.html"))
            scan_paths.extend((base / "legal").glob("*.txt"))
    for path in scan_paths:
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        for label, pattern in forbidden_patterns.items():
            if re.search(pattern, content):
                errors.append(f"{path.relative_to(ROOT).as_posix()}: {label}")

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
        f"{len(seen_identity)} unique identities."
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

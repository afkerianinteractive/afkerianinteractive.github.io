#!/usr/bin/env python3
"""Build a read-only dependency and license evidence report for the three games.

Gradle project state is redirected to a temporary directory. The script reads the
resolved release graph and the local Gradle artifact cache; it does not edit any
Android repository. It intentionally marks missing or ambiguous license metadata
as UNVERIFIED instead of inferring a license from a Maven group name.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import urllib.error
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "legal" / "dependency-license-bom.json"
GRADLE_CACHE = Path.home() / ".gradle" / "caches" / "modules-2" / "files-2.1"
APPS = {
    "xo-arcade": Path.home() / "AndroidStudioProjects" / "XOArcade",
    "air-strike-arcade": Path.home() / "AndroidStudioProjects" / "AirStrikeArcade",
    "tap-odyssey": Path.home() / "AndroidStudioProjects" / "TapOdyssey",
}
DEPENDENCY_RE = re.compile(
    r"---\s+([^:()\s]+):([^:()\s]+):([^\s()]+)(?:\s+->\s+([^\s()]+))?"
)
LEGAL_ENTRY_RE = re.compile(
    r"(?i)(?:^|/)(?:meta-inf/)?"
    r"(?:license|licence|notice|copying|copyright|dependencies)"
    r"(?:[-_.][^/]*)?$"
)
OFFICIAL_PROJECT_LICENSES = {
    # These coordinates map to source directories present in the official
    # firebase/firebase-android-sdk repository. That repository expressly excludes
    # Analytics and Auth, so no override is applied to firebase-analytics or the
    # closed measurement connector.
    "com.google.firebase:firebase-annotations": {
        "classification": "APACHE-2.0",
        "license_url": "https://github.com/firebase/firebase-android-sdk/blob/main/LICENSE",
        "source_url": "https://github.com/firebase/firebase-android-sdk/tree/main/firebase-annotations",
    },
    "com.google.firebase:firebase-common": {
        "classification": "APACHE-2.0",
        "license_url": "https://github.com/firebase/firebase-android-sdk/blob/main/LICENSE",
        "source_url": "https://github.com/firebase/firebase-android-sdk/tree/main/firebase-common",
    },
    "com.google.firebase:firebase-components": {
        "classification": "APACHE-2.0",
        "license_url": "https://github.com/firebase/firebase-android-sdk/blob/main/LICENSE",
        "source_url": "https://github.com/firebase/firebase-android-sdk/tree/main/firebase-components",
    },
    "com.google.firebase:firebase-config-interop": {
        "classification": "APACHE-2.0",
        "license_url": "https://github.com/firebase/firebase-android-sdk/blob/main/LICENSE",
        "source_url": "https://github.com/firebase/firebase-android-sdk/tree/main/firebase-config-interop",
    },
    "com.google.firebase:firebase-datatransport": {
        "classification": "APACHE-2.0",
        "license_url": "https://github.com/firebase/firebase-android-sdk/blob/main/LICENSE",
        "source_url": "https://github.com/firebase/firebase-android-sdk/tree/main/firebase-datatransport",
    },
    "com.google.firebase:firebase-encoders": {
        "classification": "APACHE-2.0",
        "license_url": "https://github.com/firebase/firebase-android-sdk/blob/main/LICENSE",
        "source_url": "https://github.com/firebase/firebase-android-sdk/tree/main/encoders",
    },
    "com.google.firebase:firebase-encoders-json": {
        "classification": "APACHE-2.0",
        "license_url": "https://github.com/firebase/firebase-android-sdk/blob/main/LICENSE",
        "source_url": "https://github.com/firebase/firebase-android-sdk/tree/main/encoders",
    },
    "com.google.firebase:firebase-encoders-proto": {
        "classification": "APACHE-2.0",
        "license_url": "https://github.com/firebase/firebase-android-sdk/blob/main/LICENSE",
        "source_url": "https://github.com/firebase/firebase-android-sdk/tree/main/encoders",
    },
    "com.google.firebase:firebase-installations-interop": {
        "classification": "APACHE-2.0",
        "license_url": "https://github.com/firebase/firebase-android-sdk/blob/main/LICENSE",
        "source_url": "https://github.com/firebase/firebase-android-sdk/tree/main/firebase-installations-interop",
    },
    "com.google.guava:failureaccess": {
        "classification": "APACHE-2.0",
        "license_url": "https://github.com/google/guava/blob/master/LICENSE",
        "source_url": "https://github.com/google/guava/tree/master/futures/failureaccess",
    },
    "com.google.guava:guava": {
        "classification": "APACHE-2.0",
        "license_url": "https://github.com/google/guava/blob/master/LICENSE",
        "source_url": "https://github.com/google/guava",
    },
    "com.google.guava:listenablefuture": {
        "classification": "APACHE-2.0",
        "license_url": "https://github.com/google/guava/blob/master/LICENSE",
        "source_url": "https://github.com/google/guava/tree/master/futures/listenablefuture",
    },
    # Firebase's setup documentation identifies firebase-analytics as an official
    # supported SDK and the Firebase open-source repository expressly excludes
    # Analytics. Treat these two closed artifacts as governed service software,
    # not as Apache-licensed Firebase source.
    "com.google.firebase:firebase-analytics": {
        "classification": "GOOGLE_MOBILE_DEVELOPER_TERMS",
        "license_url": "https://developers.google.com/mobile/terms",
        "source_url": "https://firebase.google.com/docs/android/setup#available-libraries",
    },
    "com.google.firebase:firebase-measurement-connector": {
        "classification": "GOOGLE_MOBILE_DEVELOPER_TERMS",
        "license_url": "https://developers.google.com/mobile/terms",
        "source_url": "https://firebase.google.com/docs/analytics",
    },
}


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest().upper()


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def child_text(element: ElementTree.Element | None, name: str) -> str | None:
    if element is None:
        return None
    for child in element:
        if local_name(child.tag) == name and child.text:
            value = child.text.strip()
            return value or None
    return None


def children(element: ElementTree.Element, name: str) -> list[ElementTree.Element]:
    return [child for child in element if local_name(child.tag) == name]


def first_child(
    element: ElementTree.Element, name: str
) -> ElementTree.Element | None:
    return next((child for child in element if local_name(child.tag) == name), None)


def normalize_license(name: str, url: str) -> str:
    value = f"{name} {url}".lower()
    if "android software development kit license" in value:
        return "ANDROID_SDK_LICENSE"
    if "apache" in value and ("2.0" in value or "2" in value):
        return "APACHE-2.0"
    if "bsd" in value and "3" in value:
        return "BSD-3-CLAUSE"
    if "mit" in value:
        return "MIT"
    if "eclipse public license" in value and "2" in value:
        return "EPL-2.0"
    if "classpath" in value and ("gpl" in value or "general public" in value):
        return "GPL-2.0-WITH-CLASSPATH-EXCEPTION"
    if "cddl" in value:
        return "CDDL-OR-COMPOSITE"
    return "UNCLASSIFIED"


def infer_license_from_bytes(raw: bytes) -> str:
    text = raw[:262144].decode("utf-8", errors="ignore").lower()
    if "apache license" in text and "version 2.0" in text:
        return "APACHE-2.0"
    if "redistribution and use in source and binary forms" in text and (
        "neither the name" in text or "contributors may be used to endorse" in text
    ):
        return "BSD-3-CLAUSE"
    if "permission is hereby granted, free of charge" in text:
        return "MIT"
    if "eclipse public license - v 2.0" in text:
        return "EPL-2.0"
    if "gnu general public license" in text and "classpath exception" in text:
        return "GPL-2.0-WITH-CLASSPATH-EXCEPTION"
    if "android software development kit license agreement" in text:
        return "ANDROID_SDK_LICENSE"
    return "UNCLASSIFIED"


def pom_evidence_bytes(raw: bytes, source: str) -> dict[str, Any]:
    try:
        root = ElementTree.fromstring(raw)
    except ElementTree.ParseError:
        return {
            "status": "UNREADABLE",
            "source": source,
            "licenses": [],
            "project_url": None,
            "owner": None,
        }

    licenses: list[dict[str, str]] = []
    license_parent = first_child(root, "licenses")
    if license_parent is not None:
        for license_element in children(license_parent, "license"):
            name = child_text(license_element, "name") or ""
            url = child_text(license_element, "url") or ""
            licenses.append(
                {
                    "name": name,
                    "url": url,
                    "classification": normalize_license(name, url),
                }
            )

    organization = first_child(root, "organization")
    owner = child_text(organization, "name")
    if not owner:
        developer_parent = first_child(root, "developers")
        developer = (
            first_child(developer_parent, "developer")
            if developer_parent is not None
            else None
        )
        owner = child_text(developer, "organization") or child_text(developer, "name")

    return {
        "status": "READ",
        "source": source,
        "licenses": licenses,
        "project_url": child_text(root, "url"),
        "owner": owner,
    }


def pom_evidence(path: Path) -> dict[str, Any]:
    try:
        return pom_evidence_bytes(path.read_bytes(), "LOCAL_GRADLE_CACHE")
    except OSError:
        return {
            "status": "UNREADABLE",
            "source": "LOCAL_GRADLE_CACHE",
            "licenses": [],
            "project_url": None,
            "owner": None,
        }


def official_pom_urls(group: str, artifact: str, version: str) -> list[str]:
    relative = "/".join(
        [group.replace(".", "/"), artifact, version, f"{artifact}-{version}.pom"]
    )
    google_prefixes = (
        "androidx.",
        "com.android.",
        "com.google.android.",
        "com.google.firebase.",
    )
    if group.startswith(google_prefixes):
        return [
            f"https://dl.google.com/dl/android/maven2/{relative}",
            f"https://repo.maven.apache.org/maven2/{relative}",
        ]
    return [f"https://repo.maven.apache.org/maven2/{relative}"]


def remote_pom_evidence(group: str, artifact: str, version: str) -> dict[str, Any]:
    attempted: list[str] = []
    for url in official_pom_urls(group, artifact, version):
        attempted.append(url)
        try:
            request = urllib.request.Request(
                url, headers={"User-Agent": "Jesus-Afkerian-License-Audit/1.0"}
            )
            with urllib.request.urlopen(request, timeout=15) as response:
                raw = response.read(2_097_153)
                if len(raw) > 2_097_152:
                    continue
        except (OSError, urllib.error.URLError):
            continue
        evidence = pom_evidence_bytes(raw, url)
        evidence["attempted_sources"] = attempted
        return evidence
    return {
        "status": "UNAVAILABLE",
        "source": None,
        "attempted_sources": attempted,
        "licenses": [],
        "project_url": None,
        "owner": None,
    }


def archive_evidence(path: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    try:
        with zipfile.ZipFile(path) as archive:
            for name in sorted(archive.namelist(), key=str.lower):
                normalized = name.replace("\\", "/")
                if normalized.endswith("/") or not LEGAL_ENTRY_RE.search(normalized):
                    continue
                info = archive.getinfo(name)
                if info.file_size > 2_097_152:
                    results.append(
                        {
                            "entry": normalized,
                            "size_bytes": info.file_size,
                            "status": "TOO_LARGE_TO_INSPECT",
                        }
                    )
                    continue
                raw = archive.read(name)
                copyright_lines = [
                    line.strip()
                    for line in raw.decode("utf-8", errors="ignore").splitlines()
                    if re.search(r"(?i)\bcopyright\b|\(c\)|©", line)
                ][:20]
                results.append(
                    {
                        "entry": normalized,
                        "size_bytes": len(raw),
                        "sha256": sha256(raw),
                        "license_classification": infer_license_from_bytes(raw),
                        "copyright_lines": copyright_lines,
                        "status": "INSPECTED",
                    }
                )
    except (OSError, zipfile.BadZipFile):
        return [{"status": "UNREADABLE_ARCHIVE"}]
    return results


def component_evidence(
    coordinate: str, remote_pom: dict[str, Any] | None = None
) -> dict[str, Any]:
    group, artifact, version = coordinate.split(":", 2)
    base = GRADLE_CACHE / group / artifact / version
    pom_paths = sorted(base.glob("*/*.pom")) if base.is_dir() else []
    archives = sorted(
        [
            path
            for pattern in ("*/*.aar", "*/*.jar")
            for path in base.glob(pattern)
            if not re.search(r"(?i)-(sources|javadoc)\.jar$", path.name)
        ]
    )
    poms = [pom_evidence(path) for path in pom_paths]
    if not poms and remote_pom is not None:
        poms.append(remote_pom)
    archive_rows = [
        {
            "artifact_type": path.suffix.lower().lstrip("."),
            "artifact_size_bytes": path.stat().st_size,
            "artifact_sha256": sha256(path.read_bytes()),
            "legal_entries": archive_evidence(path),
        }
        for path in archives
    ]
    classifications = sorted(
        {
            license_row["classification"]
            for pom in poms
            for license_row in pom["licenses"]
            if license_row["classification"] != "UNCLASSIFIED"
        }
        | {
            legal_entry.get("license_classification", "")
            for archive in archive_rows
            for legal_entry in archive["legal_entries"]
            if legal_entry.get("license_classification")
            not in {"", "UNCLASSIFIED"}
        }
    )
    official_project_evidence = OFFICIAL_PROJECT_LICENSES.get(f"{group}:{artifact}")
    if official_project_evidence:
        classifications = sorted(
            set(classifications) | {official_project_evidence["classification"]}
        )
    distributed_artifact_count = len(archives)
    if not base.is_dir() and classifications:
        status = "LICENSE_IDENTIFIED_METADATA_ONLY"
    elif not base.is_dir():
        status = "UNVERIFIED_COMPONENT_CACHE_MISSING"
    elif not classifications:
        status = "UNVERIFIED_LICENSE_NOT_IDENTIFIED"
    elif len(classifications) > 1:
        status = "REVIEW_MULTIPLE_LICENSES"
    else:
        status = "LICENSE_IDENTIFIED"
    owner = next((pom["owner"] for pom in poms if pom.get("owner")), None)
    project_url = next(
        (pom["project_url"] for pom in poms if pom.get("project_url")), None
    )
    return {
        "coordinate": coordinate,
        "owner_from_pom": owner,
        "official_url_from_pom": project_url,
        "license_classifications": classifications,
        "pom_evidence": poms,
        "archive_evidence": archive_rows,
        "official_project_license_evidence": official_project_evidence,
        "distributed_artifact_count": distributed_artifact_count,
        "redistribution_review": status,
    }


def resolve_graph(project: Path) -> tuple[list[str], dict[str, Any]]:
    if not (project / "gradlew.bat").is_file():
        raise FileNotFoundError(f"Gradle wrapper not found: {project}")
    with tempfile.TemporaryDirectory(prefix="codex-license-audit-") as cache:
        env = os.environ.copy()
        extra = (
            "-Dorg.gradle.vfs.watch=false "
            "-Dorg.gradle.internal.problems.report=false"
        )
        env["GRADLE_OPTS"] = (env.get("GRADLE_OPTS", "") + " " + extra).strip()
        command = [
            str(project / "gradlew.bat"),
            ":app:dependencies",
            "--configuration",
            "releaseRuntimeClasspath",
            "--offline",
            "--no-daemon",
            "--console=plain",
            "--no-problems-report",
            "--project-cache-dir",
            cache,
        ]
        completed = subprocess.run(
            command,
            cwd=project,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
            check=False,
        )
    output = completed.stdout + "\n" + completed.stderr
    if completed.returncode != 0:
        tail = "\n".join(output.splitlines()[-40:])
        raise RuntimeError(f"Gradle dependency resolution failed:\n{tail}")
    coordinates: set[str] = set()
    for match in DEPENDENCY_RE.finditer(output):
        version = match.group(4) or match.group(3)
        coordinates.add(f"{match.group(1)}:{match.group(2)}:{version}")
    return sorted(coordinates), {
        "configuration": "releaseRuntimeClasspath",
        "gradle_exit_code": completed.returncode,
        "resolved_component_count": len(coordinates),
        "unresolved_marker_count": len(
            re.findall(r"(?i)could not resolve|not found|\bFAILED\b", output)
        ),
    }


def build_report() -> dict[str, Any]:
    applications = []
    overall: dict[str, dict[str, Any]] = {}
    coordinates_by_product: dict[str, list[str]] = {}
    resolutions: dict[str, dict[str, Any]] = {}
    all_coordinates: set[str] = set()
    for product, project in APPS.items():
        coordinates, resolution = resolve_graph(project)
        coordinates_by_product[product] = coordinates
        resolutions[product] = resolution
        all_coordinates.update(coordinates)

    def fetch(coordinate: str) -> tuple[str, dict[str, Any]]:
        group, artifact, version = coordinate.split(":", 2)
        return coordinate, remote_pom_evidence(group, artifact, version)

    with ThreadPoolExecutor(max_workers=16) as executor:
        remote_poms = dict(executor.map(fetch, sorted(all_coordinates)))

    for coordinate in sorted(all_coordinates):
        overall[coordinate] = component_evidence(
            coordinate, remote_pom=remote_poms[coordinate]
        )

    for product in APPS:
        applications.append(
            {
                "product_id": product,
                "resolution": resolutions[product],
                "components": coordinates_by_product[product],
            }
        )
    counts: dict[str, int] = {}
    for component in overall.values():
        status = component["redistribution_review"]
        counts[status] = counts.get(status, 0) + 1
    return {
        "schema_version": 1,
        "reviewed_on": "2026-07-23",
        "scope": "Resolved release runtime dependencies; Android repositories read-only.",
        "method": (
            "Gradle releaseRuntimeClasspath resolved offline with project state redirected "
            "to a temporary directory; local POM/AAR/JAR license and NOTICE evidence inspected."
        ),
        "applications": applications,
        "unique_components": [overall[key] for key in sorted(overall)],
        "summary": {
            "unique_component_count": len(overall),
            "redistribution_review_counts": dict(sorted(counts.items())),
            "approval_rule": (
                "Any UNVERIFIED or REVIEW_MULTIPLE_LICENSES result blocks final license approval."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    report = build_report()
    serialized = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not args.output.is_file():
            print(f"ERROR: missing {args.output}", flush=True)
            return 1
        if args.output.read_text(encoding="utf-8") != serialized:
            print(f"ERROR: stale {args.output}", flush=True)
            return 1
    else:
        args.output.write_text(serialized, encoding="utf-8", newline="\n")
    summary = report["summary"]
    print(
        json.dumps(
            {
                "applications": {
                    row["product_id"]: row["resolution"]
                    for row in report["applications"]
                },
                "summary": summary,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Validate custom integration metadata files."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "benq_infrared" / "manifest.json"
HACS = ROOT / "hacs.json"


def test_manifest_required_keys() -> None:
    """manifest.json should include keys required for HACS/custom integrations."""
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    required = {
        "domain",
        "name",
        "version",
        "documentation",
        "issue_tracker",
        "codeowners",
        "integration_type",
        "iot_class",
    }
    missing = sorted(required - set(data))
    assert not missing, f"manifest.json missing keys: {missing}"


def test_manifest_domain_matches_hacs() -> None:
    """The integration domain should match across manifest and hacs.json."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    hacs = json.loads(HACS.read_text(encoding="utf-8"))

    assert manifest["domain"] in hacs["domains"]


def test_manifest_version_is_semver_like() -> None:
    """Version should be a dotted version string."""
    version = json.loads(MANIFEST.read_text(encoding="utf-8"))["version"]
    parts = version.split(".")
    assert len(parts) >= 3
    assert all(part.isdigit() for part in parts)

"""Validate that translation/icon keys are aligned."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRINGS = ROOT / "custom_components" / "benq_infrared" / "strings.json"
ICONS = ROOT / "custom_components" / "benq_infrared" / "icons.json"


def test_button_translation_keys_match_icons() -> None:
    """Button keys in strings.json should match icons.json keys."""
    strings_data = json.loads(STRINGS.read_text(encoding="utf-8"))
    icons_data = json.loads(ICONS.read_text(encoding="utf-8"))

    string_keys = set(strings_data["entity"]["button"].keys())
    icon_keys = set(icons_data["entity"]["button"].keys())

    assert string_keys == icon_keys

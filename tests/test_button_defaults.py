"""Tests for BenQ IR button default enablement."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUTTON_FILE = ROOT / "custom_components" / "benq_infrared" / "button.py"
POWER_KEYS = {"power_on", "power_off"}


def _get_button_default_flags() -> dict[str, bool]:
    """Return mapping of button key to entity_registry_enabled_default from source."""
    module = ast.parse(BUTTON_FILE.read_text(encoding="utf-8"))

    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue

        if not any(isinstance(target, ast.Name) and target.id == "PROJECTOR_BUTTON_DESCRIPTIONS" for target in node.targets):
            continue

        descriptions = node.value
        if not isinstance(descriptions, ast.Tuple):
            continue

        results: dict[str, bool] = {}
        for item in descriptions.elts:
            if not isinstance(item, ast.Call):
                continue

            if not isinstance(item.func, ast.Name) or item.func.id != "BenQIrButtonEntityDescription":
                continue

            key: str | None = None
            enabled_default = True
            for kwarg in item.keywords:
                if kwarg.arg == "key" and isinstance(kwarg.value, ast.Constant):
                    key = str(kwarg.value.value)
                if kwarg.arg == "entity_registry_enabled_default" and isinstance(kwarg.value, ast.Constant):
                    enabled_default = bool(kwarg.value.value)

            if key is not None:
                results[key] = enabled_default

        return results

    raise AssertionError("PROJECTOR_BUTTON_DESCRIPTIONS not found in button.py")


def test_only_power_buttons_enabled_by_default() -> None:
    """Only power buttons should be enabled by default in the registry."""
    default_flags = _get_button_default_flags()
    enabled_keys = {key for key, enabled in default_flags.items() if enabled}

    assert enabled_keys == POWER_KEYS

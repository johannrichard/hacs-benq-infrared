"""Constants for the BenQ Infrared integration."""

from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from infrared_protocols.commands import Command


def _resolve_nec_command_class() -> type[Any]:
    """Return the NECCommand class across infrared_protocols versions."""
    try:
        from infrared_protocols.commands import NECCommand

        return NECCommand
    except ImportError:
        # Older layout where commands is a package with a nec module.
        from infrared_protocols.commands.nec import NECCommand

        return NECCommand

DOMAIN = "benq_infrared"

CONF_INFRARED_ENTITY_ID = "infrared_entity_id"
CONF_DEVICE_TYPE = "device_type"

# BenQ W1070 / W1080ST / W2000 series
# Protocol: NEC Extended (16-bit address, no address inversion)
# Address:  0x3000
# Carrier:  38 kHz
# Source:   github.com/Sirr-Al-Asrar/BenQ-W1070-IR-remote (raw timing decode)
BENQ_NEC_ADDRESS = 0x3000


class BenQDeviceType(str):
    """BenQ device types."""
    PROJECTOR = "projector"


class BenQProjectorCode(IntEnum):
    """BenQ projector IR command bytes (NEC Extended, address=0x3000)."""

    # ── Power ──────────────────────────────────────────────────────────────
    POWER_ON     = 0x4F
    POWER_OFF    = 0x4E
    POWER_TOGGLE = 0x02   # BenQ LK952 spec

    # ── Navigation ─────────────────────────────────────────────────────────
    MENU         = 0x0F
    UP           = 0x0B
    DOWN         = 0x0C
    LEFT         = 0x0D
    RIGHT        = 0x0E
    OK           = 0x10

    # ── Input sources ──────────────────────────────────────────────────────
    HDMI_1       = 0x58
    HDMI_2       = 0x59
    VGA          = 0x41
    COMPONENT    = 0x51
    VIDEO        = 0x52

    # ── Picture ────────────────────────────────────────────────────────────
    AUTO         = 0x08
    ECO_BLANK    = 0x07
    ASPECT_RATIO = 0x13
    BRIGHTNESS   = 0x16
    CONTRAST     = 0x11

    # ── Audio ──────────────────────────────────────────────────────────────
    MUTE         = 0x14
    VOLUME_UP    = 0x0E   # BenQ W1070: shared with RIGHT
    VOLUME_DOWN  = 0x0D   # BenQ W1070: shared with LEFT

    def to_command(self, repeat_count: int = 0) -> Command:
        """Build a NECCommand object for infrared.async_send_command."""
        NECCommand = _resolve_nec_command_class()

        return NECCommand(
            address=BENQ_NEC_ADDRESS,
            command=self.value,
            modulation=38000,
            repeat_count=repeat_count,
        )

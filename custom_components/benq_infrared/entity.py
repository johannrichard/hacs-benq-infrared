"""Common base entity for BenQ IR integration."""

from __future__ import annotations

import asyncio
import logging

from homeassistant.components.infrared import async_send_command
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_state_change_event

from .const import CONF_INFRARED_ENTITY_ID, DOMAIN, BenQProjectorCode

_LOGGER = logging.getLogger(__name__)

# The infrared entity state is a timestamp (last command sent) or "unavailable".
# "unknown" means the transmitter is reachable but has never sent a command yet —
# this is NORMAL on first boot and must NOT be treated as unavailable.
_IR_UNAVAILABLE_STATES = {"unavailable"}


def _ir_entity_available(state_str: str | None) -> bool:
    """Return True if the IR transmitter entity is usable.

    The infrared entity state is either:
      - A timestamp  → transmitter is reachable and has sent at least one command.
      - "unknown"    → transmitter is reachable but has never sent a command yet.
      - "unavailable"→ transmitter is offline / unreachable.
    """
    if state_str is None:
        return False
    return state_str not in _IR_UNAVAILABLE_STATES


class BenQIrEntity(Entity):
    """BenQ IR base entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_entity_id: str,
        unique_id_suffix: str,
    ) -> None:
        """Initialise the BenQ IR entity."""
        self._infrared_entity_id = infrared_entity_id
        self._attr_unique_id = f"{entry.entry_id}_{unique_id_suffix}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="BenQ Projector",
            manufacturer="BenQ",
        )

    async def async_added_to_hass(self) -> None:
        """Subscribe to infrared entity state changes."""
        await super().async_added_to_hass()

        @callback
        def _async_ir_state_changed(event: Event) -> None:
            """Handle infrared entity state changes."""
            new_state = event.data.get("new_state")
            if new_state is None:
                return
            available = _ir_entity_available(new_state.state)
            _LOGGER.debug(
                "IR entity %s state=%r → %s for %s",
                self._infrared_entity_id,
                new_state.state,
                "available" if available else "UNAVAILABLE",
                self.entity_id,
            )
            self._attr_available = available
            self.async_write_ha_state()

        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._infrared_entity_id], _async_ir_state_changed
            )
        )

        ir_state = self.hass.states.get(self._infrared_entity_id)
        self._attr_available = _ir_entity_available(
            ir_state.state if ir_state is not None else None
        )
        _LOGGER.debug(
            "Initial IR entity %s state=%r → %s for %s",
            self._infrared_entity_id,
            ir_state.state if ir_state else None,
            "available" if self._attr_available else "UNAVAILABLE",
            self.unique_id,
        )

    async def _send_command(self, code: BenQProjectorCode) -> None:
        """Send an IR command via the infrared platform.

        Passes a NECCommand object — NOT a raw string.
        infrared.async_send_command requires an infrared_protocols.Command
        instance with a get_raw_timings() method.
        """
        await async_send_command(
            self.hass,
            self._infrared_entity_id,
            code.to_command(),   # ← NECCommand object, not a string
            context=self._context,
        )

    async def _send_command_twice(
        self,
        code: BenQProjectorCode,
        delay_seconds: float = 0.5,
    ) -> None:
        """Send an IR command twice with a small pause between sends.

        BenQ projectors require this for power-off to consistently enter standby.
        """
        await self._send_command(code)
        await asyncio.sleep(delay_seconds)
        await self._send_command(code)

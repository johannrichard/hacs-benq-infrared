"""Media player platform for BenQ IR integration."""

from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_DEVICE_TYPE, CONF_INFRARED_ENTITY_ID, BenQProjectorCode
from .entity import BenQIrEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up BenQ IR media player from a config entry."""
    infrared_entity_id = entry.data[CONF_INFRARED_ENTITY_ID]
    device_type = entry.data[CONF_DEVICE_TYPE]

    if device_type == "projector":
        async_add_entities([BenQIrMediaPlayer(entry, infrared_entity_id)])


class BenQIrMediaPlayer(BenQIrEntity, MediaPlayerEntity):
    """BenQ IR media player entity."""

    _attr_name = None
    _attr_assumed_state = True
    _attr_device_class = MediaPlayerDeviceClass.TV

    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.VOLUME_STEP
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    _attr_source_list = ["HDMI 1", "HDMI 2", "VGA", "Component", "Video"]

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        """Initialise the media player."""
        super().__init__(entry, infrared_entity_id, unique_id_suffix="media_player")
        self._attr_state = MediaPlayerState.ON

    async def async_turn_on(self) -> None:
        """Power on the projector."""
        await self._send_command(BenQProjectorCode.POWER_ON)
        self._attr_state = MediaPlayerState.ON
        self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        """Power off the projector."""
        await self._send_command(BenQProjectorCode.POWER_OFF)
        self._attr_state = MediaPlayerState.OFF
        self.async_write_ha_state()

    async def async_volume_up(self) -> None:
        await self._send_command(BenQProjectorCode.VOLUME_UP)

    async def async_volume_down(self) -> None:
        await self._send_command(BenQProjectorCode.VOLUME_DOWN)

    async def async_mute_volume(self, mute: bool) -> None:
        await self._send_command(BenQProjectorCode.MUTE)

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        source_map: dict[str, BenQProjectorCode] = {
            "HDMI 1":    BenQProjectorCode.HDMI_1,
            "HDMI 2":    BenQProjectorCode.HDMI_2,
            "VGA":       BenQProjectorCode.VGA,
            "Component": BenQProjectorCode.COMPONENT,
            "Video":     BenQProjectorCode.VIDEO,
        }
        if code := source_map.get(source):
            await self._send_command(code)
            self._attr_source = source
            self.async_write_ha_state()

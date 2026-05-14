"""Button platform for BenQ IR integration."""

from __future__ import annotations

from dataclasses import dataclass


from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_DEVICE_TYPE, CONF_INFRARED_ENTITY_ID, BenQProjectorCode
from .entity import BenQIrEntity

PARALLEL_UPDATES = 1

PROJECTOR_BUTTON_DESCRIPTIONS: tuple["BenQIrButtonEntityDescription", ...] = ()


@dataclass(frozen=True, kw_only=True)
class BenQIrButtonEntityDescription(ButtonEntityDescription):
    """Describes a BenQ IR button entity."""

    command_code: BenQProjectorCode
    entity_registry_enabled_default: bool = True


PROJECTOR_BUTTON_DESCRIPTIONS = (
    BenQIrButtonEntityDescription(key="power_on", name="Power On", translation_key="power_on", command_code=BenQProjectorCode.POWER_ON),
    BenQIrButtonEntityDescription(key="power_off", name="Power Off", translation_key="power_off", command_code=BenQProjectorCode.POWER_OFF),
    BenQIrButtonEntityDescription(key="power_toggle", name="Power Toggle", translation_key="power_toggle", command_code=BenQProjectorCode.POWER_TOGGLE, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="menu", name="Menu", translation_key="menu", command_code=BenQProjectorCode.MENU, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="up", name="Up", translation_key="up", command_code=BenQProjectorCode.UP, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="down", name="Down", translation_key="down", command_code=BenQProjectorCode.DOWN, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="left", name="Left", translation_key="left", command_code=BenQProjectorCode.LEFT, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="right", name="Right", translation_key="right", command_code=BenQProjectorCode.RIGHT, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="ok", name="OK", translation_key="ok", command_code=BenQProjectorCode.OK, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="hdmi_1", name="HDMI 1", translation_key="hdmi_1", command_code=BenQProjectorCode.HDMI_1, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="hdmi_2", name="HDMI 2", translation_key="hdmi_2", command_code=BenQProjectorCode.HDMI_2, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="vga", name="VGA", translation_key="vga", command_code=BenQProjectorCode.VGA, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="component", name="Component", translation_key="component", command_code=BenQProjectorCode.COMPONENT, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="video", name="Video", translation_key="video", command_code=BenQProjectorCode.VIDEO, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="auto", name="Auto", translation_key="auto", command_code=BenQProjectorCode.AUTO, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="eco_blank", name="Eco Blank", translation_key="eco_blank", command_code=BenQProjectorCode.ECO_BLANK, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="aspect_ratio", name="Aspect Ratio", translation_key="aspect_ratio", command_code=BenQProjectorCode.ASPECT_RATIO, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="mute", name="Mute", translation_key="mute", command_code=BenQProjectorCode.MUTE, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="volume_up", name="Volume Up", translation_key="volume_up", command_code=BenQProjectorCode.VOLUME_UP, entity_registry_enabled_default=False),
    BenQIrButtonEntityDescription(key="volume_down", name="Volume Down", translation_key="volume_down", command_code=BenQProjectorCode.VOLUME_DOWN, entity_registry_enabled_default=False),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up BenQ IR buttons from a config entry."""
    infrared_entity_id = entry.data[CONF_INFRARED_ENTITY_ID]
    device_type = entry.data[CONF_DEVICE_TYPE]

    if device_type == "projector":
        async_add_entities(
            BenQIrButton(entry, infrared_entity_id, description)
            for description in PROJECTOR_BUTTON_DESCRIPTIONS
        )


class BenQIrButton(BenQIrEntity, ButtonEntity):
    """BenQ IR button entity."""

    entity_description: BenQIrButtonEntityDescription

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_entity_id: str,
        description: BenQIrButtonEntityDescription,
    ) -> None:
        """Initialise the button."""
        super().__init__(entry, infrared_entity_id, unique_id_suffix=description.key)
        self.entity_description = description

    async def async_press(self) -> None:
        """Press the button — transmit the IR command."""
        if self.entity_description.command_code is BenQProjectorCode.POWER_OFF:
            await self._send_command_twice(self.entity_description.command_code)
            return

        await self._send_command(self.entity_description.command_code)

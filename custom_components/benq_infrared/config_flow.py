"""Config flow for BenQ IR integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components.infrared import DOMAIN as INFRARED_DOMAIN
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import CONF_DEVICE_TYPE, CONF_INFRARED_ENTITY_ID, DOMAIN


def _get_emitter_entity_ids(flow: ConfigFlow) -> list[str]:
    """Return available infrared emitter entity IDs.

    Newer Home Assistant versions may expose an async_get_emitters helper on the
    infrared integration. Older versions do not, which would make this module
    fail to import and surface as "platform ... config_flow not found".
    """
    infrared_module = flow.hass.components.infrared
    async_get_emitters = getattr(infrared_module, "async_get_emitters", None)
    if callable(async_get_emitters):
        return list(async_get_emitters(flow.hass))

    entity_registry = er.async_get(flow.hass)
    return sorted(
        entry.entity_id
        for entry in entity_registry.entities.values()
        if entry.entity_id
        and entry.domain == INFRARED_DOMAIN
        and entry.disabled_by is None
    )


class BenQIrConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the config flow for BenQ IR."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial setup step."""
        emitter_entity_ids = _get_emitter_entity_ids(self)
        if not emitter_entity_ids:
            return self.async_abort(reason="no_emitters")

        if user_input is not None:
            entity_id   = user_input[CONF_INFRARED_ENTITY_ID]
            device_type = user_input[CONF_DEVICE_TYPE]

            await self.async_set_unique_id(f"benq_ir_{device_type}_{entity_id}")
            self._abort_if_unique_id_configured()

            ent_reg = er.async_get(self.hass)
            entry   = ent_reg.async_get(entity_id)
            entity_name = (
                entry.name or entry.original_name or entity_id if entry else entity_id
            )
            title = f"BenQ Projector via {entity_name}"
            return self.async_create_entry(title=title, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICE_TYPE, default="projector"): SelectSelector(
                        SelectSelectorConfig(
                            options=["projector"],
                            translation_key=CONF_DEVICE_TYPE,
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Required(CONF_INFRARED_ENTITY_ID): EntitySelector(
                        EntitySelectorConfig(
                            domain=INFRARED_DOMAIN,
                            include_entities=emitter_entity_ids,
                        )
                    ),
                }
            ),
        )

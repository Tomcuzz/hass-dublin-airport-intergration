# config_flow.py

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from datetime import timedelta
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

# Constants (matching those in other files)
DOMAIN = "flightaware_tracker"
DEFAULT_SCAN_INTERVAL = 300 # 5 minutes in seconds

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_KEY): str,
})

OPTIONS_SCHEMA = vol.Schema({
    # Time period selector is best for scan_interval in options flow
    vol.Optional(
        CONF_SCAN_INTERVAL, 
        default=timedelta(seconds=DEFAULT_SCAN_INTERVAL)
    ): cv.time_period,
})


class FlightAwareConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for FlightAware Tracker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Simple validation - in a real component, you'd test the API key here
            if not user_input[CONF_API_KEY]:
                errors["base"] = "invalid_auth"
            
            if not errors:
                # Create the entry with the API Key in 'data'
                # The polling interval will be added in the options flow (next step)
                return self.async_create_entry(
                    title="FlightAware Tracker",
                    data=user_input,
                    options={CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL} # Initial option data
                )

        # Show the form to the user
        return self.async_show_form(
            step_id="user", 
            data_schema=DATA_SCHEMA, 
            errors=errors
        )

    # --- OPTIONS FLOW (For Polling Interval) ---
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return FlightAwareOptionsFlowHandler(config_entry)


class FlightAwareOptionsFlowHandler(config_entries.OptionsFlow):
    """Handles options flow for the integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # Update the Config Entry's options
            return self.async_create_entry(title="", data=user_input)

        # Pre-populate the form with current options/defaults
        options_schema = self.add_suggested_values_to_schema(
            OPTIONS_SCHEMA, self.config_entry.options
        )
        
        return self.async_show_form(
            step_id="init", 
            data_schema=options_schema
        )

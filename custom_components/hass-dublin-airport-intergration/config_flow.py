import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME

# The domain of your component
from .const import DOMAIN

class MySensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Sensor Integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # This step is called when the user starts the integration setup.
        
        # Check if an instance already exists (optional, but good practice for no-input setups)
        # If you only want ONE instance of this sensor, uncomment the next block:

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        
        if user_input is not None:
            # If the flow has reached this point, it means the user clicked 'SUBMIT'
            # on a default (empty) form or we are simulating the completion.
            
            # Since we need NO inputs, we immediately create the config entry.
            return self.async_create_entry(
                title="Dublin Airport",
                data={} # Empty data dictionary as no input was gathered
            )

        # Show the default form. Since we haven't provided a schema, it'll be a 
        # single 'SUBMIT' button, effectively.
        return self.async_show_form(step_id="user")

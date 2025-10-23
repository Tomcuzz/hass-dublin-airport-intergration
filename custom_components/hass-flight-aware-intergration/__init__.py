from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS

# The domain of your component
# DOMAIN = "my_sensor_integration"

# List of platforms (like sensor, switch, light) your integration provides
# PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up My Sensor Integration from a config entry."""
    
    # Store the entry data globally if needed, often in hass.data[DOMAIN]
    hass.data.setdefault(DOMAIN, {})
    # hass.data[DOMAIN][entry.entry_id] = entry.data # if you had data to store

    # Forward the setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    
    # Unload platforms (sensor, etc.)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    # Clean up global data if needed
    if unload_ok:
        # hass.data[DOMAIN].pop(entry.entry_id) # if you stored data
        pass

    return unload_ok

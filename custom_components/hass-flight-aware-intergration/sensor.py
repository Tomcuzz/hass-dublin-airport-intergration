# from __future__ import annotations
# import requests
# import datetime
# from homeassistant.components.sensor import SensorEntity
# from homeassistant.config_entries import ConfigEntry
# from homeassistant.core import HomeAssistant
# from homeassistant.helpers.entity import DeviceInfo
# from homeassistant.helpers.entity_platform import AddEntitiesCallback
# import logging

# # Get the domain from your const.py or define it here if you skipped const.py
# try:
#     from .const import DOMAIN
# except ImportError:
#     DOMAIN = "my_sensor_integration"

# _LOGGER = logging.getLogger(__name__)

# # --- Data Fetching Functions (Synchronous) ---
# # These functions MUST run in the executor to avoid blocking HA.

# def _get_today_tempo_state() -> str:
#     """Synchronous function to fetch the state for today."""
#     day_colour = "Unknown"
#     # Check if before 6 AM to get previous day's color, as it persists until 6 AM
#     if datetime.datetime.now().time() < datetime.time(6):
#         today = datetime.date.today()
#         previous_day = today - datetime.timedelta(days=1)
#         formatted_url = previous_day.strftime('https://www.api-couleur-tempo.fr/api/jourTempo/%Y-%m-%d')
#     else:
#         formatted_url = "https://www.api-couleur-tempo.fr/api/jourTempo/today"
    
#     try:
#         response = requests.get(formatted_url, timeout=10)
#         response.raise_for_status() # Raise exception for bad status codes
#         data = response.json()
#         day_colour = data.get('libCouleur', 'Error')
#     except requests.RequestException as e:
#         _LOGGER.error("Failed to fetch Tempo color for today/yesterday: %s", e)
#         day_colour = "Error"
#     except Exception as e:
#         _LOGGER.error("Error processing Tempo data: %s", e)
#         day_colour = "Error"

#     return day_colour


# def _get_tomorrow_tempo_state() -> str:
#     """Synchronous function to fetch the state for tomorrow."""
#     try:
#         response = requests.get("https://www.api-couleur-tempo.fr/api/jourTempo/tomorrow", timeout=10)
#         response.raise_for_status()
#         data = response.json()
        
#         # Check if the API returned a valid color (codeJour != 0)
#         if data.get('codeJour') != 0:
#             return data.get('libCouleur', 'Not Set Yet')
        
#     except requests.RequestException as e:
#         _LOGGER.error("Failed to fetch Tempo color for tomorrow: %s", e)
    
#     return "Not Set Yet" # Default state


# # --- Setup Function (Asynchronous) ---

# async def async_setup_entry(
#     hass: HomeAssistant, 
#     entry: ConfigEntry, 
#     async_add_entities: AddEntitiesCallback
# ) -> None:
#     """Set up the sensor platform."""
    
#     # Initialize sensors with placeholder state. The first async_update will fetch real data.
#     sensors = [
#         TodaySensor(hass, entry), 
#         TomorrowSensor(hass, entry)
#     ]
    
#     async_add_entities(sensors, True)


# # --- Entity Classes (Asynchronous) ---

# class TodaySensor(SensorEntity):
#     """Todays Day Colour."""

#     def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
#         """Initialize the sensor."""
#         self.hass = hass
#         self._attr_name = "Tempo Colour Today" 
#         self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_today_colour"
#         self._state = None # Start with unknown state
#         self._attr_icon = "mdi:palette"
#         self._attr_device_info = DeviceInfo(
#             identifiers={(DOMAIN, entry.entry_id)},
#             name="EDF Tempo Sensor",
#             manufacturer="EDF",
#             model="EDF Tempo API",
#         )

#     @property
#     def native_value(self):
#         """Return the state of the sensor."""
#         return self._state

#     async def async_update(self) -> None:
#         """Fetch new state data for the sensor using the executor."""
#         # Use hass.async_add_executor_job to run the blocking function safely
#         self._state = await self.hass.async_add_executor_job(_get_today_tempo_state)


# class TomorrowSensor(SensorEntity):
#     """Tomorrow Day Colour."""

#     def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
#         """Initialize the sensor."""
#         self.hass = hass
#         self._attr_name = "Tempo Colour Tomorrow"
#         self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_tomorrow_colour"
#         self._state = None # Start with unknown state
#         self._attr_icon = "mdi:palette-outline"
#         self._attr_device_info = DeviceInfo(
#             identifiers={(DOMAIN, entry.entry_id)},
#             name="EDF Tempo Sensor",
#             manufacturer="EDF",
#             model="EDF Tempo API",
#         )

#     @property
#     def native_value(self):
#         """Return the state of the sensor."""
#         return self._state

#     async def async_update(self) -> None:
#         """Fetch new state data for the sensor using the executor."""
#         # Use hass.async_add_executor_job to run the blocking function safely
#         self._state = await self.hass.async_add_executor_job(_get_tomorrow_tempo_state)

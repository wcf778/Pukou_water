"""Constants for the Nanjing Water integration."""
DOMAIN = "nanjing_water"
DEFAULT_NAME = "Nanjing Water"

CONF_OPENID = "openid"
CONF_ACCOUNT = "account"
CONF_JSLUID = "jsluid"
CONF_UPDATE_INTERVAL = "update_interval"

DEFAULT_UPDATE_INTERVAL = 12  # Default to 12 hours

# Sensor types
SENSOR_TYPES = {
    "current_water_usage": {
        "name": "Current Water Usage",
        "unit_of_measurement": "m³",
        "icon": "mdi:water",
    },
    "current_water_fee": {
        "name": "Current Water Fee",
        "unit_of_measurement": "CNY",
        "icon": "mdi:currency-cny",
    },
    "last_water_usage": {
        "name": "Last Month Water Usage",
        "unit_of_measurement": "m³",
        "icon": "mdi:water",
    },
    "last_water_fee": {
        "name": "Last Month Water Fee",
        "unit_of_measurement": "CNY",
        "icon": "mdi:currency-cny",
    },
    "water_price": {
        "name": "Water Price",
        "unit_of_measurement": "CNY/m³",
        "icon": "mdi:currency-cny",
    },
}
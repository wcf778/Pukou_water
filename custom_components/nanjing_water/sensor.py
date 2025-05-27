"""The Nanjing Water sensor."""
from __future__ import annotations

import logging
from datetime import timedelta
import aiohttp
import json

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    DOMAIN,
    SENSOR_TYPES,
    CONF_JSLUID,
    CONF_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

class NanjingWaterCoordinator(DataUpdateCoordinator):
    """Nanjing Water data coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        openid: str,
        account: str,
        jsluid: str,
        update_interval: int,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Nanjing Water",
            update_interval=timedelta(hours=update_interval),
        )
        self.openid = openid
        self.account = account
        self._cookies = {
            "default_unit_second": "input_value",
            "openid": openid,
            "__jsluid_s": jsluid,
        }
        self._headers = {
            "Host": "www.njpkwater.com",
            "Accept": "application/json, text/plain, */*",
            "Sec-Fetch-Site": "same-origin",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-Mode": "cors",
            "Content-Type": "application/json;charset=utf-8",
            "Origin": "https://www.njpkwater.com",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.54(0x1800363a) NetType/WIFI Language/zh_CN",
            "Referer": "https://www.njpkwater.com/weixin/?code=091Moq100u9tiU1BPx2004Bhhq0Moq1g&state=STATE",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty"
        }

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            async with aiohttp.ClientSession() as session:
                # Get current water info
                info_url = "https://www.njpkwater.com/api/info/"
                info_data = {
                    "openid": self.openid,
                    "format": "json"
                }
                
                _LOGGER.debug("Fetching water info with data: %s", info_data)
                async with session.post(
                    info_url,
                    headers=self._headers,
                    cookies=self._cookies,
                    json=info_data
                ) as info_response:
                    info_response.raise_for_status()
                    water_info = await info_response.json()
                    _LOGGER.debug("Received water info: %s", water_info)

                if not water_info:
                    _LOGGER.error("No water info received")
                    return None

                # Get history info
                history_url = "https://www.njpkwater.com/api/gethistory/"
                history_headers = self._headers.copy()
                history_headers["Referer"] = "https://www.njpkwater.com/weixin/history"
                
                history_data = {
                    "huhao": self.account,
                    "format": "json"
                }
                
                _LOGGER.debug("Fetching history info with data: %s", history_data)
                async with session.post(
                    history_url,
                    headers=history_headers,
                    cookies=self._cookies,
                    json=history_data
                ) as history_response:
                    history_response.raise_for_status()
                    history_info = await history_response.json()
                    _LOGGER.debug("Received history info: %s", history_info)

                if not history_info:
                    _LOGGER.error("No history info received")
                    return None

                return {
                    "water_info": water_info[0] if water_info else None,
                    "history_info": history_info[0] if history_info else None,
                    "last_month_info": history_info[1] if len(history_info) > 1 else None,
                }
        except aiohttp.ClientError as err:
            _LOGGER.error("Request failed: %s", err)
            return None
        except json.JSONDecodeError as err:
            _LOGGER.error("JSON decode failed: %s", err)
            return None
        except Exception as err:
            _LOGGER.error("Unexpected error: %s", err)
            return None

class NanjingWaterSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Nanjing Water sensor."""

    def __init__(
        self,
        coordinator: NanjingWaterCoordinator,
        sensor_type: str,
        name: str,
        unit_of_measurement: str,
        icon: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit_of_measurement
        self._attr_icon = icon
        self._attr_unique_id = f"{DOMAIN}_{sensor_type}"

        # Set device class and state class for energy dashboard compatibility
        if sensor_type in ["current_water_usage", "last_water_usage"]:
            self._attr_device_class = SensorDeviceClass.WATER
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif sensor_type in ["current_water_fee", "last_water_fee"]:
            self._attr_device_class = SensorDeviceClass.MONETARY
            self._attr_state_class = SensorStateClass.TOTAL
        elif sensor_type == "water_price":
            self._attr_device_class = SensorDeviceClass.MONETARY
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            _LOGGER.debug("No data available for sensor %s", self._sensor_type)
            return None

        try:
            if self._sensor_type == "current_water_usage":
                value = float(self.coordinator.data["history_info"]["final_water_data"])
            elif self._sensor_type == "current_water_fee":
                value = float(self.coordinator.data["history_info"]["water_fee"])
            elif self._sensor_type == "last_water_usage":
                value = float(self.coordinator.data["last_month_info"]["final_water_data"])
            elif self._sensor_type == "last_water_fee":
                value = float(self.coordinator.data["last_month_info"]["water_fee"])
            elif self._sensor_type == "water_price":
                value = float(self.coordinator.data["history_info"]["water_price"])
            else:
                return None

            _LOGGER.debug("Sensor %s value: %s", self._sensor_type, value)
            return value
        except (KeyError, ValueError, TypeError) as err:
            _LOGGER.error("Error getting value for sensor %s: %s", self._sensor_type, err)
            return None

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Nanjing Water sensors."""
    coordinator = NanjingWaterCoordinator(
        hass,
        entry.data["openid"],
        entry.data["account"],
        entry.data[CONF_JSLUID],
        entry.data[CONF_UPDATE_INTERVAL],
    )
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor_type, sensor_info in SENSOR_TYPES.items():
        entities.append(
            NanjingWaterSensor(
                coordinator,
                sensor_type,
                sensor_info["name"],
                sensor_info["unit_of_measurement"],
                sensor_info["icon"],
            )
        )

    async_add_entities(entities)
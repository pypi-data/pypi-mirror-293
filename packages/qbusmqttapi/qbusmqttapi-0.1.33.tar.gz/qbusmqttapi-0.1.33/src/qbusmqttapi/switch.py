"""QBUS MQTT SWITCH API."""
from __future__ import annotations

import json
import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)


class QbusSwitchAPI:
    """Class for parsing MQTT data messages for DROP devices."""
    def __init__(self) -> None:
        """Initialize the DROP API."""
        self._data_cache = {}
        
    
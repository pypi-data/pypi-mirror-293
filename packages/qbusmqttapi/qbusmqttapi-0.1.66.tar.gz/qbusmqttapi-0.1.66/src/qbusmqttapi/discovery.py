"""QBUS Discovery."""
from __future__ import annotations
import json
import logging

_LOGGER = logging.getLogger(__name__)

KEY_DEVICES = "devices"

KEY_DEVICE_FUNCTIONBLOCKS = "functionBlocks"
KEY_DEVICE_ID = "id"
KEY_DEVICE_IP = "ip"
KEY_DEVICE_MAC = "mac"
KEY_DEVICE_NAME = "name"
KEY_DEVICE_SERIAL_NR = "serialNr"
KEY_DEVICE_TYPE = "type"

KEY_OUTPUT_ID = "id"
KEY_OUTPUT_TYPE = "type"
KEY_OUTPUT_NAME = "name"
KEY_OUTPUT_REF_ID = "refId"
KEY_OUTPUT_PROPERTIES = "properties"
KEY_OUTPUT_ACTIONS = "actions"

KEY_CONTROLLER_CONNECTABLE = "connectable"
KEY_CONTROLLER_CONNECTED = "connected"
KEY_CONTROLLER_ID = "id"
KEY_CONTROLLER_STATE_PROPERTIES = "properties"

   

class QbusSwitch:
    """Class for parsing MQTT discovered switches for Qbus Home Automation."""
    def __init__(self, id: str) -> None:
        """Initialize based on a json loaded dictionary."""
        self._id = id
      
    @property
    def stateOn(self) -> dict:
        stateOn = {}
        stateOn['id'] = self._id
        stateOn['type'] = "state"
        stateOn['properties'] = {}
        stateOn['properties']['value'] = True
        return stateOn
    
    @property
    def stateOff(self) -> dict:
        stateOff = {}
        stateOff['id'] = self._id
        stateOff['type'] = "state"
        stateOff['properties'] = {}
        stateOff['properties']['value'] = False
        return stateOff

class QbusDimmer:
    """Class for parsing MQTT discovered switches for Qbus Home Automation."""
    def __init__(self, id: str) -> None:
        """Initialize based on a json loaded dictionary."""
        self._id = id
      
    @property
    def stateOn(self) -> dict:
        stateOn = {}
        stateOn['id'] = self._id
        stateOn['type'] = "state"
        stateOn['properties'] = {}
        stateOn['properties']['value'] = True
        return stateOn
    
    @property
    def stateOff(self) -> dict:
        stateOff = {}
        stateOff['id'] = self._id
        stateOff['type'] = "state"
        stateOff['properties'] = {}
        stateOff['properties']['value'] = False
        return stateOff   
        
class QbusMqttOutput:
    """Class for parsing MQTT discovered outputs for Qbus Home Automation."""
    
    def __init__(self, dict: dict, device_id: str) -> None:
        """Initialize based on a json loaded dictionary."""
        self._dict = dict
        self._device_id = device_id
        self._state = QbusSwitch | None
        #self._stateMessage: json = {}

    @property
    def id(self) -> str:
        """Return the id."""
        return self._dict.get(KEY_OUTPUT_ID) or ""

    @property
    def type(self) -> str:
        """Return the type."""
        return self._dict.get(KEY_OUTPUT_TYPE) or ""

    @property
    def name(self) -> str:
        """Return the name."""
        return self._dict.get(KEY_OUTPUT_NAME) or ""

    @property
    def ref_id(self) -> str:
        """Return the ref id."""
        return self._dict.get(KEY_OUTPUT_REF_ID) or ""

    @property
    def properties(self) -> dict:
        """Return the properties."""
        return self._dict.get(KEY_OUTPUT_PROPERTIES) or {}

    @property
    def actions(self) -> dict:
        """Return the actions."""
        return self._dict.get(KEY_OUTPUT_ACTIONS) or {}

    
    @property
    def stateMessage(self) -> QbusSwitch | QbusDimmer | None:
        """Return the state Message."""
        if self.type == 'onoff':
            self._state = QbusSwitch(self.id)
        if self.type == 'analog':
            self._state = QbusDimmer(self.id)
        return self._state
    
    @property
    def command_topic(self) -> str:
        "cloudapp/QBUSMQTTGW/" + self._device_id + "/" + self.id + "/setState"
        
    @property
    def state_topic(self) -> str:
        "cloudapp/QBUSMQTTGW/" + self._device_id + "/" + self.id + "/state"
        

class QbusMqttDevice:
    """Class for parsing MQTT discovered devices for Qbus Home Automation."""
    
    def __init__(self, dict: dict) -> None:
        self._dict = dict
        #self._outputs: list[QbusMqttOutput] = []
        #self._connection_state: bool
        #self._state_message: json = {}
        #self._activate: json = {}
        #self._sub_state_topic = ''
        #self._req_state_topic = ''
        
   # async def parse_outputs(self, )
        
    @property
    def id(self) -> str:
        """Return the id."""
        return self._dict.get(KEY_DEVICE_ID) or ""
    
    @property
    def ip(self) -> str:
        """Return the ip address."""
        return self._dict.get(KEY_DEVICE_IP) or ""
    
    @property
    def mac(self) -> str:
        """Return the ip address."""
        return self._dict.get(KEY_DEVICE_MAC) or ""
    
    @property
    def name(self) -> str:
        """Return the ip address."""
        return self._dict.get(KEY_DEVICE_NAME) or ""

    @property
    def serial_number(self) -> str:
        """Return the serial number."""
        return self._dict.get(KEY_DEVICE_SERIAL_NR) or ""

    @property
    def type(self) -> str:
        """Return the mac address."""
        return self._dict.get(KEY_DEVICE_TYPE) or ""
    
    @property
    def outputs(self) -> list[QbusMqttOutput]:
        """Return the outputs."""

        outputs: list[QbusMqttOutput] = []

        if self._dict.get(KEY_DEVICE_FUNCTIONBLOCKS):
            outputs = [QbusMqttOutput(x, self.id) for x in self._dict[KEY_DEVICE_FUNCTIONBLOCKS]]

        #self._outputs = outputs
        return outputs

    @property
    def state_message(self) -> json:
        deviceArray = []
        deviceArray.append(self.id)
        #self._state_message = json.dumps(deviceArray)
        return json.dumps(deviceArray)
    
    @property
    def activate(self) -> json:
        topic = f"cloudapp/QBUSMQTTGW/{self.id}/setState"
        payload ='{"id": "'+ self.id+ '", "type": "action", "action": "activate", "properties": { "authKey": "ubielite" } }'
        self._activate.topic = topic
        self._activate.payload = payload
        message = {}
        message.topic = f"cloudapp/QBUSMQTTGW/{self.id}/setState"
        message.payload = '{"id": "'+ self.id+ '", "type": "action", "action": "activate", "properties": { "authKey": "ubielite" } }'
        #return self._activate
        return message
    
    @property
    def sub_state_topic(self) -> str:
        #self._sub_state_topic = f"cloudapp/QBUSMQTTGW/{self.id}/state"
        return f"cloudapp/QBUSMQTTGW/{self.id}/state"
    
    @property
    def req_state_topic(self) -> str:
        #self._sub_state_topic = f"cloudapp/QBUSMQTTGW/{self.id}/getState"
        return "cloudapp/QBUSMQTTGW/getState"
        
    
class QbusMqttControllerStateProperties:
    """MQTT representation a Qbus controller its state properties."""

    def __init__(self, state: dict) -> None:
        """Initialize based on a json loaded dictionary."""
        self._state = state
        
       
    @property    
    def connectable(self) -> bool | None:
        """Return True if the controller is connectable."""
        return self._state.get('connectable')
    
    @property    
    def connected(self) -> bool | None:
        """Return True if the controller is connected."""
        return self._state.get('connected')
        
class QbusActivateCommand:
    """MQTT representation a Qbus controller state."""

    def __init__(self, id: str) -> None:
        """Initialize based on a json loaded dictionary."""
        self._id = id
        
    @property    
    def payload(self) -> dict:
        activate_payload = {}
        activate_payload['id'] = self._id
        activate_payload['type'] = "action"
        activate_payload['action'] = "activate"
        activate_payload['properties'] = {}
        activate_payload['properties']['authKey'] = "ubielite"      
        return activate_payload
    
    @property    
    def topic(self) -> str:
        topic = 'cloudapp/QBUSMQTTGW/' + self._id + '/setState'
        return topic


class QbusMqttControllerState:
    """MQTT representation a Qbus controller state."""

    def __init__(self) -> None:
        """Initialize based on a json loaded dictionary."""
        self._properties: QbusMqttControllerStateProperties | None = None
        self._activate_command: QbusActivateCommand | None = None
        
    async def parse_state(self, payload: str | bytes) -> bool:
        try:
            json_data = json.loads(payload)
        except ValueError:
            _LOGGER.error(
                "Invalid DROP MQTT discovery payload on %s",
                payload,
            )
            return False
        
        self._id = json_data["id"]
        self._properties = QbusMqttControllerStateProperties(json_data["properties"])
        self._activate_command = QbusActivateCommand(self._id)

        return True
    
    @property
    def id(self) -> str | None:
        """Return the id."""
        return self._id

    @property
    def properties(self) -> QbusMqttControllerStateProperties | None:
        """Return the properties."""
        return self._properties   
    
    @property
    def activate_command(self) -> QbusActivateCommand | None:
        """Return the properties."""
        return self._activate_command   
    
class QbusMqttOutputState:
    """MQTT representation a Qbus output state."""

    def __init__(self, dict: dict) -> None:
        """Initialize based on a json loaded dictionary."""
        self._dict = dict

    @property
    def id(self) -> str:
        """Return the id."""
        return self._dict.get(KEY_OUTPUT_ID) or ""

    @property
    def type(self) -> str:
        """Return the type."""
        return self._dict.get(KEY_OUTPUT_TYPE) or ""

    @property
    def properties(self) -> dict | None:
        """Return the properties."""
        return self._dict.get(KEY_OUTPUT_PROPERTIES)
    
class QbusDiscovery:
    """Class for parsing MQTT discovery messages for Qbus Home Automation."""

    def __init__(self, domain: str) -> None:
        """Initialize."""
        self._domain = domain
        self._devices: list[QbusMqttDevice] = []
        self._hub_id = ""
        self._device_id = ""
        self._device_type = ""
        self._device_desc = ""
        self._name = ""
        self._owner_id = ""
        self._data_topic = ""
        self._command_topic = ""
        self._config_topic = "cloudapp/QBUSMQTTGW/getConfig"
        self._sub_config_topic = "cloudapp/QBUSMQTTGW/config/#"
        self._get_state_topic = "cloudapp/QBUSMQTTGW/getState"
        self._device: QbusMqttDevice = None
           
    async def parse_config(self, config_topic: str, payload: str | bytes) -> bool:
        """Parse an MQTT discovery message and return True if successful."""

        try:
            json_data = json.loads(payload)
        except ValueError:
            _LOGGER.error(
                "Invalid QBUS MQTT discovery payload on %s: %s",
                config_topic,
                payload,
            )
            return False
        
        # Extract the DROP hub ID and DROP device ID from the MQTT topic.
        topic_elements = config_topic.split("/")
        if not (
            topic_elements[2] == "config"
        ):
            return False
        
        # Discovery data must include the Qbus device type and name.
        if (
            KEY_DEVICES in json_data
        ):
            self._devices = [QbusMqttDevice(x) for x in json_data[KEY_DEVICES]]
        else:
            _LOGGER.error(
                "Incomplete MQTT discovery payload on %s: %s", config_topic, payload
            )
            return False
        
        self._name = json_data["app"]
        
        #self._command_topic = f"{self._domain}/{self._hub_id}/cmd/{self._device_id}"
        
        return True
           
               
    @property
    def devices(self) -> list[QbusMqttDevice]:
        """Return the devices."""
        return self._devices    

    @property
    def name(self):
        """Return device name."""
        return self._name
    
    @property
    def device(self):
        """Return device """
        return self._device
    
    @property
    def config_topic(self):
        """Returns config topic"""
        return self._config_topic
    
    @property
    def get_state_topic(self):
        """Returns state topic"""
        return self._get_state_topic

    @property
    def sub_config_topic(self):
        """Returns config topic"""
        return self._sub_config_topic
     
    def set_device(self, id: str) -> QbusMqttDevice | None:
        """Get the device by device id."""
        self._device = next((x for x in self._devices if x.id == id), None)
        return self._device
    

        
    
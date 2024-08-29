"""Vconnex Device"""

from __future__ import annotations

import asyncio
import copy
import json
import logging
import random
import threading
import time
from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from queue import Queue
from types import SimpleNamespace
from typing import Any, NamedTuple
from urllib.parse import urlsplit

import paho.mqtt.client as mqtt

from .api import ReturnCode, VconnexAPI

_LOGGER = logging.getLogger(__name__)

MQTTCLIENT_SUCCESS = 0

NOTIFY_TOPICS_KEY = "notifyTopics"
NOTIFY_TOPIC_PREFIX = "TOPIC-VCX/SmartHome-V2/Notify"
USER_NOTIFY_TOPIC_PREFIX = "/USER/NOTIFY"


class VconnexDevice(SimpleNamespace):
    """Vconnex Device info."""

    deviceId: str
    name: str
    status: int
    version: str
    topicContent: str
    topicNotify: str

    createdTimeStr: str
    modifiedTimeStr: str

    params: list[dict[str, Any]]

    data: dict[str, Any]

    def __init__(self, **kwargs: Any) -> None:
        """Create Vconnex Device object."""
        super().__init__(**kwargs)
        self.data = {}
        if not hasattr(self, "params") or self.params is None:
            self.params = []
        if not hasattr(self, "createdTimeStr"):
            self.createdTimeStr = None
        if not hasattr(self, "modifiedTimeStr"):
            self.modifiedTimeStr = None


class DeviceValue(NamedTuple):
    """Device value."""

    param: str
    value: Any


class DeviceMessage(SimpleNamespace):
    """Device message."""

    name: str
    devExtAddr: str
    devT: int
    batteryPercent: float
    timeStamp: int
    devV: list[dict[str, Any]]


class MqConfig(SimpleNamespace):
    """Message queue config."""

    url: str
    user: str
    password: str


class VconnexDeviceListener(metaclass=ABCMeta):
    """Device listener."""

    @abstractmethod
    def on_device_update(
        self, new_device: VconnexDevice, old_device: VconnexDevice = None
    ):
        """Update device info."""

    @abstractmethod
    def on_device_added(self, device: VconnexDevice):
        """Device Added."""

    @abstractmethod
    def on_device_removed(self, device: VconnexDevice):
        """Device removed."""


class Uninitialized(RuntimeError):
    """Error to indicate object is uninitialized."""


class ReadOnlyDict(dict):
    """Readonly Dict."""

    __readonly = False

    def readonly(self, allow=1):
        """Allow or deny modifying dictionary."""
        self.__readonly = bool(allow)

    def __setitem__(self, key, value):
        if self.__readonly:
            raise TypeError("__setitem__ is not supported")
        return dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        if self.__readonly:
            raise TypeError("__delitem__ is not supported")
        return dict.__delitem__(self, key)


class VconnexDeviceManager:
    """Device manager."""

    __initialized: bool = False

    def __init__(self, api: VconnexAPI) -> None:
        """Create Device Manager object."""
        self.__initialized = False
        self.api = api
        self.mq_client = None
        self.access_config: dict[str, Any] = None
        self.lock: threading.Lock = threading.Lock()

        self.device_map: dict[str, VconnexDevice] = {}
        self.message_listeners: set[Callable[[str, str], None]] = set()
        self.device_listeners: set[VconnexDeviceListener] = set()
        self.device_data_listeners: set[Callable[[str, dict[str, Any]], None]] = set()

        self._device_message_processor: self._DeviceMessageProcessor = None
        self._device_listener_internal: self._DeviceListenerInternal = None
        self._device_sync_processor: self._DeviceSyncProcessor = None

    def __del__(self):
        """Delete Device Manager object."""
        if self.__initialized:
            self.release()

    ###############################################################################
    # Message queue callback
    ###############################################################################
    def _on_mq_connect(self, mqttc: mqtt.Client, user_data: Any, flags, rc):
        data_dict = dict[str, Any](**user_data)
        _LOGGER.info(f"[{data_dict["client_id"]}] Connect flags->{flags}, rc->{rc}")
        if rc == 0 and self.device_map is not None:
            asyncio.run(self._subscribeTopic())

        elif rc != MQTTCLIENT_SUCCESS and self.__initialized:
            _LOGGER.warning("Connect to message queue failure, attempt reconnect...")
            self._init_mq(MqConfig(data_dict["config"]), str(data_dict["client_id"]))

    def _on_mq_connect_fail(self, mqttc: mqtt.Client, user_data: Any):
        data_dict = dict[str, Any](**user_data)
        _LOGGER.info(f"[{data_dict["clientId"]}] Connect fail, attempt reconnect...")
        if self.__initialized:
            self._init_mq(MqConfig(data_dict["config"]), str(data_dict["client_id"]))

    def _on_mq_disconnect(self, client: mqtt.Client, user_data: Any, rc):
        data_dict = dict[str, Any](**user_data)
        if rc != 0:
            _LOGGER.error(
                f"[{data_dict["client_id"]}] Unexpected disconnection. code={rc}"
            )
        else:
            _LOGGER.info(f"[{data_dict["client_id"]}] Disconnect!")

    def _on_mq_subscribe(self, mqttc: mqtt.Client, user_data: Any, mid, granted_qos):
        _LOGGER.debug(f"on_mq_subscribe: mid={mid}")

    def _on_mq_message(self, mqttc: mqtt.Client, user_data: Any, msg: mqtt.MQTTMessage):
        _LOGGER.debug(f"on_mq_message: {msg}")
        if self._device_message_processor is not None:
            self._device_message_processor.add_message(
                msg.topic, msg.payload.decode("utf8")
            )

    def _on_mq_log(self, mqttc: mqtt.Client, user_data: Any, level, string):
        _LOGGER.log(level=level, msg=f"on_mq_log: {string}")

    ###############################################################################
    ###############################################################################

    async def _subscribeTopic(self):
        if self.mq_client is not None and self.mq_client.is_connected():
            if NOTIFY_TOPICS_KEY in self.access_config:
                notifyTopics = list(self.access_config[NOTIFY_TOPICS_KEY])
                for notifyTopic in notifyTopics:
                    try:
                        self.mq_client.subscribe(notifyTopic)
                    except Exception as e:
                        _LOGGER.error(f"Subscribe to topic={notifyTopic} failure: {e}")

            for device in self.device_map.values():
                if device.topicContent is not None:
                    self.mq_client.subscribe(device.topicContent)

    def _get_access_config(self, res_type: str, res_target: str) -> dict[str, Any]:
        try:
            resp = self.api.get(
                "access-config", {"type": res_type, "target": res_target}
            )
            if resp is not None and resp.code == ReturnCode.SUCCESS:
                return resp.data
        except Exception:
            _LOGGER.exception("Oops, something went wrong!")
        return None

    def _get_device_list(self):
        try:
            resp = self.api.get("devices")
            if resp is not None:
                if resp.code == ReturnCode.SUCCESS:
                    raw_list = resp.data
                    if raw_list is not None:
                        device_list = []
                        for raw in raw_list:
                            device_list.append(VconnexDevice(**raw))
                        return device_list
                elif resp.code == ReturnCode.NOT_FOUND:
                    return []
        except Exception:
            _LOGGER.exception("Oops, something went wrong!")
        return None

    def initialize(self) -> bool:
        """Init resource."""
        with self.lock:
            if self.__initialized:
                return False
            try:
                access_config = self._get_access_config("mqtt", "device")
                if access_config is None:
                    _LOGGER.error(
                        "error while get mqtt config access_config is None"
                    )
                    return False
                
                if "mqConfig" in access_config: 
                    self.access_config = access_config
                    mq_config = MqConfig(**access_config["mqConfig"])
                elif "url" in access_config: #old api version
                    mq_config = MqConfig(**access_config)
                    self.access_config = {
                        NOTIFY_TOPICS_KEY: access_config.get(NOTIFY_TOPICS_KEY, []),
                        "mqConfig": access_config
                    }
                else:
                    _LOGGER.error(
                        f"error while get mqtt config access_config={access_config}"
                    )
                    return False
                
                self.__initialized = True

                mq_client_id = f"hass_device_{self.api.get_client_id()}_{int(time.time())}_{random.randint(0, 9)}"
                self._init_mq(mq_config, mq_client_id)
                self._init_device()

                return True
            except Exception:
                _LOGGER.exception("Oops! Initialize failure.")
        return False

    def _init_mq(self, config: MqConfig, client_id: str):
        mqttc = mqtt.Client(
            client_id=client_id,
            clean_session=False,
        )
        mqttc.username_pw_set(config.user, config.password)
        mqttc.user_data_set({"client_id": client_id, "config": config})

        mqttc.on_connect = self._on_mq_connect
        mqttc.on_connect_fail = self._on_mq_connect_fail
        mqttc.on_message = self._on_mq_message
        mqttc.on_disconnect = self._on_mq_disconnect
        mqttc.on_subscribe = self._on_mq_subscribe
        mqttc.on_log = self._on_mq_log

        url = urlsplit(config.url)
        if url.scheme == "ssl" or url.scheme == "mqtts":
            mqttc.tls_set()

        try:
            mqttc.connect(url.hostname, url.port, 30)
            mqttc.loop_start()
            self.mq_client = mqttc
        except Exception:
            _LOGGER.exception("Exception while connect mqtt client.")

    def _init_device(self):
        self._device_listener_internal = self._DeviceListenerInternal(self)
        self.add_device_listener(self._device_listener_internal)

        self._device_sync_processor = self._DeviceSyncProcessor(self, 1800)
        self._device_sync_processor.start()

        self._device_message_processor = self._DeviceMessageProcessor(self, 0.05)
        self._device_message_processor.start()

    def release(self) -> bool:
        """Release resource."""
        with self.lock:
            if not self.__initialized:
                return False
            self.__initialized = False

            self._release_mq()
            self._release_device()

        return True

    def _release_mq(self):
        mqttc = self.mq_client
        if mqttc is not None:
            mqttc.loop_stop()
            if mqttc.is_connected():
                mqttc.disconnect()
            self.mq_client = None

    def _release_device(self):
        self._device_message_processor.stop()
        self._device_message_processor = None

        self._device_sync_processor.stop()
        self._device_sync_processor.join()
        self._device_sync_processor = None

        for device in self.device_map.values():
            for listener in self.device_listeners:
                try:
                    listener.on_device_removed(device)
                except Exception as e:
                    _LOGGER.exception(f"on_device_removed event occur error: {e}")
        self.device_map.clear()

        self.remove_device_listener(self._device_listener_internal)
        self._device_listener_internal = None

    def reload(self) -> bool:
        with self.lock:
            if not self.__initialized:
                return False

            access_config = self._get_access_config("mqtt", "device")
            if access_config is None:
                _LOGGER.error(
                    "error while get mqtt config access_config is None"
                )
                return False
            
            if "mqConfig" in access_config: 
                self.access_config = access_config
                mq_config = MqConfig(**access_config["mqConfig"])
            elif "url" in access_config: #old api version
                mq_config = MqConfig(**access_config)
                self.access_config = {
                    NOTIFY_TOPICS_KEY: access_config.get(NOTIFY_TOPICS_KEY, []),
                    "mqConfig": access_config
                }
            else:
                _LOGGER.error(
                    f"error while get mqtt config access_config={access_config}"
                )
                return False
            
            mq_client_id = f"hass_device_{self.api.get_client_id()}_{int(time.time())}_{random.randint(0, 9)}"
            self._release_mq()
            self._init_mq(mq_config, mq_client_id)

            for device in self.device_map.values():
                for listener in self.device_listeners:
                    try:
                        listener.on_device_removed(device)
                    except Exception as e:
                        _LOGGER.exception(f"on_device_removed event occur error: {e}")
            self.device_map.clear()
            self._device_sync_processor.request_sync()

            return True

    def _check_initialize(self) -> None:
        if not self.is_initialized():
            raise Uninitialized("Object should be initital first")

    def is_initialized(self) -> bool:
        """Check initialized."""
        return self.__initialized

    def add_message_listener(self, listener: Callable[[str, str], None]):
        """Add message listener."""
        self.message_listeners.add(listener)

    def remove_message_listener(self, listener: Callable[[str, str], None]):
        """Remove message listener."""
        self.message_listeners.discard(listener)

    def add_device_listener(self, listener: VconnexDeviceListener):
        """Add device listener."""
        self.device_listeners.add(listener)

    def remove_device_listener(self, listener: VconnexDeviceListener):
        """Remove device listener."""
        self.device_listeners.discard(listener)

    def add_device_data_listener(self, listener: Callable[[str, dict[str, Any]], None]):
        """Add device data listener."""
        self.device_data_listeners.add(listener)

    def remove_device_data_listener(
        self, listener: Callable[[str, dict[str, Any]], None]
    ):
        """Remove device data listener."""
        self.device_data_listeners.discard(listener)

    def get_all_device(self) -> list[VconnexDevice]:
        """Get all device info."""
        return list(self.device_map.values())

    def get_device(self, device_id: str) -> VconnexDevice | None:
        """Get device info by device id."""
        self._check_initialize()
        return self.device_map.get(device_id, None)

    def get_device_data(self, device_id: str) -> dict[str, Any]:
        """Get device data by device id."""
        self._check_initialize()
        if device_id in self.device_map:
            return ReadOnlyDict(self.device_map[device_id].data)
        return None

    def send_commands(self, device_id, command: str, values: dict[str, Any]) -> int:
        """Send device command."""
        self._check_initialize()
        if device_id in self.device_map:
            try:
                body = {"deviceId": device_id, "command": command}
                body["values"] = values

                resp = self.api.post("commands/execute", body)
                result_code = resp.code if resp is not None else ReturnCode.ERROR
                if result_code != ReturnCode.SUCCESS:
                    _LOGGER.warning(
                        f"Execute command [{command}] of [{device_id}] failure with code={result_code}"
                    )
                return result_code
            except Exception:
                _LOGGER.exception("Oops, something went wrong!")
                return ReturnCode.ERROR
        else:
            _LOGGER.warning("Device is not exist")
            return ReturnCode.ERROR

    class _DeviceMessageProcessor(threading.Thread):
        """Device Message Processor."""

        def __init__(
            self,
            mgr: VconnexDeviceManager,
            update_interval: float,
            data_ttl: int = 86400,
        ):
            """Create Device Message Processor object"""
            threading.Thread.__init__(self)
            self.mgr = mgr
            self._running = False
            self._queue = Queue()
            self._update_interval = update_interval
            self._data_ttl = data_ttl

        def start(self) -> None:
            """Start threading."""
            self._running = True
            super().start()

        def stop(self) -> None:
            """Stop threading"""
            self._running = False

        def add_message(self, topic: str, message: str):
            """Add device message to list"""
            self._queue.put((topic, message))

        def handle_message(self, topic: str, message: str):
            """Handle device message."""
            try:
                msg_dict = json.loads(message)
                if topic.startswith(USER_NOTIFY_TOPIC_PREFIX) or topic.startswith(
                    NOTIFY_TOPIC_PREFIX
                ):
                    self.on_notify_message_arrived(topic, msg_dict)
                else:
                    self.on_device_message_arrived(topic, msg_dict)
            except Exception:
                _LOGGER.exception("Something went wrong!!!")

        def on_device_message_arrived(self, topic: str, msg_dict: dict):
            if "name" in msg_dict and "devExtAddr" in msg_dict:
                device = self.mgr.device_map.get(msg_dict.get("devExtAddr"))
                if device is not None:
                    msg_dict["created_ts"] = int(time.time())
                    device.data[msg_dict["name"]] = msg_dict

                    for listener in list(self.mgr.device_data_listeners):
                        listener(device.deviceId, dict(msg_dict))

                    for listener in self.mgr.message_listeners:
                        # FIXME remove
                        listener(topic, json.dumps(msg_dict))
                else:
                    logging.error(
                        f"Device [{msg_dict.get("devExtAddr")}] not exists: topic=[{topic}], msg=[{msg_dict}]"
                    )

        def on_notify_message_arrived(self, topic: str, msg_dict: dict):
            if "name" in msg_dict:
                name = msg_dict["name"]
                if (
                    name == "DeviceChanged"
                    and self.mgr._device_sync_processor is not None
                ):
                    self.mgr._device_sync_processor.request_sync()
                elif name == "AccessConfigChanged":
                    self.mgr.reload()

        def cleanup_data(self):
            expires_ts = int(time.time()) - self._data_ttl
            for device in self.mgr.device_map.values():
                if device.data is not None:
                    for name, msg_dict in list(device.data.items()):
                        if (
                            "created_ts" in msg_dict
                            and msg_dict["created_ts"] <= expires_ts
                        ):
                            device.data.pop(name)

        def run(self) -> None:
            """Run method of threading."""

            cleanup_count_max = int(3600.0 / self._update_interval)
            cleanup_count = cleanup_count_max
            while self._running:
                remaining = self._queue.qsize()
                if remaining > 0:
                    list = []
                    while remaining > 0:
                        list.append(self._queue.get())
                        remaining = remaining - 1

                    for topic, message in list:
                        self.handle_message(topic, message)

                if cleanup_count == 0:
                    cleanup_count = cleanup_count_max
                    self.cleanup_data()
                else:
                    cleanup_count = cleanup_count - 1

                time.sleep(self._update_interval)

    class _DeviceListenerInternal(VconnexDeviceListener):
        """DeviceListenerInternal."""

        def __init__(self, mgr: VconnexDeviceManager):
            """Create Device Message Listener Internal object."""
            self.mgr = mgr

        def on_device_added(self, device: VconnexDevice):
            """On device added."""
            if self.mgr.mq_client is not None and self.mgr.mq_client.is_connected():
                self.mgr.mq_client.subscribe(device.topicContent)
                if hasattr(device, "topicNotify"):
                    self.mgr.mq_client.unsubscribe(device.topicNotify)

        def on_device_removed(self, device: VconnexDevice):
            """On device removed."""
            if self.mgr.mq_client is not None and self.mgr.mq_client.is_connected():
                self.mgr.mq_client.unsubscribe(device.topicContent)
                if hasattr(device, "topicNotify"):
                    self.mgr.mq_client.unsubscribe(device.topicNotify)

        def on_device_update(
            self, new_device: VconnexDevice, old_device: VconnexDevice = None
        ):
            """On device updated."""
            if self.mgr.mq_client is not None and self.mgr.mq_client.is_connected():
                if (
                    old_device is None
                    or old_device.topicContent != new_device.topicContent
                ):
                    if old_device is not None:
                        self.mgr.mq_client.unsubscribe(old_device.topicContent)
                    self.mgr.mq_client.subscribe(new_device.topicContent)

    class _DeviceSyncProcessor(threading.Thread):
        """Device Sync Processor."""

        def __init__(self, mgr: VconnexDeviceManager, update_interval: float) -> None:
            """Create Device Sync Processor object."""
            threading.Thread.__init__(self)
            self._running = False
            self.remaining = 1.0
            self._update_interval = update_interval
            self.mgr = mgr
            self.lock = threading.Lock()

        def run(self):
            """Threading function"""
            self._running = True
            self._on_task_run()

        def stop(self):
            self._running = False

        def _on_task_run(self):
            step = 0.05
            start_sync = False
            while self._running:
                with self.lock:
                    if self.remaining < 0:
                        start_sync = True
                        self.remaining = self._update_interval
                    self.remaining = self.remaining - step

                if start_sync:
                    self.sync_device()
                    start_sync = False
                time.sleep(step)

        def request_sync(self):
            with self.lock:
                self.remaining = 1.0

        def sync_device(self):
            """Sync device."""
            device_list = self.mgr._get_device_list()
            if device_list is None:
                return

            new_device_map = {}
            for device in device_list:
                new_device_map[device.deviceId] = device
            current_device_map = self.mgr.device_map

            new_device_id_list = new_device_map.keys()
            current_device_id_list = current_device_map.keys()

            # Check removed device
            removed_device_id_list = list(
                filter(
                    lambda device_id: device_id not in new_device_id_list,
                    current_device_id_list,
                )
            )
            if len(removed_device_id_list) > 0:
                for device_id in removed_device_id_list:
                    device = current_device_map.pop(device_id)
                    for listener in self.mgr.device_listeners:
                        try:
                            listener.on_device_removed(device)
                        except Exception as e:
                            _LOGGER.exception(
                                f"on_device_removed event occur error: {e}"
                            )

            # Check added device
            added_device_id_list = list(
                filter(
                    lambda device_id: device_id not in current_device_id_list,
                    new_device_id_list,
                )
            )
            if len(added_device_id_list) > 0:
                for device_id in added_device_id_list:
                    device = new_device_map.get(device_id)
                    current_device_map[device_id] = device
                    for listener in self.mgr.device_listeners:
                        try:
                            listener.on_device_added(device)
                        except Exception as e:
                            _LOGGER.exception(f"on_device_added event occur error: {e}")

            # Check modified device
            modified_device_tuple_list: list[tuple[VconnexDevice, VconnexDevice]] = []
            for device_id in current_device_id_list:
                if device_id in new_device_id_list:
                    current_device = current_device_map[device_id]
                    new_device = new_device_map[device_id]
                    try:
                        if (
                            current_device.createdTimeStr != new_device.createdTimeStr
                            or current_device.modifiedTimeStr
                            != new_device.modifiedTimeStr
                        ):
                            current_device_data = current_device.data
                            old_device = copy.deepcopy(current_device)
                            for attr in vars(new_device):
                                setattr(current_device, attr, getattr(new_device, attr))
                            current_device.data = current_device_data
                            old_device.data = None
                            modified_device_tuple_list.append(
                                (current_device, old_device)
                            )
                    except Exception:  # py-lint: disable=broad-except
                        _LOGGER.exception("Oops, something went wrong!")

            if len(modified_device_tuple_list) > 0:
                for device_tuple in modified_device_tuple_list:
                    for listener in self.mgr.device_listeners:
                        try:
                            listener.on_device_update(*device_tuple)
                        except Exception as e:
                            _LOGGER.exception(
                                f"on_device_update event occur error: {e}"
                            )

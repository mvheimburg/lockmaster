from typing import Any, Callable
import asyncio
import logging
from paho.mqtt.client import Client, MQTTMessage
from paho.mqtt.enums import CallbackAPIVersion
from .config import MqttSettings, MqttTopics
from doorbell.config.payloads import BELL
from doorbell.models.models import Subscription


_LOGGER = logging.getLogger(__name__)

class MqttClient(Client):
    def __init__(self, settings: MqttSettings = MqttSettings(),
                 logger: logging.Logger | None = None):
        # if logger is None:
        #     logger = logging.getLogger(__name__)
        # print(f"logger is :{logger}")
        # self._logger = logger
        self._settings = settings
        self._background_tasks: set[asyncio.Task[Any]] = set()
        super().__init__(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=settings.client_id,
            transport="tcp"
        )
        self.username_pw_set(settings.username, settings.password)

        self.topics = MqttTopics.load()
        self.subscriptions: list[Subscription] = []


    # def subscribe_all(self):
    #     self.subscribe(self.mode_config.command_topic, qos=0)
    #     self.subscribe(self.state_config.command_topic, qos=0)


    def subscribe_callback(self, topic: str, callback: Callable[[MQTTMessage], None], qos: int = 0):
        """Subscribe to a topic and add the subscription to the list of subscriptions.

        Call this method before calling connect() to ensure
        that the subscription is re-established after a reconnect.

        Parameters
        ----------
        topic : str
            The topic to subscribe to.
        callback : Callable
            The callback function to call when a message is received on the topic.
        qos:
            The Quality of Service level for this subscription
        """
        if topic in [subscription.topic for subscription in self.subscriptions]:
            print(f"Already subscribed to topic: {topic}")
            return

        def callback_wrapper(_, __, message: MQTTMessage):  # To match paho-mqtt on_message callback signature.
            callback(message)

        self.subscriptions.append(Subscription(topic=topic, qos=qos))

        self.message_callback_add(topic, callback_wrapper)

    def connect_std_creds(self):
        print(f"Connecting to: \
                          {self._settings.broker_url} : \
                          {self._settings.broker_port}")
        self.connect(
            host=self._settings.broker_url,
            port=self._settings.broker_port,
        )

    async def ring_bell(self):
        print('ringing that bell')
        self.publish(self.topics.bell.command, payload=BELL.COMMAND.DO)


    def garage_command(self, command: str):
        self.publish(self.topics.garage.command, payload=command)

      
from os import environ
from fastapi_mqtt import FastMQTT, MQTTConfig
import logging

logger = logging.getLogger(__name__)    

class MqttLayer():

    def __init__(self) -> None:
        ######### MQTT ###################

        host = environ.get('MQTT_HOST', 'mqtt://localhost')
        port = environ.get('MQTT_PORT', '1883')
        username = environ.get('MQTT_USERNAME', None)
        password = environ.get('MQTT_PASSWORD', None)

        mqtt_config = MQTTConfig(host = host,
                                port= port,
                                keepalive = 60,
                                username=username,
                                password=password)

        mqtt = FastMQTT(
            config=mqtt_config
        )

        self.mqtt.init_app(app)


    @mqtt.on_connect()
    def connect(client, flags, rc, properties):
        # mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
        print("Connected: ", client, flags, rc, properties)
        # doormanager.subscribe()


    @mqtt.on_message()
    async def message(client, topic, payload, qos, properties):
        print("Message: ", client, topic, payload)
        # payload_str = msg.payload.decode("utf-8") 
        # doormanager.mqtt_on_message(topic, payload.decode())


    @mqtt.on_disconnect()
    def disconnect(client, packet, exc=None):
        print("Disconnected")

    @mqtt.on_subscribe()
    def subscribe(client, mid, qos, properties):
        print("subscribed", client, mid, qos, properties)

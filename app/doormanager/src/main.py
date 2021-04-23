"""Application module."""
from os import environ, path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mqtt import FastMQTT, MQTTConfig

from containers import Container
import endpoints as ep

def create_app() -> FastAPI:
    container = Container()
    current_dir = path.dirname(path.realpath(__file__))
    config_path = path.join(current_dir, "config.yaml")
    container.config.from_yaml(config_path)
    container.wire(modules=[ep])

    # doormanager=container.doormanager()
    # doormanager.connect_to_broker()
    # doormanager.subscribe()
    doormanager=container.doormanager()

    db = container.db()
    db.create_database()

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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

    mqtt.init_app(app)


    @mqtt.on_connect()
    def connect(client, flags, rc, properties):
        # mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
        print("Connected: ", client, flags, rc, properties)
        doormanager.subscribe(client)


    @mqtt.on_message()
    async def message(client, topic, payload, qos, properties):
        print("Message: ", client, topic, payload)
        # payload_str = msg.payload.decode("utf-8") 
        doormanager.mqtt_on_message(client, topic, payload.decode())


    @mqtt.on_disconnect()
    def disconnect(client, packet, exc=None):
        print("Disconnected")

    @mqtt.on_subscribe()
    def subscribe(client, mid, qos, properties):
        print("subscribed", client, mid, qos, properties)

    app.container = container
    app.include_router(ep.router)

    return app

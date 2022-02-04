"""Application module."""
from os import access, environ, path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mqtt import FastMQTT, MQTTConfig

from containers import Container
import endpoints as ep


def create_app() -> FastAPI:
    app = FastAPI()
    
    app.container = Container()
    current_dir = path.dirname(path.realpath(__file__))
    config_path = path.join(current_dir, "config.yaml")
    app.container.config.from_yaml(config_path)
    app.container.wire(modules=[ep])

    bell_service=app.container.bell_service()
    door_service=app.container.door_service()  
    access_service=app.container.access_service()  

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    build_type = environ.get('BUILD_TYPE', None)   

    if build_type == 'release':
        print("Going MQTT")

        host = environ.get('MQTT_HOST', 'mqtt://localhost')
        print(f"host: {host}")
        port = int(environ.get('MQTT_PORT', 1883))
        print(f"port: {port}")
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
            access_service.set_mqttc(mqttc=client)
            bell_service.set_mqttc(mqttc=client)
            door_service.set_mqttc(mqttc=client)
            access_service.subscribe()
            door_service.subscribe()


        @mqtt.on_message()
        async def message(client, topic, payload, qos, properties):
            # print("Message: ", client, topic, payload)
            # payload_str = msg.payload.decode("utf-8") 
            topiclist=topic.split("/")
            if topiclist[0] == "door":
                door_service.mqtt_on_message(topic, payload.decode())
            elif topiclist[0] == "room-assistant":
                access_service.mqtt_on_message(client, properties, topiclist, payload.decode())
            


        @mqtt.on_disconnect()
        def disconnect(client, packet, exc=None):
            print("Disconnected")

        @mqtt.on_subscribe()
        def subscribe(client, mid, qos, properties):
            print("subscribed", client, mid, qos, properties)


    print("include_router")
    app.include_router(ep.router)

    print("return app")
    return app


app = create_app()
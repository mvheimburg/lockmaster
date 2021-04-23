import os, sys
import yaml
from box import Box



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mqtt import FastMQTT, MQTTConfig
from fastapi_utils.tasks import repeat_every


# from database.databasemanager import DatabaseManager
from door.doormanager import DoorManager


def create_app() -> FastAPI:

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    ######### MQTT ###################
    host = os.environ.get('MQTT_HOST', 'mqtt://localhost')
    port = os.environ.get('MQTT_PORT', '1883')
    username = os.environ.get('MQTT_USERNAME', None)
    password = os.environ.get('MQTT_PASSWORD', None)

    mqtt_config = MQTTConfig(host = host,
                            port= port,
                            keepalive = 60,
                            username=username,
                            password=password)

    mqtt = FastMQTT(
        config=mqtt_config
    )
    mqtt.init_app(app)
    #################################



    ############# DOORMANAGER #####
    cfg = None
    current_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(current_dir, "config.yaml")
    with open(path, 'r') as stream:
        cfg = yaml.load(stream, Loader=yaml.FullLoader)

    cfg = Box(cfg)
    print(cfg)




    # databasemanager = DatabaseManager()
    doormanager = DoorManager(mqtt=mqtt, doors_cfg=cfg)
    ###############################



    @mqtt.on_connect()
    def connect(client, flags, rc, properties):
        # mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
        print("Connected: ", client, flags, rc, properties)
        doormanager.subscribe()


    @mqtt.on_message()
    async def message(client, topic, payload, qos, properties):
        print("Message: ", client, topic, payload)
        # payload_str = msg.payload.decode("utf-8") 
        doormanager.mqtt_on_message(topic, payload.decode())



    @mqtt.on_disconnect()
    def disconnect(client, packet, exc=None):
        print("Disconnected")

    @mqtt.on_subscribe()
    def subscribe(client, mid, qos, properties):
        print("subscribed", client, mid, qos, properties)



    @app.on_event("startup")
    async def startup():
        doormanager.startup()
        # databasemanager.startup()
        # await database.connect()

    # @app.on_event("shutdown")
    # async def shutdown():
    #     await database.disconnect()



    @app.on_event("startup")
    @repeat_every(seconds=10)  
    async def publish_all():
        doormanager.publish_status()



    @app.get("/test")
    async def root():
        print('ROOT Called')
        return {"message": "Hello World"}

    return app
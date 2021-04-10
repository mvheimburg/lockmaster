import os, sys
import yaml

from doormanager import DoorManager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mqtt import FastMQTT, MQTTConfig
from fastapi_utils.tasks import repeat_every
# from pydispatch import dispatcher

# SIGNAL = 'my-first-signal'

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

host = os.environ.get('MQTT_HOST', 'mqtt://localhost')
port = os.environ.get('MQTT_PORT', '1883')
username = os.environ.get('MQTT_USERNAME', None)
password = os.environ.get('MQTT_PASSWORD', None)

mqtt_config = MQTTConfig(host = host,
                        port= 1883,
                        keepalive = 60,
                        username=username,
                        password=password)

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)


cfg = None
current_dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(current_dir, "config.yaml")
with open(path, 'r') as stream:
    cfg = yaml.load(stream, Loader=yaml.FullLoader)
print(cfg)
doormanager = DoorManager(config=cfg)

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    # mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)
    for door in cfg:
        topic = cfg[door]["command_topic"]
        print(f"subscribing to topic: {topic}")
        mqtt.client.subscribe(topic, qos=0)

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
@repeat_every(seconds=1)  
async def publish_all():
    # for door in self._config:
        # if self._config[door]["state"] != "Unknown":
    for door in cfg:
        state = doormanager.get_state(door)
        print(f"State of door {door}: {state}")
        if state != "Unknown":
            print("publishing")
            await mqtt.publish(cfg[door]["state_topic"], state)

    return {"result": True,"message":"Published" }



# def handle_event( sender ):
#     """Simple event handler"""
#     print('Signal was sent by', sender)

# dispatcher.connect( handle_event, signal=SIGNAL, sender=dispatcher.Any )



@app.get("/test")
async def root():
    print('ROOT Called')
    return {"message": "Hello World"}



@app.get("/test")
async def root():
    print('ROOT Called')
    return {"message": "Hello World"}
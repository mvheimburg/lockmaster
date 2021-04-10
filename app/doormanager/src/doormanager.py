import os

from threading import Thread
from time import sleep

# import paho.mqtt.client as mqtt
import urllib.parse
import gpiozero

# from pydispatch import dispatcher
# import protos.doormanager_pb2_grpc as pb2_grpc
# import protos.doormanager_pb2 as pb2

# SIGNAL = 'my-first-signal'

from const import(
    COMMAND_PAYLOAD
    ,STATUS_PAYLOAD
)

class DoorManager():

    # def Test(self, request, context):
    #     print('getting Test request')
    #     return pb2.TestReply(rep='testing 123....')

    # def ToggleDoor(self, request, context):
    #     print('getting Test request')
    #     self.toggle_door(request.nr)
    #     return pb2.ToggleDoorReply()

    def __init__(self, client_id=None, config=None):
        print(client_id)

        # client_id = os.environ.get('MQTT_CLIENT_ID', None)
        # self._mqttc = mqtt.Client(client_id)
        self._config = config
        # self._mqttc.on_message = self.mqtt_on_message
        # self._mqttc.on_connect = self.mqtt_on_connect
        # self._mqttc.on_publish = self.mqtt_on_publish
        # self._mqttc.on_subscribe = self.mqtt_on_subscribe

        for door in self._config:
            relay = gpiozero.OutputDevice(self._config[door]["bcd_pin_number"], active_high=False, initial_value=False)
            self._config[door].update({"relay":relay})

        # self.mqtt_connect_to_broker()
        # self.mqtt_subscribe()
        # self.mqtt_run()

        # t = Thread(target=self.publish_status_intervals, args=(), daemon=True)
        # t.start()
        self.update_status()


    def update_status(self):
        for door in self._config:
            if self._config[door]["relay"].value:
                self._config[door].update({"state": STATUS_PAYLOAD.LOCKED})
            else:
                self._config[door].update({"state": STATUS_PAYLOAD.UNLOCKED})

        # dispatcher.send( signal=SIGNAL, sender=self )

    # def publish_status(self):
    #     self.update_status()
    #     for door in self._config:
    #         if self._config[door]["state"] != "Unknown":
    #             self._mqttc.publish(self._config[door]["state_topic"], payload=self._config[door]["state"])

    # def publish_status_intervals(self):
    #     self.publish_status()
    #     sleep(10)


    def unlock_door(self, index):
        print(f"Unlocking door {index}")
        self._config[index]["relay"].off()
        self.update_status()
        # self.publish_status()


    def lock_door(self, index):
        print(f"Locking door {index}")
        self._config[index]["relay"].on()
        self.update_status()
        # self.publish_status()

    def toggle_door(self, index):
        print(f"Toggling door {index}")
        self._config[index]["relay"].toggle()
        self.update_status()
        # self.publish_status()

    def get_state(self, index):
        return self._config[index]["state"]


    # ### MQTT FUNCTIONS AND CALLBACKS
    # def mqtt_on_connect(self, mqttc, obj, flags, rc):
    #     print("rc: "+str(rc))
    #     print(f"flag: {flags}")

    def mqtt_on_message(self, topic, payload):
        # print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        
        # topic_array = msg.topic.split("/")
        # payload_str = msg.payload.decode("utf-8")  
        print("Doormanager message: ", topic, payload) 
        for door in self._config:
            if topic == self._config[door]["command_topic"]:
                if payload == COMMAND_PAYLOAD.LOCK:
                    print(f"Doormanager message: Locking door {door}") 
                    self.lock_door(door)
                elif payload == COMMAND_PAYLOAD.UNLOCK:
                    print(f"Doormanager message: Unlocking door {door}") 
                    self.unlock_door(door)
                    

    # def mqtt_on_publish(self, mqttc, obj, mid):
    #     print("mid: "+str(mid))

    # def mqtt_on_subscribe(self, mqttc, obj, mid, granted_qos):
    #     print("Subscribed: "+str(mid)+" "+str(granted_qos))

    # def mqtt_on_log(self, mqttc, obj, level, string):
    #     print(string)

    # def tls_set(self):
    #     #TODO: sett ssl and cert for encrypt
    #     pass

    # def mqtt_connect_to_broker(self):
    #     broker = os.environ.get('MQTT_SERVER', 'mqtt://localhost:1883')
    #     username = os.environ.get('MQTT_USERNAME', None)
    #     password = os.environ.get('MQTT_PASSWORD', None)
    #     print(f"connecting to broker {broker}")
    #     print(f"Username: {username}, Password: {password}")
    #     broker_parsed = urllib.parse.urlparse(broker)
    #     self._mqttc.username_pw_set(username, password=password)
    #     self._mqttc.connect(broker_parsed.hostname, port=broker_parsed.port, keepalive=60)


    # def mqtt_subscribe(self):
    #     for door in self._config:
    #         topic = self._config[door]["command_topic"]
    #         print(f"subscribing to topic: {topic}")
    #         self._mqttc.subscribe(topic, qos=0)


    # def mqtt_run(self):
    #     self._mqttc.loop_start()
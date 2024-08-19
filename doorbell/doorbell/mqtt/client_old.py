#!/usr/local/bin/python
# -*- coding: utf-8 -*-
__author__ = 'mvheimburg'


import paho.mqtt.client as mqtt


from doorbell.models import AccessModel
from doorbell.config.config import DoorsConfig, MqttCfg


class MqttClinet():
    """
    """
    _mqttc = mqtt.Client

    def __init__(self) -> None:
        super().__init__()

        self.doors_config = DoorsConfig.load()

        mqtt_cfg = MqttCfg.load()
        self.bell_config = mqtt_cfg.bell
        self.garage_config = mqtt_cfg.garage
        self.mode_config = mqtt_cfg.mode
        self.state_config = mqtt_cfg.state


        # self.screen_timer = Timer(callback=self.screen_time_out ,time=SCREEN_TIMER)
        # self.log_out_timer = Timer(callback= self.log_out ,time=LOGOUT_TIMER)

        try:
            self._mqttc.on_message = self.mqtt_on_message
            self._mqttc.on_connect = self.mqtt_on_connect
            self._mqttc.on_publish = self.mqtt_on_publish
            self._mqttc.on_subscribe = self.mqtt_on_subscribe
            self._mqttc = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                client_id=MQTT_SETTINGS.client_id)
            self._mqttc.username_pw_set(MQTT_SETTINGS.username, password=MQTT_SETTINGS.password)

            print("STARTING MQTT")
            self._mqttc.connect(MQTT_SETTINGS.broker, port=MQTT_SETTINGS.port, keepalive=60)
        except Exception:
            self._mqttc = None
        else:
            self._mqttc.loop_start()

        self.bellsound = SoundLoader.load('frontend/assets/audio/bell-ringing-05.wav')


    def presence_detected(self, am:dict):
        am=AccessModel(**am, login_state = LoginState.PRESENCE_IN)
        print(f"presence_detected: {am}")
        # if self.current_user != am.name:
        print(f"self.current_user: {self.current_user }")
        if self.current_user.login_state == LoginState.OUT:
            # if self.current_user != am:
            print("Setting new user")
            self.current_user = am
        elif self.current_user.name == am.name:
            self.extend_screen_timer()


    def on_current_user(self, instance, value):
        print(value)
        try:
            if value.access_level>0:
                if value.name is not None:
                    user = str(value.name)
                    print(f"Current user is {user}")
                    # toast(f"Velkommen {user}")
                    MDSnackbar(
                        MDSnackbarText(
                            text=f"Velkommen {user}",
                        ),
                        y=dp(24),
                        pos_hint={"center_x": 0.5},
                        size_hint_x=0.5,
                    ).open()
                else:
                    print(f"Login user is {None}")

                self.change_screen('Control')
                self.screens['DoorBell']["object"].login_feedback(True)
        except Exception as e:
            print(e)


    def get_door_name(self, door_nr, *args):
        print(door_nr)
        door = self.doors_config.get_name_by_nr(door_nr)
        if door is not None:
            return door.name
        else:
            return ""

    def get_door_id(self, door_nr, *args):
        print(door_nr)
        door = self.doors_config.get_id_by_nr(door_nr)
        if door is not None:
            return door.name
        else:
            return ""

    def login_from_pin(self, result):
        print(f"login response: {result}")
        print(f"self.current_user: {self.current_user}")
        if self.current_user.login_state == LoginState.OUT:
            self.current_user = AccessModel(access_level=result, login_state = LoginState.PIN_IN)

    def log_out(self, *args):
        print(f"Log out, user {self.current_user.name}")
        self.current_user = AccessModel(access_level=0, login_state = LoginState.OUT)
        print(f"Logged out, user {self.current_user}")
        if self.screen_timer.running:
            self.screen_timer.stop()
        if self.log_out_timer.running:
            self.log_out_timer.stop()


    def extend_log_out_timer(self):
        self.log_out_timer.reset()


    def start_screen_timer(self):
        self.screen_timer.start()


    def screen_time_out(self):
        self.change_screen('DoorBell')
        if self.current_user.login_state == LoginState.PIN_IN:
            # self.start_log_out_timer()
            self.log_out_timer.start()
        else:
            self.log_out()


    def extend_screen_timer(self):
        self.screen_timer.reset()


    def mqtt_on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))
        print(f"flag: {flags}")
        self.mqttc_subscribe()
        # self.mqttc_run()



    def mqtt_on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        topic = msg.topic
        payload = msg.payload.decode("utf-8")

        # door = self.doors_config.get_by_state_topic(topic)
        # if door is not None:
        #     print(f"state received")
        #     if payload == DOORLOCK_STATE.LOCKED:
        #         door.state="LOCKED"
        #         self.screens['Control']["object"].update_door_states(door.door_id,True)

        #     elif payload == DOORLOCK_STATE.UNLOCKED:
        #         door.state="UNLOCKED"
        #         self.screens['Control']["object"].update_door_states(door.door_id, False)

        if topic == self.mode_config.command_topic:
            print(f"mode received: {payload}")
            self.mode_config.state = payload


    def mqtt_on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def mqtt_on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def mqtt_on_log(self, mqttc, obj, level, string):
        print(string)

    def tls_set(self):
        #TODO: sett ssl and cert for encrypt
        pass

    # def mqttc_connect_to_broker(self):
    #     print(f"connecting to broker {MQTT_SETTINGS.broker} as {MQTT_SETTINGS.client_id}")
    #     # broker_parsed = urllib.parse.urlparse(MQTT_SETTINGS.broker)
    #     self._mqttc.username_pw_set(MQTT_SETTINGS.username, password=MQTT_SETTINGS.password)
    #     self._mqttc.connect(MQTT_SETTINGS.broker, port=MQTT_SETTINGS.port, keepalive=60)


    def mqttc_subscribe(self):
        # for door in self.doors_config.doors:
        #     print(f"Subscribing: {door.topic.state}")
        #     self._mqttc.subscribe(door.topic.state, qos=1)
        self._mqttc.subscribe(self.mode_config.command_topic, qos=0)
        self._mqttc.subscribe(self.state_config.command_topic, qos=0)

    # def mqttc_run(self):
    #     self._mqttc.loop_start()

    def ring_bell(self):
        print('ringing that bell')
        print(f'self.mode_config.state: {self.mode_config.state}')
        self._mqttc.publish(self.bell_config.command_topic, payload=BELL_COMMAND_PAYLOAD.DO)
        if self.mode_config.state == MODE_COMMAND_PAYLOAD.NORMAL:
            pass
        elif self.mode_config.state == MODE_COMMAND_PAYLOAD.HALLOWEEN:
           self.change_screen('Scary')



        print("Sound found at %s" % self.bellsound.source)
        print("Sound is %.3f seconds" % self.bellsound.length)
        self.bellsound.play()


    def toggle_state(self, *args):
        print(f"Toggle state: {args}")


    def garage_open(self, *args):
        self.garage_command(GARAGE_COMMAND_PAYLOAD.OPEN)

    def garage_close(self, *args):
        self.garage_command(GARAGE_COMMAND_PAYLOAD.CLOSE)

    def garage_stop(self, *args):
        self.garage_command(GARAGE_COMMAND_PAYLOAD.STOP)

    def garage_command(self, command):
        self._mqttc.publish(self.garage_config.command_topic, payload=command)

    def next_screen(self):
        self.change_screen(self.gui.next())

    def prev_screen(self):
        self.change_screen(self.gui.previous())

    def change_screen(self, screen_name):
        if screen_name == 'Control':
            self.start_screen_timer()
        self.gui.current = screen_name

import paho.mqtt.client as mqtt
import urllib.parse


import protos.doormanager_pb2_grpc as pb2_grpc
import protos.doormanager_pb2 as pb2


class DoorManager(pb2_grpc.DoorManagerServicer):
    def __init__(self, client_id=None, config=None):
        print(client_id)
        self._config = config

    def Test(self, request, context):
        print('getting Test request')
        return pb2.TestReply(rep='testing 123....')
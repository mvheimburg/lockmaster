import requests
# from typing import Callable
import json
import xmlrpc.client
from models import AccessModel

from os import environ

# DOORBELL_URL="http://192.168.1.100:80"
DOORBELL_URL = environ.get('DOORBELL_URL')

# def presence_out_of_bounds(am:AccessModel):
#     with xmlrpc.client.ServerProxy(DOORBELL_URL) as proxy:
#         try:
#             success = proxy.presence_out_of_bounds(am.dict())
#         except xmlrpc.client.Fault as e:
#             print(e)
#         except OSError as e:
#             print(e)


def presence_detected(am:AccessModel):
    with xmlrpc.client.ServerProxy(DOORBELL_URL) as proxy:
        try:
            success = proxy.presence_detected(am.dict())
        except xmlrpc.client.Fault as e:
            print(e)
        except OSError as e:
            print(e)

    # req = f"{DOORBELL_URL}/presence_detected/"
    # data=json.dumps(am)
    # r = requests.put(req, data=data)
    # print(r)
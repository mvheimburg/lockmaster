# import requests
from typing import Callable
import json
import xmlrpc.client
from models import AccessModel

DOORBELL_URL="http://192.168.1.100:80"

def presence_out_of_bounds(am:AccessModel):
    with xmlrpc.client.ServerProxy(DOORBELL_URL) as proxy:
        try:
            success = proxy.presence_out_of_bounds(am.dict())
        except xmlrpc.client.Fault as e:
            print(e)

def presence_detected(am:AccessModel):
    with xmlrpc.client.ServerProxy(DOORBELL_URL) as proxy:
        try:
            success = proxy.presence_detected(am.dict())
        except xmlrpc.client.Fault as e:
            print(e)

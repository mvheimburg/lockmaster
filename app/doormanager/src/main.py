import os, sys
import yaml

from threading import Event

from concurrent import futures
import grpc

import protos.doormanager_pb2_grpc as pb2_grpc

from doormanager import DoorManager


def main():

    cfg = None
    current_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(current_dir, "config.yaml")
    with open(path, 'r') as stream:
        cfg = yaml.load(stream, Loader=yaml.FullLoader)
    print(cfg)

    stop_event = Event()
    port = os.environ.get('DOORMANAGER_GRPC_PORT')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    print('allocated server')
    pb2_grpc.add_DoorManagerServicer_to_server(DoorManager(config=cfg['doors']), server)
    print('added Server to grpc server')

    server.add_insecure_port(f'[::]:{port}')

    print(f'allocated port {port}')
    server.start()
    print('server started')
    stop_event.wait()
    server.stop(GRPC_GRACE)

# Tests
if __name__ == '__main__':
    main()


# ustates = States(36, 38, 40)

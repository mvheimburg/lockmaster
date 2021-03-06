# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import doormanager_pb2 as protos_dot_doormanager__pb2


class DoorManagerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Test = channel.unary_unary(
                '/doormanager.DoorManager/Test',
                request_serializer=protos_dot_doormanager__pb2.TestRequest.SerializeToString,
                response_deserializer=protos_dot_doormanager__pb2.TestReply.FromString,
                )
        self.UnlockDoor = channel.unary_unary(
                '/doormanager.DoorManager/UnlockDoor',
                request_serializer=protos_dot_doormanager__pb2.UnlockDoorRequest.SerializeToString,
                response_deserializer=protos_dot_doormanager__pb2.UnlockDoorReply.FromString,
                )
        self.LockDoor = channel.unary_unary(
                '/doormanager.DoorManager/LockDoor',
                request_serializer=protos_dot_doormanager__pb2.LockDoorRequest.SerializeToString,
                response_deserializer=protos_dot_doormanager__pb2.LockDoorReply.FromString,
                )
        self.ToggleDoor = channel.unary_unary(
                '/doormanager.DoorManager/ToggleDoor',
                request_serializer=protos_dot_doormanager__pb2.ToggleDoorRequest.SerializeToString,
                response_deserializer=protos_dot_doormanager__pb2.ToggleDoorReply.FromString,
                )
        self.GetDoorState = channel.unary_unary(
                '/doormanager.DoorManager/GetDoorState',
                request_serializer=protos_dot_doormanager__pb2.GetDoorStateRequest.SerializeToString,
                response_deserializer=protos_dot_doormanager__pb2.GetDoorStateReply.FromString,
                )


class DoorManagerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Test(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnlockDoor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LockDoor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ToggleDoor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDoorState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DoorManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Test': grpc.unary_unary_rpc_method_handler(
                    servicer.Test,
                    request_deserializer=protos_dot_doormanager__pb2.TestRequest.FromString,
                    response_serializer=protos_dot_doormanager__pb2.TestReply.SerializeToString,
            ),
            'UnlockDoor': grpc.unary_unary_rpc_method_handler(
                    servicer.UnlockDoor,
                    request_deserializer=protos_dot_doormanager__pb2.UnlockDoorRequest.FromString,
                    response_serializer=protos_dot_doormanager__pb2.UnlockDoorReply.SerializeToString,
            ),
            'LockDoor': grpc.unary_unary_rpc_method_handler(
                    servicer.LockDoor,
                    request_deserializer=protos_dot_doormanager__pb2.LockDoorRequest.FromString,
                    response_serializer=protos_dot_doormanager__pb2.LockDoorReply.SerializeToString,
            ),
            'ToggleDoor': grpc.unary_unary_rpc_method_handler(
                    servicer.ToggleDoor,
                    request_deserializer=protos_dot_doormanager__pb2.ToggleDoorRequest.FromString,
                    response_serializer=protos_dot_doormanager__pb2.ToggleDoorReply.SerializeToString,
            ),
            'GetDoorState': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDoorState,
                    request_deserializer=protos_dot_doormanager__pb2.GetDoorStateRequest.FromString,
                    response_serializer=protos_dot_doormanager__pb2.GetDoorStateReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'doormanager.DoorManager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DoorManager(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Test(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/doormanager.DoorManager/Test',
            protos_dot_doormanager__pb2.TestRequest.SerializeToString,
            protos_dot_doormanager__pb2.TestReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UnlockDoor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/doormanager.DoorManager/UnlockDoor',
            protos_dot_doormanager__pb2.UnlockDoorRequest.SerializeToString,
            protos_dot_doormanager__pb2.UnlockDoorReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LockDoor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/doormanager.DoorManager/LockDoor',
            protos_dot_doormanager__pb2.LockDoorRequest.SerializeToString,
            protos_dot_doormanager__pb2.LockDoorReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ToggleDoor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/doormanager.DoorManager/ToggleDoor',
            protos_dot_doormanager__pb2.ToggleDoorRequest.SerializeToString,
            protos_dot_doormanager__pb2.ToggleDoorReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDoorState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/doormanager.DoorManager/GetDoorState',
            protos_dot_doormanager__pb2.GetDoorStateRequest.SerializeToString,
            protos_dot_doormanager__pb2.GetDoorStateReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

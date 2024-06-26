# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import chat_pb2 as chat__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in chat_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class ChatOperationsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UserLogin = channel.unary_unary(
                '/ChatOperations/UserLogin',
                request_serializer=chat__pb2.UserLoginRequest.SerializeToString,
                response_deserializer=chat__pb2.OperationResponse.FromString,
                _registered_method=True)
        self.ConnectUser = channel.unary_unary(
                '/ChatOperations/ConnectUser',
                request_serializer=chat__pb2.UserConnectionRequest.SerializeToString,
                response_deserializer=chat__pb2.OperationResponse.FromString,
                _registered_method=True)
        self.DisconnectUser = channel.unary_unary(
                '/ChatOperations/DisconnectUser',
                request_serializer=chat__pb2.UserConnectionRequest.SerializeToString,
                response_deserializer=chat__pb2.OperationResponse.FromString,
                _registered_method=True)
        self.Disconnect = channel.unary_unary(
                '/ChatOperations/Disconnect',
                request_serializer=chat__pb2.UserConnectionRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.SubscribeToGroup = channel.unary_unary(
                '/ChatOperations/SubscribeToGroup',
                request_serializer=chat__pb2.GroupSubscription.SerializeToString,
                response_deserializer=chat__pb2.OperationResponse.FromString,
                _registered_method=True)
        self.SendGroupMessage = channel.unary_unary(
                '/ChatOperations/SendGroupMessage',
                request_serializer=chat__pb2.ChatMessageRequest.SerializeToString,
                response_deserializer=chat__pb2.OperationResponse.FromString,
                _registered_method=True)
        self.DiscoverUsers = channel.unary_unary(
                '/ChatOperations/DiscoverUsers',
                request_serializer=chat__pb2.UserLoginRequest.SerializeToString,
                response_deserializer=chat__pb2.OperationResponse.FromString,
                _registered_method=True)


class ChatOperationsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def UserLogin(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConnectUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DisconnectUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Disconnect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeToGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendGroupMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DiscoverUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatOperationsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UserLogin': grpc.unary_unary_rpc_method_handler(
                    servicer.UserLogin,
                    request_deserializer=chat__pb2.UserLoginRequest.FromString,
                    response_serializer=chat__pb2.OperationResponse.SerializeToString,
            ),
            'ConnectUser': grpc.unary_unary_rpc_method_handler(
                    servicer.ConnectUser,
                    request_deserializer=chat__pb2.UserConnectionRequest.FromString,
                    response_serializer=chat__pb2.OperationResponse.SerializeToString,
            ),
            'DisconnectUser': grpc.unary_unary_rpc_method_handler(
                    servicer.DisconnectUser,
                    request_deserializer=chat__pb2.UserConnectionRequest.FromString,
                    response_serializer=chat__pb2.OperationResponse.SerializeToString,
            ),
            'Disconnect': grpc.unary_unary_rpc_method_handler(
                    servicer.Disconnect,
                    request_deserializer=chat__pb2.UserConnectionRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'SubscribeToGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.SubscribeToGroup,
                    request_deserializer=chat__pb2.GroupSubscription.FromString,
                    response_serializer=chat__pb2.OperationResponse.SerializeToString,
            ),
            'SendGroupMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendGroupMessage,
                    request_deserializer=chat__pb2.ChatMessageRequest.FromString,
                    response_serializer=chat__pb2.OperationResponse.SerializeToString,
            ),
            'DiscoverUsers': grpc.unary_unary_rpc_method_handler(
                    servicer.DiscoverUsers,
                    request_deserializer=chat__pb2.UserLoginRequest.FromString,
                    response_serializer=chat__pb2.OperationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ChatOperations', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('ChatOperations', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ChatOperations(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def UserLogin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ChatOperations/UserLogin',
            chat__pb2.UserLoginRequest.SerializeToString,
            chat__pb2.OperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ConnectUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ChatOperations/ConnectUser',
            chat__pb2.UserConnectionRequest.SerializeToString,
            chat__pb2.OperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DisconnectUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ChatOperations/DisconnectUser',
            chat__pb2.UserConnectionRequest.SerializeToString,
            chat__pb2.OperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Disconnect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ChatOperations/Disconnect',
            chat__pb2.UserConnectionRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SubscribeToGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ChatOperations/SubscribeToGroup',
            chat__pb2.GroupSubscription.SerializeToString,
            chat__pb2.OperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SendGroupMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ChatOperations/SendGroupMessage',
            chat__pb2.ChatMessageRequest.SerializeToString,
            chat__pb2.OperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DiscoverUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ChatOperations/DiscoverUsers',
            chat__pb2.UserLoginRequest.SerializeToString,
            chat__pb2.OperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class ClientOperationsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ReceiveChatMessage = channel.unary_unary(
                '/ClientOperations/ReceiveChatMessage',
                request_serializer=chat__pb2.ChatMessageRequest.SerializeToString,
                response_deserializer=chat__pb2.OperationResponse.FromString,
                _registered_method=True)


class ClientOperationsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ReceiveChatMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientOperationsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ReceiveChatMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.ReceiveChatMessage,
                    request_deserializer=chat__pb2.ChatMessageRequest.FromString,
                    response_serializer=chat__pb2.OperationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ClientOperations', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('ClientOperations', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ClientOperations(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ReceiveChatMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ClientOperations/ReceiveChatMessage',
            chat__pb2.ChatMessageRequest.SerializeToString,
            chat__pb2.OperationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

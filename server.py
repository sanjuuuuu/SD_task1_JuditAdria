import grpc
import chat_pb2
import chat_pb2_grpc
import redis
from concurrent import futures
import time
import pika
import google

class ChatOperationsService(chat_pb2_grpc.ChatOperationsServicer):
    def __init__(self):
        self.name_server = UserDirectory()
        self.message_broker = MessagingService()

    def UserLogin(self, request, context):
        user_name = request.user_name
        if self.name_server.is_registered(user_name):
            print(f"User {user_name} has logged in!")
            address = self.name_server.get_user_address(user_name)
            ip, port = address.split(':')
            self.name_server.update_user_status(user_name, False)
            return chat_pb2.OperationResponse(is_success=True, msg="Welcome!", ip_address=ip, port_number=int(port))
        else:
            return chat_pb2.OperationResponse(is_success=False, msg="Not registered!")

    def ConnectUser(self, request, context):
        user_name = request.user_name
        chat_id = request.chat_id
        if self.name_server.is_user_connected(chat_id):
            return chat_pb2.OperationResponse(is_success=False, msg="User already connected!")
        else:
            address = self.name_server.get_user_address(chat_id)
            if address:
                self.name_server.update_user_status(chat_id, True)
                ip, port = address.split(':')
                return chat_pb2.OperationResponse(is_success=True, msg="Connection established!", ip_address=ip, port_number=int(port))
            else:
                return chat_pb2.OperationResponse(is_success=False, msg="Client information not found!")

    def DisconnectUser(self, request, context):
        chat_id = request.chat_id
        if not self.name_server.is_user_connected(chat_id):
            return chat_pb2.OperationResponse(is_success=True)
        else:
            return chat_pb2.OperationResponse(is_success=False)

    def Disconnect(self, request, context):
        user_name = request.user_name
        chat_id = request.chat_id
        self.name_server.update_user_status(user_name, False)
        self.name_server.update_user_status(chat_id, False)
        return google.protobuf.empty_pb2.Empty()

    def DiscoverUsers(self, request, context):
        connected_users = self.name_server.get_all_connected_users()
        for user in connected_users:
            address = self.name_server.get_user_address(user)
            message = f"{user}:{address}"
            self.message_broker.publish(message)
        return chat_pb2.OperationResponse(is_success=True)


class UserDirectory:
    def __init__(self):
        try:
            self.redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)
            self.redis_client.set("user:Judit", "127.0.0.1:50052")
            self.redis_client.set("user:Adria", "127.0.0.1:50053")
            self.redis_client.set("user:Marc", "127.0.0.1:50054")
            self.redis_client.set("user:Pepe", "127.0.0.1:50055")
        except Exception as e:
            print(e)

    def is_registered(self, user_name):
        return self.redis_client.exists(f"user:{user_name}")

    def get_user_address(self, user_name):
        return self.redis_client.get(f"user:{user_name}")

    def update_user_status(self, user_name, status):
        status_str = "connected" if status else "disconnected"
        self.redis_client.set(f"user:{user_name}:status", status_str)

    def is_user_connected(self, user_name):
        status_str = self.redis_client.get(f"user:{user_name}:status")
        return status_str == "connected"

    def get_all_connected_users(self):
        connected_users = []
        for key in self.redis_client.keys("user:*:status"):
            user_name = key.split(":")[1]
            if self.is_user_connected(user_name):
                connected_users.append(user_name)
        return connected_users

class MessagingService:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='group_chat', exchange_type='fanout')

    def publish(self, message):
        self.channel.basic_publish(exchange='group_chat', routing_key='', body=message)


def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatOperationsServicer_to_server(ChatOperationsService(), server)
    print('Server is starting on port 50051.')
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    start_server()
import grpc
import chat_pb2
import chat_pb2_grpc
import pika
from concurrent import futures
import threading
import time

class ClientOperationsService(chat_pb2_grpc.ClientOperationsServicer):
    def __init__(self, user_name):
        self.user_name = user_name
        self.server_channel = grpc.insecure_channel('localhost:50051')
        self.server_stub = chat_pb2_grpc.ChatOperationsStub(self.server_channel)
        self.ip = None
        self.port = None
        self.user_channel = None
        self.user_stub = None
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None
        self.rabbitmq_exchange = None
        self.stop_thread = threading.Event()
        self.stop_discovery_thread = threading.Event()

    def user_login(self):
        request = chat_pb2.UserLoginRequest(user_name=self.user_name)
        try:
            response = self.server_stub.UserLogin(request)
            if response.is_success:
                print(f"{response.msg}: {response.ip_address}:{response.port_number}")
                self.ip = response.ip_address
                self.port = response.port_number
                return response.port_number
            else:
                print(f"{response.msg}")
        except grpc.RpcError as e:
            print(f"gRPC Error: {e}")
            return None

    def connect_to_chat(self, chat_id):
        request = chat_pb2.UserConnectionRequest(user_name=self.user_name, chat_id=chat_id)
        try:
            response = self.server_stub.ConnectUser(request)
            if response.is_success:
                print(f"\tCHAT {chat_id}")
                print(f"{response.msg}")
                self.user_channel = grpc.insecure_channel(f'{response.ip_address}:{response.port_number}')
                self.user_stub = chat_pb2_grpc.ClientOperationsStub(self.user_channel)
                return True
            else:
                print(f'{response.msg}')
                return False
        except grpc.RpcError as e:
            print(f"gRPC Error: {e}")

    def send_chat_message(self, chat_id, message):
        request = chat_pb2.ChatMessageRequest(from_user=self.user_name, chat_message=message)
        try:
            response = self.user_stub.ReceiveChatMessage(request)
            if not response.is_success:
                print("Recipient is not connected to the chat.")
        except grpc.RpcError as e:
            print(f"gRPC Error: {e}")

    def ReceiveChatMessage(self, request, context):
        print(f"{request.from_user}: {request.chat_message}")
        return chat_pb2.OperationResponse(is_success=True)

    def start_client(self, client, port, chat_id):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        chat_pb2_grpc.add_ClientOperationsServicer_to_server(client, self.server)
        self.server.add_insecure_port(f'[::]:{port}')
        self.server.start()
        print("Type 'exit' to leave.")
        while True:
            message = input("")
            if message.lower() == "exit":
                request = chat_pb2.UserConnectionRequest(user_name=self.user_name, chat_id=chat_id)
                self.server_stub.Disconnect(request)
                break
            client.send_chat_message(chat_id, message)
            request = chat_pb2.UserConnectionRequest(user_name=self.user_name, chat_id=chat_id)
            response = self.server_stub.DisconnectUser(request)
            if response.is_success:
                break
        self.server.stop(0)

    def setup_rabbitmq(self, chat_id):
        try:
            self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.rabbitmq_channel = self.rabbitmq_connection.channel()
            self.rabbitmq_exchange = chat_id
            self.rabbitmq_channel.exchange_declare(exchange=self.rabbitmq_exchange, exchange_type='fanout')
        except pika.exceptions.AMQPError as e:
            print(f"RabbitMQ Error: {e}")

    def subscribe_to_group_chat(self, chat_id):
        self.setup_rabbitmq(chat_id)
        self.listener_thread = threading.Thread(target=self.listen_for_messages, args=(chat_id,))
        self.listener_thread.start()

    def listen_for_messages(self, chat_id):
        if self.rabbitmq_connection:
            result = self.rabbitmq_channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            self.rabbitmq_channel.queue_bind(exchange=self.rabbitmq_exchange, queue=queue_name)

            def callback(ch, method, properties, body):
                message = body.decode('utf-8')
                print(f"{message}")

            self.rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            print(f"Subscribed to {chat_id}. Waiting for messages...")
            while not self.stop_thread.is_set():
                self.rabbitmq_channel.connection.process_data_events()
        else:
            print("Failed to connect to RabbitMQ.")

    def send_group_message(self, chat_id):
        if not self.rabbitmq_connection:
            print("Failed to connect to RabbitMQ")
            return
        while True:
            message = input("")
            if message.lower() == "exit":
                print("Closing connection...")
                self.stop_thread.set()
                break
            message = f"{self.user_name}: {message}"
            self.rabbitmq_channel.basic_publish(exchange=self.rabbitmq_exchange, routing_key='', body=message.encode('utf-8'))
        self.rabbitmq_connection.close()

    def discover_chats(self):
        self.setup_rabbitmq('discovery')
        self.publish_discovery_event()
        self.discovery_thread = threading.Thread(target=self.listen_for_discovery)
        self.discovery_thread.start()
        self.stop_discovery_thread.wait()

    def publish_discovery_event(self):
        self.rabbitmq_channel.exchange_declare(exchange='discovery', exchange_type='fanout')
        discovery_message = f"{self.user_name}: {self.ip}:{self.port}"
        self.rabbitmq_channel.basic_publish(exchange='discovery', routing_key='', body=discovery_message.encode('utf-8'))
        request = chat_pb2.UserLoginRequest(user_name=self.user_name)
        self.server_stub.DiscoverUsers(request)

    def listen_for_discovery(self):
        result = self.rabbitmq_channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.rabbitmq_channel.queue_bind(exchange='discovery', queue=queue_name)

        def callback(ch, method, properties, body):
            response = body.decode('utf-8')
            users = response.split('\n')
            print("Active chats:")
            for user in users:
                print(user)
            self.stop_discovery_thread.set()

        self.rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        while not self.stop_discovery_thread.is_set():
            self.rabbitmq_channel.connection.process_data_events()

    def setup_rabbitmq_queue(self, queue_name):
        try:
            self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.rabbitmq_channel = self.rabbitmq_connection.channel()
            self.rabbitmq_channel.queue_declare(queue=queue_name, durable=True)  # Ensure durable is True
        except pika.exceptions.AMQPError as e:
            print(f"RabbitMQ Error: {e}")

    def subscribe_to_insult_queue(self, queue_name):
        self.setup_rabbitmq_queue(queue_name)
        self.insult_thread = threading.Thread(target=self.listen_for_insults, args=(queue_name,))
        self.insult_thread.start()

    def listen_for_insults(self, queue_name):
        if self.rabbitmq_connection:
            def callback(ch, method, properties, body):
                message = body.decode('utf-8')
                print(f"{message}")

            self.rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            while not self.stop_thread.is_set():
                self.rabbitmq_channel.connection.process_data_events()
        else:
            print("Failed to connect")

    def send_insult(self, queue_name):
        if not self.rabbitmq_connection:
            print("Failed to connect")
            return
        while True:
            message = input("")
            if message.lower() == "exit":
                print("Closing connection...")
                self.stop_thread.set()
                break
            message = f"{self.user_name}: {message}"
            self.rabbitmq_channel.basic_publish(exchange='', routing_key=queue_name, body=message.encode('utf-8'))
        self.rabbitmq_connection.close()


if __name__ == "__main__":
    user_name = input("Login: ")
    client = ClientOperationsService(user_name)
    port = client.user_login()
    client.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    client.rabbitmq_channel = client.rabbitmq_connection.channel()
    if port:
        while True:
            print("\n1. Connect to Chat")
            print("2. Subscribe to Group")
            print("3. Discover Chats")
            print("4. Insult Channel")
            choice = input("Select an option: ")

            if choice == "1":
                chat_id = input("Chat ID to connect to: ")
                if client.connect_to_chat(chat_id):
                    client.start_client(client, port, chat_id)
            elif choice == "2":
                chat_id = input("Group ID to subscribe to: ")
                client.subscribe_to_group_chat(chat_id)
                client.send_group_message(chat_id)
            elif choice == "3":
                client.discover_chats()
            elif choice == "4":
                queue_name = "insult_channel"
                client.subscribe_to_insult_queue(queue_name)
                client.send_insult(queue_name)
            else:
                print("Invalid option. Try again.")
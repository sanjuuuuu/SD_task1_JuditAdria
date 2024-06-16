from concurrent import futures
import grpc
import chat_pb2
import chat_pb2_grpc
import pika
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
        self.rabbitmq_exchange = None
        self.stop_event = threading.Event()
        self.listener_threads = []

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
                return None
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
            return False

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
        try:
            while True:
                message = input("")
                if message.lower() == "exit":
                    request = chat_pb2.UserConnectionRequest(user_name=self.user_name, chat_id=chat_id)
                    self.server_stub.Disconnect(request)
                    break
                client.send_chat_message(chat_id, message)
        except KeyboardInterrupt:
            pass
        finally:
            self.server.stop(0)

    def setup_rabbitmq(self, exchange_name):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        self.rabbitmq_exchange = exchange_name
        channel.exchange_declare(exchange=self.rabbitmq_exchange, exchange_type='fanout')
        return connection, channel

    def subscribe_to_group_chat(self, chat_id):
        connection, channel = self.setup_rabbitmq(chat_id)
        listener_thread = threading.Thread(target=self.listen_for_messages, args=(connection, channel, chat_id,))
        listener_thread.start()
        self.listener_threads.append(listener_thread)

    def listen_for_messages(self, connection, channel, chat_id):
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=self.rabbitmq_exchange, queue=queue_name)

        def callback(ch, method, properties, body):
            message = body.decode('utf-8')
            print(f"{message}")

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f"Subscribed to {chat_id}. Waiting for messages...")
        try:
            while not self.stop_event.is_set():
                connection.process_data_events(time_limit=1)
        except Exception as e:
            print(f"Error in listen_for_messages: {e}")
        finally:
            if connection.is_open:
                connection.close()

    def send_group_message(self, chat_id):
        connection, channel = self.setup_rabbitmq(chat_id)
        try:
            while True:
                message = input("")
                if message.lower() == "exit":
                    print("Closing connection...")
                    break
                message = f"{self.user_name}: {message}"
                channel.basic_publish(exchange=self.rabbitmq_exchange, routing_key='', body=message.encode('utf-8'))
        except KeyboardInterrupt:
            pass
        finally:
            if connection.is_open:
                connection.close()

    def discover_chats(self):
        connection, channel = self.setup_rabbitmq('discovery')
        self.publish_discovery_event(channel)
        listener_thread = threading.Thread(target=self.listen_for_discovery, args=(connection, channel,))
        listener_thread.start()
        self.listener_threads.append(listener_thread)
        time.sleep(5)  # Wait for responses
        self.stop_event.set()  # Signal the listener thread to stop
        listener_thread.join()  # Wait for the listener thread to finish
        if connection.is_open:
            connection.close()

    def publish_discovery_event(self, channel):
        channel.exchange_declare(exchange='discovery', exchange_type='fanout')
        discovery_message = f"{self.user_name}: {self.ip}:{self.port}"
        channel.basic_publish(exchange='discovery', routing_key='', body=discovery_message.encode('utf-8'))
        request = chat_pb2.UserLoginRequest(user_name=self.user_name)
        self.server_stub.DiscoverUsers(request)

    def listen_for_discovery(self, connection, channel):
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='discovery', queue=queue_name)

        def callback(ch, method, properties, body):
            response = body.decode('utf-8')
            print("Active chats:")
            print(response)

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print("Waiting for discovery messages...")
        try:
            while not self.stop_event.is_set():
                connection.process_data_events(time_limit=1)
        except Exception as e:
            print(f"Error in listen_for_discovery: {e}")
        finally:
            if connection.is_open:
                connection.close()

    def setup_rabbitmq_queue(self, queue_name):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        return connection, channel

    def subscribe_to_insult_queue(self, queue_name):
        connection, channel = self.setup_rabbitmq_queue(queue_name)
        insult_thread = threading.Thread(target=self.listen_for_insults, args=(connection, channel, queue_name,))
        insult_thread.start()
        self.listener_threads.append(insult_thread)

    def listen_for_insults(self, connection, channel, queue_name):
        def callback(ch, method, properties, body):
            message = body.decode('utf-8')
            print(f"{message}")

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        try:
            while True:
                connection.process_data_events(time_limit=1)
        except KeyboardInterrupt:
            pass
        finally:
            if connection.is_open:
                connection.close()

    def send_insult(self, queue_name):
        connection, channel = self.setup_rabbitmq_queue(queue_name)
        try:
            while True:
                message = input("")
                if message.lower() == "exit":
                    print("Closing connection...")
                    break
                message = f"{self.user_name}: {message}"
                channel.basic_publish(exchange='', routing_key=queue_name, body=message.encode('utf-8'))
        except KeyboardInterrupt:
            pass
        finally:
            if connection.is_open:
                connection.close()

    def cleanup(self):
        # Clean up all threads
        self.stop_event.set()
        for thread in self.listener_threads:
            thread.join()

if __name__ == "__main__":
    user_name = input("Login: ")
    client = ClientOperationsService(user_name)
    port = client.user_login()
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
                queue_name = "insults"
                print(f"Subscribed to {queue_name} channel. Waiting for insults...")
                client.subscribe_to_insult_queue(queue_name)
                client.send_insult(queue_name)
            else:
                print("Invalid choice. Please select a valid option.")
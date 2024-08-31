import socket
import threading
import json

class PubSubServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.topics = {}
        self.running = True

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_socket.settimeout(1)  # Set a timeout for socket.accept()
        print(f"Server listening on {self.host}:{self.port}")
        try:
            while self.running:
                try:
                    client_socket, addr = self.server_socket.accept()
                    print(f"New connection from {addr}")
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                    client_thread.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\nShutting down the server...")
        finally:
            self.shutdown()

    def handle_client(self, client_socket):
        self.clients[client_socket] = set()
        while self.running:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                message = json.loads(data)
                if message['action'] == 'subscribe':
                    self.subscribe(client_socket, message['topic'])
                elif message['action'] == 'publish':
                    self.publish(client_socket, message['topic'], message['content'])
            except json.JSONDecodeError:
                print("Invalid JSON received")
            except Exception as e:
                print(f"Error handling client: {e}")
                break
        self.disconnect_client(client_socket)

    def subscribe(self, client_socket, topic):
        if topic not in self.topics:
            self.topics[topic] = set()
        self.topics[topic].add(client_socket)
        self.clients[client_socket].add(topic)
        print(f"Client subscribed to topic: {topic}")

    def publish(self, sender_socket, topic, content):
        if topic in self.topics:
            message = json.dumps({'topic': topic, 'content': content})
            for client in self.topics[topic]:
                if client != sender_socket:  # Don't send the message back to the sender
                    try:
                        client.send(message.encode('utf-8'))
                    except Exception as e:
                        print(f"Error sending message to client: {e}")
                        self.disconnect_client(client)
        print(f"Message published to topic: {topic}")

    def disconnect_client(self, client_socket):
        for topic in self.clients[client_socket]:
            self.topics[topic].remove(client_socket)
            if not self.topics[topic]:
                del self.topics[topic]
        del self.clients[client_socket]
        client_socket.close()
        print("Client disconnected")

    def shutdown(self):
        self.running = False
        for client_socket in list(self.clients.keys()):
            self.disconnect_client(client_socket)
        self.server_socket.close()
        print("Server shut down")

def run_server():
    server = PubSubServer()
    server.start()

if __name__ == "__main__":
    run_server()
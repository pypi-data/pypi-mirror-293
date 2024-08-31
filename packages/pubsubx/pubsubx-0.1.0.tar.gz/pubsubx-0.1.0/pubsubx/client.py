import socket
import threading
import json

class PubSubClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.receive_thread = None
        self.on_message_callback = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.running = True
        self.receive_thread = threading.Thread(target=self._receive_messages)
        self.receive_thread.start()
        print(f"Connected to server at {self.host}:{self.port}")

    def disconnect(self):
        self.running = False
        if self.socket:
            self.socket.close()
        if self.receive_thread:
            self.receive_thread.join()
        print("Disconnected from server")

    def subscribe(self, topic):
        message = json.dumps({'action': 'subscribe', 'topic': topic})
        self._send_message(message)
        print(f"Subscribed to topic: {topic}")

    def publish(self, topic, content):
        message = json.dumps({'action': 'publish', 'topic': topic, 'content': content})
        self._send_message(message)
        print(f"Published message to topic: {topic}")

    def on_message(self, callback):
        self.on_message_callback = callback

    def _send_message(self, message):
        if self.socket:
            self.socket.send(message.encode('utf-8'))
        else:
            print("Not connected to server")

    def _receive_messages(self):
        self.socket.settimeout(1)  # Set a timeout for socket.recv()
        while self.running:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if not data:
                    break
                message = json.loads(data)
                if self.on_message_callback:
                    self.on_message_callback(message['topic'], message['content'])
                else:
                    print(f"Received message on topic '{message['topic']}': {message['content']}")
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

        self.disconnect()
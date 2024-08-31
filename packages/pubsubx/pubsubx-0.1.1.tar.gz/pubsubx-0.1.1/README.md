# pubsubx

pubsubx is a lightweight publish-subscribe messaging system implemented in Python. It provides a simple server and client for building distributed messaging applications.

## Installation

You can install pubsubx using pip:

```
pip install pubsubx
```

## Usage

### Starting the server

To start the pubsubx server:

```python
from pubsubx import PubSubServer

server = PubSubServer()
server.start()
```

### Using the client

Here's a simple example of how to use the pubsubx client:

```python
from pubsubx import PubSubClient
import time

def on_message(topic, message):
    print(f"Received message on topic '{topic}': {message}")

# Create and connect the client
client = PubSubClient()
client.connect()

# Set up the message callback
client.on_message(on_message)

# Subscribe to a topic
client.subscribe("test_topic")

# Publish a message
client.publish("test_topic", "Hello, pubsubx!")

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnecting...")
    client.disconnect()
```

## License

This project is licensed under the MIT License.
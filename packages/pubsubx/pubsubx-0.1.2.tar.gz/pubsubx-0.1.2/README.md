# PubSubX

PubSubX is a lightweight publish-subscribe messaging system implemented in Python. It provides a simple server and client for building distributed messaging applications.

## Installation

You can install PubSubX using pip:

```
pip install pubsubx
```

## Usage

### Starting the server

There are multiple ways to start the PubSubX server:

1. As a module:
   ```
   python -m pubsubx [--host HOST] [--port PORT]
   ```

2. Using the console script:
   ```
   pubsubx [--host HOST] [--port PORT]
   ```

3. In your Python code:
   ```python
   from pubsubx import PubSubServer

   server = PubSubServer(host='localhost', port=5000)
   server.start()
   ```

The default host is 'localhost' and the default port is 5000.

### Using the client

Here's a simple example of how to use the PubSubX client:

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
client.publish("test_topic", "Hello, PubSubX!")

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
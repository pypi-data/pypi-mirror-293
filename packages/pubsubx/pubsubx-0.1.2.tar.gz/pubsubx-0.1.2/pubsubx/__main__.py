import argparse
from .server import PubSubServer

def main():
    parser = argparse.ArgumentParser(description="Run the PubSubX server")
    parser.add_argument("--host", default="localhost", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind the server to")
    args = parser.parse_args()

    server = PubSubServer(host=args.host, port=args.port)
    server.start()

if __name__ == "__main__":
    main()

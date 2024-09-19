import asyncio
import websockets
from websockets.http import Headers
from websockets import WebSocketServerProtocol
from flask import Flask
from flask_cors import CORS
import logging

logging.basicConfig(filename='websocket_server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "WebSocket with CORS enabled"

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Allow only frontend URL

# WebSocket handler function
async def handler(websocket: WebSocketServerProtocol, path: str):
    """Handle incoming WebSocket messages and send responses."""
    logging.info(f"Client connected: {path}")
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            await websocket.send(f"Echo: {message}")  # Echo back the received message
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        logging.info("Client disconnected")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 5000):
        logging.info("Server started on ws://0.0.0.0:5000") # Updated port
        await asyncio.Future()  # Run forever

# Wrap handler with CORS headers
async def cors_handler(websocket: WebSocketServerProtocol, path: str):
    """Wrap the handler to handle CORS if needed."""
    # Allow all origins (wildcard '*') - For production, restrict this to your domain.
    if 'Origin' in websocket.request_headers:
        origin = websocket.request_headers['Origin']
        print(f"Connection from origin: {origin}")
    # websocket.request_headers['Origin'] = '*'
    await handler(websocket, path)

if __name__ == '__main__':
    asyncio.run(main())

# Start WebSocket server on localhost:5000
start_server = websockets.serve(cors_handler, "0.0.0.0", 5000)

# Run the server forever
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
import asyncio
import websockets
import json
import boto3
from pydub import AudioSegment
from pydub.utils import which
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AudioSegment.converter = which("ffmpeg")

async def handler(websocket, path):
    logging.info(f"Client connected: {path}")
    try:
        async for message in websocket:
            logging.info(f"Received message: {message}")
            await websocket.send(f"Echo: {message}")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        logging.info("Client disconnected")

async def main():
    server = await websockets.serve(handler, "0.0.0.0", 5000)
    logging.info("Server started on ws://0.0.0.0:5000")
    await asyncio.Future()  # Run forever


# AWS Transcribe settings
transcribe = boto3.client('transcribe', region_name='us-east-1')

async def process_audio(websocket, path):
    async for message in websocket:
        audio_data = json.loads(message)['data']
        # Handle live transcription here using AWS Transcribe streaming service
        print("Received audio data:", audio_data)

        # Just echo the received message for now (modify for actual transcription)
        await websocket.send("Transcription: " + "Your message here")

start_server = websockets.serve(process_audio, "localhost", 5000)

if __name__ == "__main__":
    asyncio.run(main())

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server running on ws://localhost:5000")
asyncio.get_event_loop().run_forever()
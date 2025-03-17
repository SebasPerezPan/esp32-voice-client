import asyncio
import websockets

HOST = "0.0.0.0"  # Escucha en todas las interfaces
PORT = 8765
FILE_PATH = "received.wav"

async def receive_audio(websocket, path):
    print("Client connected")
    with open(FILE_PATH, "wb") as f:
        while True:
            data = await websocket.recv()
            if data == "EOF":
                break
            f.write(data)
    print("File received successfully")

async def main():
    server = await websockets.serve(receive_audio, HOST, PORT)
    print(f"Server started on {HOST}:{PORT}")
    await server.wait_closed()

asyncio.run(main())

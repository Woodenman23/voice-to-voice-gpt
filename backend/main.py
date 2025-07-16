from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import json
from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from audio.translation import audio_to_text, text_to_audio, play_audio
from llm.prompt import send_prompt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Listen for voice input
            prompt = audio_to_text()
            if prompt == "":
                continue


            # Get AI response
            response = send_prompt(prompt)

            # Send AI response to frontend
            await manager.send_personal_message(
                json.dumps(
                    {
                        "type": "ai_response",
                        "text": response,
                        "timestamp": asyncio.get_event_loop().time(),
                    }
                ),
                websocket,
            )

            # Generate and play audio
            audio_response = text_to_audio(response)
            if audio_response:
                # Signal audio start
                await manager.send_personal_message(
                    json.dumps(
                        {
                            "type": "audio_start",
                            "timestamp": asyncio.get_event_loop().time(),
                        }
                    ),
                    websocket,
                )

                play_audio(audio_response)

                # Signal audio end
                await manager.send_personal_message(
                    json.dumps(
                        {
                            "type": "audio_end",
                            "timestamp": asyncio.get_event_loop().time(),
                        }
                    ),
                    websocket,
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

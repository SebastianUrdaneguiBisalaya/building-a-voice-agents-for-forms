from typing import Any, Dict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn)


class FormSession:
    def __init__(self, questions: list[dict]):
        self.current_index = 0
        self.questions = questions
        self.answers = Dict[str, Any] = {}
        self.completed = False

    def current_question(self) -> dict:
        return self.questions[self.current_index]

    def record_answer(self, key: str, value: Any):
        self.answers[key] = value
        self.current_index += 1
        if self.current_index >= len(self.questions):
            self.completed = True


manager = ConnectionManager()

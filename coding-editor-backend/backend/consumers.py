import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "WebSocket connected!"}))

    async def disconnect(self, close_code):
        print("WebSocket disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")
        await self.send(text_data=json.dumps({"response": f"You said: {message}"}))
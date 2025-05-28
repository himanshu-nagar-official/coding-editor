import asyncio
import json
import tempfile
import threading
from channels.generic.websocket import AsyncWebsocketConsumer
import subprocess

class CodeRunnerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.loop = asyncio.get_event_loop()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        code = data.get("code", "")

        # Run code in a separate thread so it doesn't block the event loop
        threading.Thread(target=self.run_code_in_docker, args=(code,)).start()

    def run_code_in_docker(self, code):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.py') as tmp:
            tmp.write(code)
            tmp.flush()
            tmp_path = tmp.name

        volume_mapping = f"{tmp_path}:/app/script.py:ro"

        try:
            result = subprocess.run(
                ["docker", "run", "--rm", "-v", volume_mapping, "code-runner"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = result.stdout + result.stderr
        except Exception as e:
            output = f"Error running Docker: {str(e)}"

        # Send the output back to the WebSocket safely
        asyncio.run_coroutine_threadsafe(self.send_output(output), self.loop)

    async def send_output(self, output):
        await self.send(text_data=json.dumps({
            "output": output
        }))
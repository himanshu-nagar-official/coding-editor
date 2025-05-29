import json
import os
import tempfile
import subprocess
from channels.generic.websocket import AsyncWebsocketConsumer

class CodeRunnerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        code = data.get("code", "")
        user_input = data.get("userInput", "")
        await self.run_code_in_docker(code, user_input)

    async def run_code_in_docker(self, code, user_input=""):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                script_path = os.path.join(temp_dir, "script.py")
                with open(script_path, "w") as f:
                    f.write(code)

                command = [
                    "docker", "run", "--rm", "-i",
                    "-v", f"{temp_dir}:/app",
                    "python:3.10-slim",
                    "python", "/app/script.py"
                ]

                # Send user input to stdin and get combined stdout+stderr
                result = subprocess.run(
                    command,
                    input=user_input.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

                output = result.stdout.decode() + result.stderr.decode()
                await self.send(text_data=json.dumps({"output": output}))

        except Exception as e:
            await self.send(text_data=json.dumps({"output": f"Error: {str(e)}"}))
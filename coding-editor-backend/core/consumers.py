import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from concurrent.futures import ThreadPoolExecutor
import tempfile
import os
import subprocess

executor = ThreadPoolExecutor()

class CodeRunnerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"output": "Connected to CodeRunner backend.\n"}))
        self.proc = None

    async def disconnect(self, close_code):
        if self.proc:
            self.proc.kill()

    async def receive(self, text_data):
        data = json.loads(text_data)
        code = data.get("code", "")
        input_text = data.get("input", "")

        if self.proc and not self.proc.stdin.closed:
            # send input to running process stdin
            self.proc.stdin.write(input_text.encode() + b"\n")
            await self.proc.stdin.drain()
            return

        # Run new code
        await self.run_code_in_docker(code)

    async def run_code_in_docker(self, code):
        # Save code to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
            tmp_file.write(code.encode())
            tmp_file.flush()
            tmp_filename = tmp_file.name

        # Docker command to run python inside container with temp file mounted
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{os.path.dirname(tmp_filename)}:/code",
            "python:3.11-slim",
            "python", f"/code/{os.path.basename(tmp_filename)}"
        ]

        loop = asyncio.get_running_loop()
        self.proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        await self.send(text_data=json.dumps({"output": "Running code inside Docker container...\n"}))

        # Stream stdout and stderr
        try:
            while True:
                line = await self.proc.stdout.readline()
                if line:
                    await self.send(text_data=json.dumps({"output": line.decode()}))
                else:
                    break
            err = await self.proc.stderr.read()
            if err:
                await self.send(text_data=json.dumps({"output": err.decode()}))
        finally:
            os.unlink(tmp_filename)
            self.proc = None
            await self.send(text_data=json.dumps({"output": "\nExecution finished.\n"}))
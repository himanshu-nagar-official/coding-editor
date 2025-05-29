# core/consumers.py
import json
import os
import tempfile
import subprocess
import shutil  # For safely removing the temporary directory later
import uuid  # For creating unique directory names for each run

from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio  # Import asyncio for create_subprocess_exec


class CodeRunnerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        code = data.get("code", "")
        user_input = data.get("userInput", "")  # Make sure your frontend sends "userInput"
        await self.run_code_in_docker(code, user_input)

    async def run_code_in_docker(self, code, user_input=""):
        # This is the path INSIDE your backend container where the shared host directory is mounted.
        # It MUST match the TARGET of the mount in your backend container's 'docker run' command (Prerequisite Step 2).
        base_runs_dir_in_backend = "/app/host_temp_runs"

        # This is the corresponding path ON YOUR HOST machine.
        # It MUST match the SOURCE of the mount in your backend container's 'docker run' command (Prerequisite Step 1).
        base_runs_dir_on_host = "/tmp/my_code_execution_space"  # <<< CHANGE THIS TO YOUR ACTUAL HOST PATH

        # Create a unique subdirectory for this specific run to avoid conflicts and for easy cleanup.
        # This subdirectory will be created INSIDE base_runs_dir_in_backend.
        run_specific_id = str(uuid.uuid4())
        run_temp_dir_in_backend = os.path.join(base_runs_dir_in_backend, run_specific_id)

        # And this is the corresponding path to that unique subdirectory ON THE HOST.
        run_temp_dir_on_host = os.path.join(base_runs_dir_on_host, run_specific_id)

        try:
            # Create the unique temporary directory for this run
            # This directory is physically on the host, but we manage it via its path in the backend container.
            os.makedirs(run_temp_dir_in_backend, exist_ok=True)

            # Path to script.py within this unique, temporary run directory (backend container's view)
            script_path_in_run_dir = os.path.join(run_temp_dir_in_backend, "script.py")

            with open(script_path_in_run_dir, "w", encoding='utf-8') as f:
                f.write(code)

            # The command for the python:3.10-slim container.
            # We mount the 'run_temp_dir_on_host' (which contains script.py) to '/app' inside the new container.
            command = [
                "docker", "run", "--rm", "-i",  # -i is important for sending input via stdin
                "-v", f"{run_temp_dir_on_host}:/app:ro",  # Mount the HOST path to /app, read-only
                "python:3.10-slim",  # The image to use
                "python", "/app/script.py"  # Command to run (script.py is now at /app/script.py)
            ]

            # For debugging: print the command that will be run
            print(f"Executing Docker command: {' '.join(command)}")
            print(f"Host path being mounted: {run_temp_dir_on_host}")
            print(f"Script content written to: {script_path_in_run_dir}")

            # Use asyncio.create_subprocess_exec for better async handling
            process = await asyncio.create_subprocess_exec(
                *command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            stdout_data, stderr_data = await process.communicate(
                input=user_input.encode('utf-8') if user_input else None
            )

            output = stdout_data.decode(errors='replace')
            error_output = stderr_data.decode(errors='replace')

            combined_output = output + error_output

            # For debugging on the server side:
            print(f"User input sent to subprocess: {user_input!r}")
            print(f"Raw STDOUT from subprocess: {stdout_data!r}")
            print(f"Raw STDERR from subprocess: {stderr_data!r}")
            print(f"Combined output sent to client: {combined_output}")

            await self.send(text_data=json.dumps({"output": combined_output}))

        except FileNotFoundError:
            # This error means the 'docker' command itself was not found.
            # Ensure Docker CLI is installed in your backend container if this happens.
            # (The Dockerfile you showed earlier for the backend *does* install docker-ce-cli)
            print("Error: Docker command not found.")
            await self.send(text_data=json.dumps(
                {"output": "Error: Docker command not found. Is Docker CLI installed in the backend service?"}))
        except Exception as e:
            print(f"An exception occurred in run_code_in_docker: {type(e).__name__} - {str(e)}")
            await self.send(text_data=json.dumps({"output": f"Error: {str(e)}"}))
        finally:
            # Clean up the unique temporary directory created for this run
            if os.path.exists(run_temp_dir_in_backend):
                try:
                    shutil.rmtree(run_temp_dir_in_backend)
                    print(f"Successfully removed temporary run directory: {run_temp_dir_in_backend}")
                except OSError as e_rm:
                    print(f"Error removing temporary run directory {run_temp_dir_in_backend}: {e_rm}")

"""
A simple FastAPI application to handle shell commands and return logs."""
import os
import tempfile
import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
# from dotenv import load_dotenv
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://host.docker.internal",
        "http://localhost:8889",           # Thêm nếu frontend chạy ở port khác
        "http://127.0.0.1:8889",
        "http://host.docker.internal:8889"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/shell/{command}")
async def shell(command: str, background_tasks: BackgroundTasks):
    """Endpoint to return a simple message."""
    background_tasks.add_task(some_background_task, command)
    return {"status": "submitted", "log": f"/shell/{command}/log"}

@app.get("/shell/{command}/log")
async def shell_log(command: str):
    """Endpoint to return the log of a shell command."""
    log_file = os.path.join(tempfile.gettempdir(), f"{command}.log")
    if not os.path.exists(log_file):
        return {"status": "error", "message": "Log file does not exist."}

    with open(log_file, 'r', encoding='utf-8') as file:
        log_content = file.read()

    return {"status": "success", "log": log_content}

def some_background_task(command: str = "echo Hello from background task"):
    """A simple background task."""
    try:
        run_shell_command(command)
    except Exception as e:
        print(f"Error occurred: {e}")

# def run_shell_command(command: str):
#     """Run a shell command."""
#     load_dotenv()
#     if command not in os.environ:
#         return
#     shell_cmd = os.environ[command]
#     log_file = os.path.join(tempfile.gettempdir(), f"{command}.log")
#     print(f"Running command: {shell_cmd} and logging to {log_file}")
#     os.system(f"{shell_cmd} > {log_file} 2>&1")


def run_shell_command(command: str):
    """Run a shell command from environment variable."""
    if command not in os.environ:
        print(f"Command '{command}' not found in environment.")
        return
    shell_cmd = os.environ[command]
    log_file = os.path.join(tempfile.gettempdir(), f"{command}.log")

    print(f"Running: {shell_cmd}, logging to: {log_file}")

    with open(log_file, "w", encoding="utf-8") as f:
        result = subprocess.run(shell_cmd, shell=True, stdout=f, stderr=subprocess.STDOUT, check=True)

    print(f"Command exited with code: {result.returncode}")


def main():
    """Run the FastAPI application."""
    uvicorn.run(app, host="0.0.0.0", port=8889, reload=False, workers=1)

if __name__ == "__main__":
    main()
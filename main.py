import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/shell/{command}")
async def shell(command: str, background_tasks: BackgroundTasks):
    """Endpoint to return a simple message."""
    background_tasks.add_task(some_background_task, command)
    return {"message": f"Executing command: {command}"}

def some_background_task(command: str = "echo Hello from background task"):
    """A simple background task."""
    try:
        run_shell_command(command)
    except Exception as e:
        print(f"Error occurred: {e}")

def run_shell_command(command: str):
    """Run a shell command."""
    load_dotenv()
    if command not in os.environ:
        return
    shell_cmd = os.environ[command]
    os.system(shell_cmd)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8889)
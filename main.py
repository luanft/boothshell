"""
A simple FastAPI application to handle shell commands and return logs."""
import hmac
import os
import re
import tempfile
import subprocess
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
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

# ─── Deploy: cap nhat bo iot len mot version ───────────────────────────────
#
# Khac /shell/{key}: endpoint nay nhan THAM SO tu ben ngoai (version) va chay quyen root,
# nen:
#   - bat buoc header X-Photoshell-Token khop PHOTOSHELL_TOKEN (photoshell nghe 0.0.0.0,
#     ai trong LAN venue / tailnet cung goi duoc). Chua cau hinh token -> tu choi het.
#   - version kiem bang regex (lop thu hai; photoserver va server da kiem truoc);
#   - chay UPDATE_SCRIPT dang argv, KHONG qua shell — version khong bao gio bi shell doc.
# /shell/{key} giu nguyen (khong token) de booth con chay image photoserver cu khong mat
# reboot/shutdown. Khoa no lai khi moi booth da gui token.

VERSION_RE = re.compile(r"\d+\.\d+\.\d+")  # dung fullmatch: `$` cua Python khop ca truoc "\n" cuoi
DEPLOY_LOG = os.path.join(tempfile.gettempdir(), "deploy.log")


class DeployRequest(BaseModel):
    version: str


def _check_token(token):
    expected = os.environ.get("PHOTOSHELL_TOKEN", "")
    if not expected or not token or not hmac.compare_digest(token, expected):
        raise HTTPException(status_code=401, detail="invalid token")


def run_deploy(version: str):
    script = os.environ.get("UPDATE_SCRIPT", "")
    with open(DEPLOY_LOG, "w", encoding="utf-8") as f:
        if not script or not os.access(script, os.X_OK):
            f.write(f"UPDATE_SCRIPT not executable: {script!r}\n")
            return
        result = subprocess.run([script, version], stdout=f, stderr=subprocess.STDOUT, check=False)
        f.write(f"\nexit code: {result.returncode}\n")


@app.post("/deploy")
async def deploy(req: DeployRequest, background_tasks: BackgroundTasks,
                 x_photoshell_token: str = Header(default="")):
    """Chay update.sh <version> o nen. Tra ve NGAY: update.sh recreate container
    photoserver dang goi minh, ket qua that doc qua GET /deploy/log hoac heartbeat."""
    _check_token(x_photoshell_token)
    if not VERSION_RE.fullmatch(req.version):
        raise HTTPException(status_code=400, detail="invalid version")
    background_tasks.add_task(run_deploy, req.version)
    return {"status": "submitted", "version": req.version, "log": "/deploy/log"}


@app.get("/deploy/log")
async def deploy_log(x_photoshell_token: str = Header(default="")):
    _check_token(x_photoshell_token)
    if not os.path.exists(DEPLOY_LOG):
        return {"status": "error", "message": "Log file does not exist."}
    with open(DEPLOY_LOG, "r", encoding="utf-8") as file:
        return {"status": "success", "log": file.read()}


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
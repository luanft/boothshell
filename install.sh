#!/bin/bash
set -e
if ! command -v python3 &>/dev/null; then
  echo "[✘] Python3 is not installed. Please install Python 3.8+ before continuing."
  exit 1
else
  echo "[✔] Found Python: $(python3 --version)"
fi

echo "[+] Installing my-fastapi-service..."
sudo python3 -m venv /opt/.boothshell_env
sudo mkdir -p /opt/boothshell

wget -qO- https://raw.githubusercontent.com/luanft/boothshell/main/commands > /opt/boothshell/.env

echo "[+] Installing Python package..."
/opt/.boothshell_env/bin/python -m pip install --upgrade pip
/opt/.boothshell_env/bin/python -m pip install --upgrade setuptools wheel
/opt/.boothshell_env/bin/python -m pip install git+https://github.com/luanft/boothshell.git


wget -qO- https://raw.githubusercontent.com/luanft/boothshell/main/photoshell.service > /opt/boothshell/photoshell.service
# Enable systemd service (nếu có)
if [ -f "/opt/boothshell/photoshell.service" ]; then
    echo "[+] Copying systemd service..."
    sudo cp /opt/boothshell/photoshell.service /etc/systemd/system/photoshell.service
    sudo systemctl daemon-reexec
    sudo systemctl daemon-reload
    sudo systemctl enable photoshell
    sudo systemctl start photoshell
fi

echo "[✔] Done. Service installed."

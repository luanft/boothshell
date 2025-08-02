#!/bin/bash
set -e

# Kiểm tra Python 3
if ! command -v python3 &>/dev/null; then
  echo "[✘] Python3 is not installed. Please install Python 3.8+ before continuing."
  exit 1
else
  echo "[✔] Found Python: $(python3 --version)"
fi

echo "[+] Installing my-fastapi-service..."
sudo mkdir -p /opt/boothshell
sudo python3 -m venv /opt/.boothshell_env

# Tải file .env
echo "[+] Downloading .env..."
sudo bash -c "curl -fsSL https://raw.githubusercontent.com/luanft/boothshell/main/command > /opt/boothshell/.env"

# Cài đặt Python package
echo "[+] Installing Python package..."
sudo /opt/.boothshell_env/bin/python -m pip install --upgrade pip setuptools wheel
sudo /opt/.boothshell_env/bin/python -m pip install git+https://github.com/luanft/boothshell.git

# Tải systemd service
echo "[+] Downloading systemd service..."
sudo bash -c "curl -fsSL https://raw.githubusercontent.com/luanft/boothshell/main/photoshell.service > /opt/boothshell/photoshell.service"

# Enable systemd service
if [ -f "/opt/boothshell/photoshell.service" ]; then
    echo "[+] Copying systemd service..."
    sudo cp /opt/boothshell/photoshell.service /etc/systemd/system/photoshell.service
    sudo systemctl daemon-reexec
    sudo systemctl daemon-reload
    sudo systemctl enable photoshell
    sudo service photoshell restart
fi

echo "[✔] Done. Service installed."

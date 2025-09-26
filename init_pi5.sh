sudo apt update
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
sudo apt install fonts-noto-core fonts-noto-color-emoji
sudo apt install fonts-nanum fonts-noto-cjk
sudo systemctl stop cups
sudo systemctl stop cups-browsed
sudo systemctl disable cups
sudo systemctl disable cups-browsed
sudo systemctl mask cups
sudo systemctl mask cups-browsed
sudo apt purge cups* -y
sudo apt autoremove -y

curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER

curl -fsSL https://tailscale.com/install.sh | sh

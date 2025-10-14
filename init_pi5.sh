sudo apt update -y 
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs git
sudo apt install fonts-noto-core fonts-noto-color-emoji -y 
sudo apt install fonts-nanum fonts-noto-cjk -y 
sudo systemctl stop cups
sudo systemctl stop cups-browsed
sudo systemctl disable cups
sudo systemctl disable cups-browsed
sudo systemctl mask cups
sudo systemctl mask cups-browsed
sudo apt purge cups* -y
sudo apt autoremove -y
sudo apt install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox  gldriver-test unclutter -y


curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER

curl -fsSL https://tailscale.com/install.sh | sh

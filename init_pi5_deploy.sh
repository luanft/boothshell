sudo apt update -y 
# curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
# sudo apt install -y nodejs git
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
sudo apt install -y libcups2 fuse3 fuse libfuse2 zlib1g zlib1g-dev libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libx11-dev libxtst6 libnss3 libasound2 libxss1 libxrandr2 libatk-bridge2.0-0 libdrm2 libgbm1
sudo apt install --no-install-recommends xserver-xorg x11-xserver-utils xinit gldriver-test unclutter unclutter-xfixes -y
sudo apt update && sudo apt install samba samba-common-bin -y


curl -sSL https://get.docker.com | sh
sudo usermod -aG docker machi
sudo usermod -aG netdev machi

sudo usermod -aG video,input machi

sudo mkdir -p /opt/machi_deployment
sudo chown machi:machi /opt/machi_deployment

touch /opt/machi_deployment/install_wifi.sh
chmod +x /opt/machi_deployment/install_wifi.sh

cat << 'EOF' | tee -a ~/.bash_profile
# Auto-start X server only on the main console (TTY1) if no display is running
if [[ -z $DISPLAY ]] && [[ $(tty) == /dev/tty1 ]]; then
  # Optional small delay (usually 3 seconds is enough)
  bash /opt/machi_deployment/install_wifi.sh &
  sleep 30
  # The 'exec' command replaces the shell process with the X server process, preventing resource leaks
  exec startx
fi
EOF

cat << 'EOF' > ~/.xinitrc
#!/bin/sh

# Disable screen blanking, screensavers, and power management
xset -dpms       # disable power management
xset s off       # disable screen saver
xset s noblank   # don't blank the video device

# Hide the cursor permanently and grab the pointer
unclutter -noevents -grab &
unclutter-xfixes --hide-on-touch --timeout 0 &

HITI_SCRIPT="/opt/machi_deployment/update_hiti_ip.sh"
if [ -f "$HITI_SCRIPT" ]; then
    echo "Running HiTi IP update script..."
    "$HITI_SCRIPT"
fi

# Launch your Electron application in KIOSK mode.
# 'exec' must be the LAST command to run the application efficiently.
exec /opt/machi_deployment/PhotoBoothLite-1.1.0-arm64.AppImage > booth_log.txt 2>&1
EOF

# curl -fsSL https://tailscale.com/install.sh | sh

echo "machi ALL=(ALL) NOPASSWD: /usr/bin/nmcli" | sudo tee /etc/sudoers.d/wifi-privilege > /dev/null
sudo chmod 0440 /etc/sudoers.d/wifi-privilege

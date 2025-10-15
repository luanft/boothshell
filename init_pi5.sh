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
sudo apt install -y libcups2 fuse3 fuse libfuse2 zlib1g zlib1g-dev libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libx11-dev libxtst6 libnss3 libasound2 libxss1 libxrandr2 libatk-bridge2.0-0 libdrm2 libgbm1
sudo apt install --no-install-recommends xserver-xorg x11-xserver-utils xinit gldriver-test unclutter -y


curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER

sudo usermod -aG video,input luant

cat << 'EOF' | tee -a ~/.bash_profile
# Auto-start X server only on the main console (TTY1) if no display is running
if [[ -z $DISPLAY ]] && [[ $(tty) == /dev/tty1 ]]; then
  # Optional small delay (usually 3 seconds is enough)
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

# Launch your Electron application in KIOSK mode.
# 'exec' must be the LAST command to run the application efficiently.
exec /home/luant/app/photobooth/photobooth_ui/dist/PhotoBoothLite-1.1.0-arm64.AppImage > log.txt 2>&1
EOF

curl -fsSL https://tailscale.com/install.sh | sh

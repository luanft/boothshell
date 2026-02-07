#!/bin/bash

FILE="/home/luant/app/photoserver/deployment/resources/wifi.txt"

if [ ! -f "$FILE" ]; then
    echo "Không tìm thấy file $FILE"
    exit 1
fi

# Read line in wifi.txt
while IFS='|' read -r ssid pass || [ -n "$ssid" ]; do
    [[ -z "$ssid" || "$ssid" =~ ^# ]] && continue

    echo "Processing: $ssid"

    # Clean up old wifi configuration
    /usr/bin/sudo /usr/bin/nmcli con delete "$ssid" > /dev/null 2>&1

    if [ -z "$pass" ] || [ "$pass" == "OPEN" ]; then
        # For open wifi
        /usr/bin/sudo /usr/bin/nmcli con add type wifi ifname wlan0 con-name "$ssid" ssid "$ssid" -- wifi-sec.key-mgmt none > /dev/null 2>&1
        echo "--> Added OPEN: $ssid"
    else
        # For secured wifi
        if [ ${#pass} -lt 8 ]; then
            echo "--> Password must longer than 8 characters"
        else
            /usr/bin/sudo /usr/bin/nmcli con add type wifi ifname wlan0 con-name "$ssid" ssid "$ssid" -- wifi-sec.key-mgmt wpa-psk wifi-sec.psk "$pass" > /dev/null 2>&1
            echo "--> Add wifi: $ssid"
        fi
    fi
done < "$FILE"

echo "Update wifi for photobooth"

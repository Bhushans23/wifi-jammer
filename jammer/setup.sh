#!/bin/bash

# Setup script for WiFi Jammer Tool

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

echo "Setting up WiFi Jammer Tool..."

# Install dependencies
echo "Installing required packages..."
apt update
apt install -y aircrack-ng python3 python3-pip

# Make the main script executable
echo "Setting permissions..."
chmod +x wifi_jammer.py

echo "Setup complete!"
echo "Usage: sudo ./wifi_jammer.py -i <interface> [options]"
echo "See README.md for more information." 
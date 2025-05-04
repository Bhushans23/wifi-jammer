# WiFi Jammer Tool - Usage Guide

## Installation and Setup

1. Ensure your Kali Linux environment is ready:
   ```
   chmod +x setup.sh wifi_jammer.py
   sudo ./setup.sh
   ```
   This installs the required dependencies (aircrack-ng, python3) and sets the correct permissions.

## Finding Your Wireless Interface

Before running the tool, identify your wireless interface:
```
iwconfig
```
Look for a wireless interface (usually wlan0, wlan1, etc.)

## Basic Usage

### Scanning Available Networks

To discover networks in range:
```
sudo ./wifi_jammer.py -i wlan0 -s
```
Replace `wlan0` with your actual wireless interface.

Press Ctrl+C to stop scanning.

### Targeting a Specific Network

To jam a specific network:
```
sudo ./wifi_jammer.py -i wlan0 -b 00:11:22:33:44:55 -c 6
```
Where:
- `wlan0` is your wireless interface
- `00:11:22:33:44:55` is the target's BSSID (MAC address)
- `6` is the channel the target network is operating on

### Jamming All Networks

To jam all networks in range (use with caution):
```
sudo ./wifi_jammer.py -i wlan0 -a
```

## Command Line Options

- `-i, --interface`: (Required) Wireless interface to use
- `-c, --channel`: Channel of the target access point
- `-b, --bssid`: BSSID (MAC address) of the target access point
- `-s, --scan`: Scan for available networks
- `-a, --all`: Deauthenticate all networks (use with caution)

## Stopping an Attack

Press Ctrl+C to stop any running attack. The tool will automatically clean up by:
- Stopping monitor mode
- Restarting network services
- Bringing your interface back to normal mode

## Troubleshooting

- **"Operation not permitted"**: Make sure you're running with sudo
- **Adapter not found**: Ensure your wireless adapter supports monitor mode
- **Commands not found**: Make sure aircrack-ng is installed (run setup.sh again)

## Important Reminders

- This tool is for educational purposes only
- Only use on networks you own or have permission to test
- Always run the tool as root (using sudo)
- Your wireless adapter must support monitor mode and packet injection

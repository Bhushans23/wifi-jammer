# WiFi Jammer Tool

A simple WiFi deauthentication tool for Kali Linux that uses the aircrack-ng suite to perform deauthentication attacks.

## Disclaimer

This tool is for **educational purposes only**. Unauthorized jamming of WiFi networks is illegal in most countries. Only use this tool on networks you own or have explicit permission to test.

## Prerequisites

- Kali Linux (or any Linux distribution with aircrack-ng installed)
- Python 3.x
- Aircrack-ng suite
- A wireless adapter that supports monitor mode and packet injection
- Root privileges

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/wifi-jammer.git
cd wifi-jammer
```

2. Make the script executable:
```
chmod +x wifi_jammer.py
```

3. Ensure aircrack-ng is installed:
```
sudo apt update
sudo apt install aircrack-ng
```

## Usage

The tool must be run as root:

```
sudo ./wifi_jammer.py [options]
```

### Options:

- `-i, --interface`: (Required) Wireless interface to use (e.g., wlan0)
- `-c, --channel`: Channel of the target access point
- `-b, --bssid`: BSSID (MAC address) of the target access point
- `-s, --scan`: Scan for available networks
- `-a, --all`: Deauthenticate all networks (use with caution)

### Examples:

1. Scan for available networks:
```
sudo ./wifi_jammer.py -i wlan0 -s
```

2. Deauthenticate a specific access point:
```
sudo ./wifi_jammer.py -i wlan0 -b 00:11:22:33:44:55 -c 6
```

3. Deauthenticate all networks in range:
```
sudo ./wifi_jammer.py -i wlan0 -a
```

## How It Works

1. The tool puts your wireless interface into monitor mode
2. It then sends deauthentication packets to the target access point
3. This forces connected clients to disconnect from the network
4. Press Ctrl+C to stop the attack and return your interface to normal mode

## Troubleshooting

- If you get "Operation not permitted" errors, make sure you're running the script as root
- If your wireless adapter isn't detected, ensure it supports monitor mode
- Some network managers may interfere with the tool; the script tries to disable them temporarily

## Legal Notice

Using this tool to disrupt networks you don't own or have permission to test is illegal and unethical. The author assumes no liability for misuse of this software. 
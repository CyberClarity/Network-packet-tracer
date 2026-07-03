# Network Packet Analysis

## Objective
Learn how to capture and analyze live network traffic at the packet level
using Scapy, and log structured details (source/destination IPs, ports,
protocol type, and flags) for later review.

## Tools Used
- Python 3
- [Scapy](https://scapy.net/) — packet manipulation and sniffing library

## ⚠️ Legal & Ethical Notice
Only capture traffic on networks and devices you own or are explicitly
authorized to monitor. Capturing traffic on networks without permission is
illegal in most jurisdictions.

## Setup

### 1. Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install scapy
```

### 2. Permissions
Packet sniffing requires raw socket access, which needs elevated privileges.

Run with `sudo`:
```bash
sudo python3 scripts/Netowk-packer-tracer.py 50
```

If using a virtual environment, make sure `sudo` uses the venv's Python:
```bash
sudo -E python3 scripts/Netowk-packer-tracer.py 50
```

Alternatively, grant the capability directly to avoid needing `sudo` each time
(personal lab machines only):
```bash
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
```

## Usage
```bash
sudo python3 scripts/Netowk-packer-tracer.py <packet_count>

# Example: capture 50 packets
sudo python3 scripts/Netowk-packer-tracer.py 50
```

While it's capturing, generate some traffic in another terminal (e.g.
`ping 8.8.8.8` or browsing a website) to see packets logged in real time.

## How It Works
1. Uses Scapy's `sniff()` to capture live packets on the default interface.
2. For each packet, inspects the IP layer and identifies whether it's
   TCP, UDP, or ARP.
3. Extracts source/destination IPs, ports (for TCP/UDP), and TCP flags.
4. Prints a live one-line summary per packet to the terminal.
5. Saves all captured packet metadata to `examples/sample_capture.json`.

## Sample Output
```
Capturing 50 packets... (Ctrl+C to stop early)
[TCP] 192.168.1.15 -> 142.250.71.14
[UDP] 192.168.1.15 -> 8.8.8.8
[ARP] 192.168.1.15 -> 192.168.1.1
...
Saved 50 packets to examples/sample_capture.json
```

## Project Structure
```
02-packet-analysis/
├── README.md
├── scripts/
│   └── packet_sniffer.py
└── examples/
    └── sample_capture.json
```

## What I Learned
- How raw packet capture works at the OS level and why it requires elevated
  (root) privileges
- The structural differences between TCP, UDP, and ARP packets
- How to use Scapy to parse packet layers programmatically instead of relying
  solely on GUI tools like Wireshark
- How virtual environments interact with `sudo`, and why `sudo -E` or
  `setcap` may be needed to avoid privilege/environment mismatches

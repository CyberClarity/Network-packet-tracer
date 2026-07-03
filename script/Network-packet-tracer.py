import sys
import json
import os
from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP, ARP

captured_packets = []

def process_packet(packet):
    entry = {"timestamp": datetime.now().isoformat()}

    if packet.haslayer(IP):
        entry["src_ip"] = packet[IP].src
        entry["dst_ip"] = packet[IP].dst
        entry["protocol"] = packet[IP].proto

        if packet.haslayer(TCP):
            entry["type"] = "TCP"
            entry["src_port"] = packet[TCP].sport
            entry["dst_port"] = packet[TCP].dport
            entry["flags"] = str(packet[TCP].flags)
        elif packet.haslayer(UDP):
            entry["type"] = "UDP"
            entry["src_port"] = packet[UDP].sport
            entry["dst_port"] = packet[UDP].dport

    elif packet.haslayer(ARP):
        entry["type"] = "ARP"
        entry["src_ip"] = packet[ARP].psrc
        entry["dst_ip"] = packet[ARP].pdst

    if "type" in entry:
        captured_packets.append(entry)
        print(f"[{entry['type']}] {entry.get('src_ip','?')} -> {entry.get('dst_ip','?')}")

def start_capture(count=50, iface=None):
    print(f"Capturing {count} packets... (Ctrl+C to stop early)")
    sniff(prn=process_packet, count=count, iface=iface, store=False)

    os.makedirs("examples", exist_ok=True)
    with open("examples/sample_capture.json", "w") as f:
        json.dump(captured_packets, f, indent=2)
    print(f"\nSaved {len(captured_packets)} packets to examples/sample_capture.json")

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    start_capture(count)

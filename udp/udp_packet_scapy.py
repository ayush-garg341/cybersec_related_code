from scapy.all import IP, UDP, sr1

dst_addr = "127.0.0.1"
dst_port = 31337

# sport = 31338

# pkt = IP(dst=dst_addr) / UDP(sport=sport, dport=dst_port) / b"Hello, World!\n"

pkt = IP(dst=dst_addr) / UDP(dport=dst_port) / b"Hello, World!\n"

reply = sr1(pkt, timeout=10, verbose=False)

if reply:
    print(bytes(reply[UDP].payload))
else:
    print("No reply")

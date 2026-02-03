from scapy.all import Ether, sendp, IP

iface = "eth0"
src_mac = "76:39:05:f2:bb:b7"
dst_ip = "10.0.0.2"

# Scapy stacking operator
pkt = Ether(src=src_mac, type=0xFFFF) / IP(dst=dst_ip) / b"HELLO"  # dst MAC left empty

# Fills Ether.dst by resolving mac address using arp
sendp(pkt, iface=iface, verbose=True)

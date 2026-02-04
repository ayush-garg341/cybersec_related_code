from scapy.all import Ether, ARP, sendp

iface = "eth0"

announced_ip = "10.0.0.42"
announced_mac = "42:42:42:42:42:42"

target_ip = "10.0.0.2"

pkt = Ether(src=announced_mac) / ARP(
    op=2,  # ARP reply ("is-at")
    psrc=announced_ip,  # IP being announced
    hwsrc=announced_mac,  # MAC being announced
    pdst=target_ip,  # target IP
)

# ARP is a Layer-2 (Ethernet) protocol.
sendp(pkt, iface=iface, verbose=True)

# send() → Layer 3 (IP)
# sendp() → Layer 2 (Ethernet)

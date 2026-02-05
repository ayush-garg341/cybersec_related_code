from scapy.all import Ether, ARP, sendp, srp

iface = "eth0"
target_ip = "10.0.0.2"

pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(  # Ethernet broadcast
    op=1, pdst=target_ip
)  # ARP who-has

sendp(pkt, iface=iface, verbose=True)

# Ethernet broadcast goes out.
# The host that owns 10.0.0.2 replies with its MAC.

# Send ARP and wait for the reply (most useful)

pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip)
ans, _ = srp(pkt, iface=iface, timeout=2, verbose=False)

for _, reply in ans:
    print("IP:", reply.psrc, "MAC:", reply.hwsrc)

# ARP requests (broadcast)
# ARP replies (unicast)

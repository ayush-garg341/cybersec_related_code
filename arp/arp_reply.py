"""
Manually send an Address Resolution Protocol packet. The packet informs the remote host that the IP address 10.0.0.42 can be found at the Ethernet address 42:42:42:42:42:42. The packet should be sent to the remote host at 10.0.0.2.
"""

from scapy.all import Ether, ARP, sendp, srp, get_if_hwaddr

iface = "eth0"


def get_mac(ip, iface="eth0"):
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    ans, _ = srp(pkt, timeout=3, retry=2, iface=iface, verbose=False)

    if len(ans) == 0:
        return None

    return ans[0][1].hwsrc


# Getting mac address of another machine
announced_ip = "10.0.0.42"
announced_mac = get_mac("10.0.0.42")
print("MAC:", announced_mac)

# if need to check same machine mac address
mac_same_machine = get_if_hwaddr("eth0")
print(mac_same_machine)


# Sending ARP reply
target_ip = "10.0.0.2"

pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(
    op=2,  # ARP reply ("is-at")
    psrc=announced_ip,  # IP being announced
    hwsrc=announced_mac,  # MAC being announced
    pdst=target_ip,  # target IP
    hwdst="ff:ff:ff:ff:ff:ff",
)

# ARP is a Layer-2 (Ethernet) protocol.
sendp(pkt, iface=iface, verbose=True)

# send() → Layer 3 (IP)
# sendp() → Layer 2 (Ethernet)

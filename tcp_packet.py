from scapy.all import IP, TCP, send

pkt = IP(dst="10.0.0.2") / TCP(
    sport=31337, dport=31337, flags="APRSF", seq=31337, ack=31337
)

send(pkt)

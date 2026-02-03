from scapy.all import IP, send

pkt = IP(dst="10.0.0.2", proto=0xFF) / b"HELLO_IP"

send(pkt)

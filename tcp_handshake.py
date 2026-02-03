from scapy.all import IP, TCP, sr1, send

# Config ===
sport = 31337
dport = 31337
seq = 31337
dest_ip = "10.0.0.2"


# Step 1 ===
ip = IP(dst=dest_ip)

# Send SYN
syn = TCP(sport=sport, dport=dport, flags="S", seq=31337)

print("[*] Sending SYN")

# send & receive 1 packet
synack = sr1(ip / syn, timeout=2, verbose=False)

if synack is None:
    print("[!] No SYN-ACK received")
    exit(1)

# STEP 2: VERIFY SYN-ACK
if not (synack.haslayer(TCP) and synack[TCP].flags & 0x12):
    print("[!] Invalid SYN-ACK")
    exit(1)

print("[*] Received SYN-ACK")

synack.show()

# STEP 3: SEND ACK

ack = TCP(sport=sport, dport=dport, flags="A", seq=synack.ack, ack=synack.seq + 1)

print("[*] Sending ACK (Handshake complete)")

# Fire-and-forget - sends packets, does not wait
send(ip / ack, verbose=False)

# STEP 4: Optional send data
payload = b"Hello from scapy"

# PA : push + ack
data = TCP(sport=sport, dport=dport, flags="PA", seq=ack.seq, ack=ack.ack) / payload

print("[*] Sending TCP data")
send(ip / data, verbose=False)

# OPTIONAL: CLOSE CONNECTION

# FA: fin + ack

fin = TCP(
    sport=sport,
    dport=dport,
    flags="FA",
    seq=data.seq + len(payload),
    ack=data.ack,
)

print("[*] Sending FIN")
send(ip / fin, verbose=False)

print("[✓] Done")

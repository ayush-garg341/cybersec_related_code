import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)
sock.bind(("10.0.0.1", 31337))

port = 0


def worker(sock, port):
    try:
        sock.sendto(b"FLAG:10.0.0.1:31337", ("10.0.0.2", port))
        data, _ = sock.recvfrom(1024)
        print(data.decode())
    except Exception as e:
        print(e)


while True:
    port += 1
    th = threading.Thread(target=worker, args=(sock, port))
    th.start()
    if port > 65535:
        print("all ports scanned")
        break

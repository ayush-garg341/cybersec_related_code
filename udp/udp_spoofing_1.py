import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

src_port = 31337

sock.bind(("10.0.0.1", 31337))
# Request new session
sock.sendto(b"FLAG", ("10.0.0.2", 31338))

data, _ = sock.recvfrom(1024)
print(data.decode())

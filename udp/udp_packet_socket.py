import socket

dst_addr = "127.0.0.1"
dst_port = 31337

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(("10.0.0.1", 31337))
sock.sendto(b"Hello, World!\n", (dst_addr, dst_port))
try:
    # Wait for reply
    data, addr = sock.recvfrom(4096)
    print("Received:", data.decode(), "from", addr)

except socket.timeout:
    print("No response from server")

sock.close()

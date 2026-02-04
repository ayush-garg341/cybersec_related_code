import socket

HOST = "127.0.0.1"
PORT = 31337
BUFFER_SIZE = 1024

try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"UDP Server is listening on {HOST}:{PORT}")
        while True:
            data, client_address = s.recvfrom(BUFFER_SIZE)
            if not data:
                break

            message = data.decode()
            print(f"Received data from {client_address}: {message}")

            response_message = f"Server Echo: {message}"
            s.sendto(response_message.encode(), client_address)
except KeyboardInterrupt:
    print("Server is shutting")

except Exception as e:
    print(f"An error occurred: {e}")

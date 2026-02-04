### Run the UDP server

- Create virtual env
- Activate
- pip install -r requirements.txt

- python3 udp_server.py
- python3 udp_packet_socket.py
    - Even if you do not specify the src port or bind, kernel will choose itself and you will get the response.

- python3 udp_packet_scapy.py
    - Requires sudo prev to run
    - If you do not specify src port, you will not receive the response from server.
    - If you specify the src port, you will receive the response.
    - You have to explicitly define the src port and not managed by the kernel.

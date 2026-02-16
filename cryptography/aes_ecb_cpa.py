from pwn import *

p = process("/challenge/run")

ascii_encryption_mapping = {}


def get_mapping(payload):
    p.sendlineafter("Choice?", b"1")
    p.sendlineafter("Data?", payload.encode())
    out = p.recvlines(1)[0]
    cipher = out.decode().split(" ")[2]
    return cipher


def get_encrypted_flag(index, length):
    p.sendlineafter("Choice?", b"2")
    p.sendlineafter("Index?", str(index).encode())
    p.sendlineafter("Length?", str(length).encode())
    out = p.recvlines(1)[0]
    cipher = out.decode().split(" ")[2]
    return cipher


def get_flag():
    for i in range(33, 126):
        char = chr(i)
        recv = get_mapping(char)
        ascii_encryption_mapping[recv] = char

    idx = 0
    length = 1
    flag = ""
    while True:
        try:
            msg = get_encrypted_flag(idx, length)
            flag += ascii_encryption_mapping[msg]
            idx += 1
        except Exception as e:
            print(e)
            break
    print(flag)


if __name__ == "__main__":
    get_flag()

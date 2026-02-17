from pwn import *

p = process("/challenge/run")


def get_mapping(payload):
    p.sendlineafter("Choice?", b"1")
    p.sendlineafter("Data?", payload.encode())
    out = p.recvlines(1)[0]
    cipher = out.decode().split(" ")[2]
    return cipher


def get_encrypted_flag(length):
    p.sendlineafter("Choice?", b"2")
    p.sendlineafter("Length?", str(length).encode())
    out = p.recvlines(1)[0]
    cipher = out.decode().split(" ")[2]
    return cipher


def get_flag():
    length = 1
    flag = ""
    while length < 64:
        try:
            msg = get_encrypted_flag(length)
            for i in range(33, 126):
                to_be_checked = flag
                char = chr(i)
                if flag == "":
                    to_be_checked = char
                else:
                    to_be_checked = char + flag
                print(to_be_checked)
                recv = get_mapping(to_be_checked)
                if recv == msg:
                    flag = char + flag
                    break

            length += 1
        except Exception as e:
            print(e)
            break

    print(flag)


if __name__ == "__main__":
    get_flag()

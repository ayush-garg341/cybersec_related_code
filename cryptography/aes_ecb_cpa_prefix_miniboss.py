"""
You don't get an easy way to build your codebook anymore: you must build it in the prefix. If you can change the length of your own prefixed data based on how much of the secret you know, you can control entire blocks, and that's all you need!
"""

from pwn import *

p = process("/challenge/run")


def get_encrypted_message(string):
    string = string.encode().hex()
    p.sendlineafter("Data?", string)
    out = p.recvlines(1)[0]
    cipher = out.decode().split(" ")[2]
    return cipher


def get_char():
    length = 64
    char = "A" * length
    while True:
        em = get_encrypted_message(char)
        if (
            em[32:64] == em[64:96]
            and em[64:96] == em[96:128]
            and em[96:128] == em[128:160]
        ):
            break
        length += 1
        char = "A" * length

    return char


def get_block(msg):
    return msg[128:160]


def get_flag():
    msg = get_char()
    length = len(msg)
    length -= 1
    msg = msg[:length]
    flag = ""
    while True:
        em = get_encrypted_message(msg)
        em_block = get_block(em)
        for i in range(33, 126):
            char = chr(i)
            to_be_checked = msg + flag + char
            to_be_checked_em = get_encrypted_message(to_be_checked)
            to_be_checked_em_block = get_block(to_be_checked_em)
            if em_block == to_be_checked_em_block:
                flag += char
                length -= 1
                msg = msg[:length]
                break
        if flag[-1] == "}":
            break
    return flag


if __name__ == "__main__":
    print(get_flag())

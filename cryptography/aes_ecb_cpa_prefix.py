"""
This attack is same as https://node-security.com/posts/cryptography-byte-by-byte-ecb-decryption/
We are prepending the unknown secret with our user message.
"""

from pwn import *

p = process("/challenge/run")


def get_encrypted_message(length):
    p.sendlineafter("Choice?", b"2")
    p.sendlineafter("Data?", str(length).encode())
    out = p.recvlines(1)[0]
    cipher = out.decode().split(" ")[2]
    return cipher


def get_block_size():
    """
    Step 1
    """
    msg = "A"
    prev_len = 0
    block_size = 0
    while True:
        encr_msg = get_encrypted_message(msg)
        current_len = len(encr_msg)
        if not prev_len:
            prev_len = len(encr_msg)
        elif current_len > prev_len:
            block_size = current_len - prev_len
            break
        msg = "A" + msg

    return block_size // 2


def get_unknown_string_length():
    """
    Step 2
    """
    msg = "A"
    prev_len = 0
    block_size = 0
    current_len = 0
    while True:
        encr_msg = get_encrypted_message(msg)
        current_len = len(encr_msg)
        if not prev_len:
            prev_len = len(encr_msg)
        elif current_len > prev_len:
            block_size = current_len - prev_len
            break
        msg = "A" + msg

    unknown_string_len = current_len // 2 - block_size // 2 - len(msg)
    return unknown_string_len


def get_user_string_len_greater_than_unknown_string(unknown_string_len, block_size):
    num = 1
    mul = block_size * num
    while mul < unknown_string_len:
        num += 1
        mul = block_size * num

    return mul


def get_user_message(user_string_len, found_unknown_string_len, found_unknown_string):
    return "A" * (user_string_len - found_unknown_string_len - 1)


def get_block_of_interest(encrypted_message, user_string_len, block_size):
    idx = (user_string_len - 1) // block_size
    return encrypted_message[block_size * idx : block_size * (idx + 1)]


def determine_the_unknown_string(block_size, unknown_string_len, user_string_len):
    """
    Function responsible to get unknown string.
    """
    found_unknown_string_len = 0
    found_unknown_string = ""

    iter = 0
    while iter < unknown_string_len:
        user_message = get_user_message(
            user_string_len, found_unknown_string_len, found_unknown_string
        )
        print(
            "user message :: {} and len :: {}".format(user_message, len(user_message))
        )

        encrypted_message = get_encrypted_message(user_message)
        encrypted_message_bytes = bytes.fromhex(encrypted_message)
        block_of_interest = get_block_of_interest(
            encrypted_message_bytes,
            user_string_len,
            block_size,
        )

        for i in range(33, 126):
            char = chr(i)
            tampered_message = user_message + found_unknown_string + char
            encrypted_message = get_encrypted_message(tampered_message)
            encrypted_message_bytes = bytes.fromhex(encrypted_message)
            tampered_block_of_interest = get_block_of_interest(
                encrypted_message_bytes,
                user_string_len,
                block_size,
            )

            if block_of_interest == tampered_block_of_interest:
                print("tampered message:: {}".format(tampered_message))
                found_unknown_string_len += 1
                found_unknown_string += char
                break

        iter += 1

    return found_unknown_string


def get_flag():
    block_size = get_block_size()
    print("Block size:: ", block_size)

    unknown_string_len = get_unknown_string_length()
    print("Unknown string len:: ", unknown_string_len)

    user_string_len = get_user_string_len_greater_than_unknown_string(
        unknown_string_len, block_size
    )

    print("User string len:: ", user_string_len)

    return determine_the_unknown_string(block_size, unknown_string_len, user_string_len)


if __name__ == "__main__":
    print(get_flag())

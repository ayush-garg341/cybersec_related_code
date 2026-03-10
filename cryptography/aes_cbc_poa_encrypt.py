"""
Padding Oracle Attack doesn't just let you decrypt arbitrary messages: it lets you encrypt arbitrary data as well.
CT: IV | C1 | C2 | C3
PT: P1 | P2 | P3

P3 = D(C3) ^ C2
P2 = D(C2) ^ C1
P1 = D(C1) ^ IV

Calculate right to left:
    - Take a random C3 and random IV, and run padding Oracle attack and retrieve D(C3)
    - Now we have C3, we can get C2 as well from above equations. And we will have C2 | C3 which will decrypt to P3
    - Now try to get C1, for that we need D(C2), but we have C2, run the same POA to get D(C2)
    - Now after getting D(C2) we can retrieve C1.
    - We have C1, but not D(C1) so run POA again to get D(C1).
    - Once we have D(C1), we can retrieve IV as well.
    - Now we have all the components of CT, we can form the complete CT as IV | C1 | C2 | C3
"""

from Crypto.Util.Padding import unpad, pad

from pwn import *

p = process("/challenge/worker")

BLOCKSIZE = 16


def get_encrypted_message(msg):
    p.sendline(msg)
    resp = p.recvline()
    return resp


def retrieve_last_block(task):
    data = bytes.fromhex(task.split()[1])

    original_iv = data[:BLOCKSIZE]
    ciphertext = data[BLOCKSIZE:]

    I = [0] * BLOCKSIZE
    plaintext = [0] * BLOCKSIZE

    for n in reversed(range(BLOCKSIZE)):

        pad = BLOCKSIZE - n

        for guess in range(256):

            iv = bytearray(original_iv)

            # adjust already found bytes
            for j in range(n + 1, BLOCKSIZE):
                iv[j] = I[j] ^ pad

            iv[n] = guess

            tampered = bytes(iv) + ciphertext
            payload = "TASK: " + tampered.hex()

            # This function, will tell whether padding is valid or not based on error.
            resp = get_encrypted_message(payload)
            resp = resp.decode()

            if "Error:" not in resp:

                # recover intermediate value
                I[n] = guess ^ pad

                # recover plaintext byte
                plaintext[n] = I[n] ^ original_iv[n]

                print("Found byte:", n, chr(plaintext[n]))

                break

    hex_value = bytes(I).hex()
    return hex_value


if __name__ == "__main__":
    # Initially random IV and random last block cipher text
    IV = "e757c00121271da8bd531a8a2ff54856"
    last_ct = "96f239bde8c7844af8fffc4784909166"
    task = f"TASK: {IV}{last_ct}"

    # Original msg that we want to encrypt, 45 characters
    original_msg = "please give me the flag, kind worker process!"
    padded = pad(original_msg.encode(), 16)

    # 16 bytes blocks/chunks of our original message.
    chunks = [padded[i : i + 16] for i in range(0, len(padded), 16)]

    # We know last block CT3, but don't know D(CT),
    # so we will run Padding Oracle attack to get D(CT)
    # And then P3 ^ D(CT3) = C2
    len_chunks = len(chunks)
    i = -1
    complete_ct = last_ct
    while len_chunks != 0:
        current_dec_block = retrieve_last_block(task)
        print("chunks :: ", chunks[i])
        print(f"D(CT[{i}])", last_ct)
        previous_block_ct = bytes(
            a ^ b for a, b in zip(bytes.fromhex(current_dec_block), chunks[i])
        )

        i -= 1
        print(f"CT[{i}]", previous_block_ct.hex())
        task = f"TASK: {IV}{previous_block_ct.hex()}"
        len_chunks -= 1

        complete_ct = previous_block_ct.hex() + complete_ct

    print("complete cipher text:: ", complete_ct)

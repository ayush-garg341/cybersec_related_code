"""
P1[i] = I[i] XOR IV[i]
I = D(C1) for i = 1

Recovering byte 15 (last byte)
 - IV'[15] = guess
 - P1'[15] = 01
 - P1'[15] = I[15] XOR IV'[15] so that I[15] XOR IV'[15] = 01
 - I[15] = IV'[15] XOR 01
 - P1[15] = I[15] XOR IV[15]

Moving to byte 14
 - Now we want padding: 02 02. So we must modify the last two bytes of IV.
 - We already know: I[15], To force padding 02: P1'[15] = 02
 - IV'[15] = I[15] XOR 02 , This guarantees: P1'[15] = 02
 - Brute-force byte 14
 - IV'[14] = guess
 - When the oracle says valid padding: P1'[14] = 02
 - I[14] XOR IV'[14] = 02, I[14] = IV'[14] XOR 02
 - Then real plaintext: P1[14] = I[14] XOR IV[14]

"""

from Crypto.Util.Padding import unpad

from pwn import *

p = process("/challenge/worker")

print(p.recvline())

BLOCKSIZE = 16


def get_encrypted_message(msg):
    p.sendline(msg)
    resp = p.recvline()
    return resp


if __name__ == "__main__":

    task = "TASK: e757c00121271da8bd531a8a2ff5485696f239bde8c7844af8fffc4784909166"
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

            resp = get_encrypted_message(payload)
            resp = resp.decode()

            if "Error:" not in resp:

                # recover intermediate value
                I[n] = guess ^ pad

                # recover plaintext byte
                plaintext[n] = I[n] ^ original_iv[n]

                print("Found byte:", n, chr(plaintext[n]))

                break

    pw = bytes(plaintext)
    print("unpadded:", unpad(pw, 16))
    print(plaintext)
    print("Recovered password:", pw.hex())

"""
P1 = D(C1) XOR IV
orig = b"sleep"
target = b"flag"

P1' = D(C1) XOR IV'
but P1  = D(C1) XOR IV
IV' = P1 XOR P1' XOR IV

P1 -> orig
P1' -> target
"""

task = "TASK: 117797cc611b5c625819068222df0b17b780d347a89cb922c8b804b8dbfe7d71"

if task.startswith("TASK: "):
    data = bytes.fromhex(task.split()[1])
    iv = bytearray(data[:16])
    ciphertext = data[16:]
    print(ciphertext)

    orig = (
        b"sleep" + b"\x0b" * 11
    )  # padding of 11, 0b  as message is 5 bytes and we need 16 bytes
    target = (
        b"flag" + b"\x0c" * 12
    )  # padding of 12, 0c as message is 4 bytes and we need 16 bytes

    for i in range(len(orig)):
        iv[i] ^= orig[i] ^ target[i]

    tampered = bytes(iv) + ciphertext

    print(tampered.hex())

"""

====== signer.py ======

#!/usr/bin/exec-suid -- /usr/bin/python3 -I

import sys

from base64 import b64encode, b64decode

n = int(open("/challenge/key-n").read(), 16)
d = int(open("/challenge/key-d").read(), 16)

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} [command-b64]")
    sys.exit(1)

command = b64decode(sys.argv[1].strip("\0"))

if b"flag" in command:
    print(f"Command contains 'flag'")
    sys.exit(1)

signature = pow(int.from_bytes(command, "little"), d, n).to_bytes(256, "little")
print(f"Signed command (b64): {b64encode(signature).decode()}")


====== verifier.py ========

#!/usr/bin/exec-suid -- /usr/bin/python3 -I

import sys

from base64 import b64decode

n = int(open("/challenge/key-n").read(), 16)
e = int(open("/challenge/key-e").read(), 16)

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} [signature-b64]")
    sys.exit(1)

signature = b64decode(sys.argv[1])
c = int.from_bytes(signature, "little")
assert c < n, "Message too big!"
command = pow(c, e, n).to_bytes(256, "little").rstrip(b"\x00")

print(f"Received signed command: {command}")
if command == b"flag":
    print(open("/flag").read())


The problem is based upon the fact that command ( be 64encode ) we use to sign,
should not be "flag", otherwise code won't sign it.

echo -n "string" | base64

So we have to modify our command in such a way that it's not "flag" and when
verified it, it recovers as a flag.

m = "flag"

m_prime = m * r^e (mod n)

m_prime ^ d = (m * r ^ e) ^ d (mod n)
            = m ^ d * r (mod n) ( because e*d = 1 (mod n))

s_prime = m_prime ^ d

r_inv = r ^ -1 ( to cancel extra r from above equation )
orig_s = s_prime * r_inv (mod n) ( it will cancel extra r, from s_prime)

And then passing this orig_s to verifier, we will recover the flag.

b64encode, b64decode -> both gives bytes...
"""

import base64

n = int(open("/challenge/key-n").read(), 16)
e = int(open("/challenge/key-e").read(), 16)

# Step 1
m = int.from_bytes(b"flag", "little")

# Step 2
r = 2

# Step 3
m_prime = (m * pow(r, e, n)) % n

# Step 4 (send to signer)
m_prime_bytes = m_prime.to_bytes(256, "little")
print("Send to signer:")
print(base64.b64encode(m_prime_bytes).decode())

# ---- paste signer output ----
sig_prime_b64 = input("Signer output: ")

# Step 5
sig_prime = int.from_bytes(base64.b64decode(sig_prime_b64), "little")

# Step 6
r_inv = pow(r, -1, n)
sig = (sig_prime * r_inv) % n

# Step 7 (verify locally BEFORE sending)
recovered = pow(sig, e, n)

print("Recovered int:", recovered)
print("Expected int :", m)

print("Recovered bytes:", recovered.to_bytes(256, "little").rstrip(b"\x00"))

# Step 8 (final payload)
print("\nFINAL PAYLOAD:")

# b64encode gives bytes, and then decoding the bytes.
print(base64.b64encode(sig.to_bytes(256, "little")).decode())

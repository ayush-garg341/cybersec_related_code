import base64
import secrets
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash.SHA256 import SHA256Hash

"""

Perform a simplified Transport Layer Security (TLS) handshake, acting as the server. You will be provided with Diffie-Hellman parameters, a self-signed root certificate, and the root private key. The client will request to establish a secure channel with a particular name, and initiate a Diffie-Hellman key exchange. The server must complete the key exchange, and derive an AES-128 key from the exchanged secret. Then, using the encrypted channel, the server must supply the requested user certificate, signed by root. Finally, using the encrypted channel, the server must sign the handshake to prove ownership of the private user key.

Diffie-Hellman (key exchange) + Certificates (identity) + Signatures (proof)

STEP 1:
You are acting as:
    - TLS Server
    - Agree on a shared secret (Diffie-Hellman)
    - Turn that into an AES key
    - Send a certificate (prove identity)
    - Prove you own the private key (signature)

Client sends:
    A = g^a mod p

You (server) do:
    b = random_secret
    B = pow(g, b, p)

SHared secret:
    shared_secret = pow(A, b, p)

Client computes same value:
    pow(B, a, p)


STEP 2 Derive AES key:
You now convert the shared secret into a key:
    key = sha256(shared_secret.to_bytes(...)).digest()[:16]  # AES-128

STEP 3 Encrypted Channel Starts:
    - All communication is encrypted using AES

STEP 4: Send User Certificate
    - CLient asks "Give me certificate for NAME"
    - You must Create user certificate:
{
  "name": requested_name,
  "key": { "e": ..., "n": ... },
  "signer": "root"
}

    - Sign it using root private key
    - Encrypt it with AES
    - Send it

This proves: Root CA says this public key belongs to NAME.

STEP 5: Prove You Own Private Key
    - Client says: Okay, prove you actually own the private key of that certificate.
    - You must: 
    - Take handshake data (usually transcript)
    - Sign it using user private key
    - signature = pow(hash, user_d, user_n)
    - Encrypt signature with AES
    - Send it

Full Flow:
1. Client → A = g^a mod p

2. Server → B = g^b mod p

3. Both compute shared_secret

4. Derive AES key

5. Encrypted channel starts

6. Server → sends signed user certificate

7. Server → signs handshake using user private key

8. Client verifies everything

"""


g = 0x2

p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF

p = int((input("Enter p? ")), 16)

root_certificate_base64 = input("Root certificate b64? ")

root_certificate_signatute_base64 = input("Root certificate signature b64? ")

root_key_d = int((input("Enter root private key? ")), 16)

A = int((input("Enter A in hex? ")), 16)

name = input("Certificate name? ")

root_certificate_decode = json.loads(base64.b64decode(root_certificate_base64).decode())
print("root certificate data== ", root_certificate_decode)
root_certificate_n = root_certificate_decode["key"]["n"]

b = secrets.randbelow(p - 2) + 1
B = pow(g, b, p)
shared_secret = pow(A, b, p)

print("b=== ", b)
print("B=== ", hex(B))
print("shared secret === ", hex(shared_secret))

user_key = RSA.generate(1024)

user_certificate = {
    "name": name,
    "key": {
        "e": user_key.e,
        "n": user_key.n,
    },
    "signer": "root",
}

certificate_data = json.dumps(user_certificate).encode()
certificate_hash = SHA256Hash(certificate_data).digest()
print("certificate hash == ", base64.b64encode(certificate_hash).decode())

# Encrypting certificate data using CBC encryption

iv = b"\x00" * 16

shared_secret_bytes = shared_secret.to_bytes(
    (shared_secret.bit_length() + 7) // 8, "little"
)

aes_key = SHA256Hash(shared_secret_bytes).digest()[:16]  # AES-128
cipher = AES.new(aes_key, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(certificate_data, 16))

print("certificate data encrypted and encoded == ", base64.b64encode(ct).decode())

certificate_signature = pow(
    int.from_bytes(certificate_hash, "little"), root_key_d, root_certificate_n
).to_bytes(256, "little")

enc_sig = cipher.encrypt(pad(certificate_signature, 16))

print(
    "certificate signature encrypted and encoded== ", base64.b64encode(enc_sig).decode()
)

user_signature_data = (
    name.encode().ljust(256, b"\0")
    + A.to_bytes(256, "little")
    + B.to_bytes(256, "little")
)

user_signature_hash = SHA256Hash(user_signature_data).digest()
user_signature = pow(
    int.from_bytes(user_signature_hash, "little"), user_key.d, user_key.n
).to_bytes(256, "little")

enc_user_sig = cipher.encrypt(pad(user_signature, 16))
print("user signature enc and encoded == ", base64.b64encode(enc_user_sig).decode())

secret_ct = input("Secret ct base64? ")
cipher_decrypt = AES.new(aes_key, AES.MODE_CBC, iv)
pt = cipher_decrypt.decrypt(base64.b64decode(secret_ct))
print("pt decode== ", pt)

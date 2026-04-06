import base64
import json
from Crypto.PublicKey import RSA
from Crypto.Hash.SHA256 import SHA256Hash

key = RSA.generate(1024)


user_certificate = {
    "name": "user",
    "key": {
        "e": key.e,
        "n": key.n,
    },
    "signer": "root",
}

print("user certificate== ", user_certificate)
user_key_d = key.d
print("user key d== ", user_key_d)

certificate_data = json.dumps(user_certificate).encode()
certificate_hash = SHA256Hash(certificate_data).digest()

root_key_d = int((input("Enter the root signer private key (d)? ")), 16)
root_certificate = input("Enter the root certificate b64? ")

root_certificate_decode = json.loads(base64.b64decode(root_certificate).decode())
print("root certificate data== ", root_certificate_decode)
root_certificate_n = root_certificate_decode["key"]["n"]

# Compute key size dynamically
key_size = (root_certificate_n.bit_length() + 7) // 8

print("key size == ", key_size)

certificate_signature = pow(
    int.from_bytes(certificate_hash, "little"), root_key_d, root_certificate_n
).to_bytes(256, "little")

print("certificate data encoded== ", base64.b64encode(certificate_data).decode())
print("certificate hash encoded== ", base64.b64encode(certificate_hash).decode())
print(
    "certificate signature encoded== ", base64.b64encode(certificate_signature).decode()
)


user_key_n = user_certificate["key"]["n"]

ct = input("Enter the base64 encoded cipher text? ")

decoded_ct = base64.b64decode(ct)

message = pow(int.from_bytes(decoded_ct, "little"), user_key_d, user_key_n).to_bytes(
    256, "little"
)

print(message)

import base64
from Crypto.PublicKey import RSA

# Step 1: Generate your key pair
key = RSA.generate(1024)

# Step 2: Send e and n to the server
print(f"Send e: {hex(key.e)}")
print(f"Send n: {hex(key.n)}")

# Step 3: Receive challenge from server and sign it
challenge = int(input("Enter challenge (hex): "), 16)

# Step 4: Sign the challenge — this is your response
response = pow(challenge, key.d, key.n)
print(f"Send response: {hex(response)}")

# Step 5: Receive the encrypted flag and decrypt it
ciphertext_b64 = input("Enter secret ciphertext (base64): ")


ct_bytes = base64.b64decode(ciphertext_b64)
ct_int = int.from_bytes(ct_bytes, "little")

# Decrypt with your private key
flag_int = pow(ct_int, key.d, key.n)
flag = flag_int.to_bytes(64, "little")  # 64 bytes = size of flag plaintext

print(f"Flag: {flag}")

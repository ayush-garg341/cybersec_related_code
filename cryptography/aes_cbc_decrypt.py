from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key_hex = "c8ef3405ef3c277fd50a687e1c15a40b"
cipher_hex = "2da8afa405b4cb63de4968d234f2ca22bd2918c40041f037c0b7fc51652545b42a8571f238702de2db5e0e04544d6cfb18b2c47b7d1d3bd2f4cd369f0ef3cede831604ff23ead10474b84c6b18c0c4c2"

key = bytes.fromhex(key_hex)
cipher_bytes = bytes.fromhex(cipher_hex)

iv = cipher_bytes[:16]
ciphertext = cipher_bytes[16:]

cipher = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(ciphertext), AES.block_size)

print(pt)

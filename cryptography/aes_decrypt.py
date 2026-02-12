"""
- Symmetric encryption (same key is used for encrypt/decrypt).
- Block cipher, encrypting one plaintext "block" of 16 bytes (128 bits) at a time.
- AES must operate on complete blocks.
- If the plaintext is shorter than a block (e.g., AAAABBBB), it will be padded to the block size, and the padded plaintext will be encrypted.
- AES operates on binary blocks, not text.

- HEX STRING -> UTF-8 ( .encode() ) -> AES ( wrong )
- HEX STRING -> RAW BYTES -> AES ( right )
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

ct = "048a3e95c009126e025738c8e36d6add82cfcaa1fa5342846b120aa06392a87a92c20a1ea78636a415d42407c36a3860f4adccbaf83f4591c5f3357e5535194f"

aes_key = "d1ba8baa583a20f8491ca01fc23c7501"

ct = bytes.fromhex(ct)
aes_key = bytes.fromhex(aes_key)

cipher = AES.new(aes_key, AES.MODE_ECB)
message = cipher.decrypt(ct)

# remove PKCS7 padding
plaintext = unpad(message, AES.block_size)

print("Message:", message.decode("ascii"))

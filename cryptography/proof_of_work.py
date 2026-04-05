import hashlib
import base64


def brute_force_3_bytes(target_bytes):
    # target_bytes should be a bytes object of length 3
    counter = 0
    challenge = "qr9Ym8djdZeaoujVIcrlxW3B5+aURfnIDHG0tSzMb80="

    # b64decode gives bytes
    challenge_bytes = base64.b64decode(challenge)
    print(challenge_bytes)
    while True:
        # Generate input (using a simple counter converted to bytes)
        input_data = str(counter).encode()
        modified_bytes = challenge_bytes + input_data

        # Calculate SHA-256 and take first 3 bytes
        current_hash = hashlib.sha256(modified_bytes).digest()[:2]

        if current_hash == target_bytes:
            print(f"Match found! Input: {counter}")

            # b64encode gives bytes
            print(base64.b64encode(input_data))
            return counter

        counter += 1


# Example: looking for a hash starting with hex '000000'
brute_force_3_bytes(b"\x00\x00")

import hashlib


def brute_force_3_bytes(target_bytes):
    # target_bytes should be a bytes object of length 3
    counter = 0
    while True:
        # Generate input (using a simple counter converted to bytes)
        input_data = str(counter).encode()

        # Calculate SHA-256 and take first 3 bytes
        current_hash = hashlib.sha256(input_data).digest()[:3]

        if current_hash == target_bytes:
            print(f"Match found! Input: {counter}")
            print(f"Full Hash: {hashlib.sha256(input_data).hexdigest()}")
            print(input_data.hex())
            return counter

        counter += 1


# Example: looking for a hash starting with hex '000000'
brute_force_3_bytes(b"\x14\x0c\xab")

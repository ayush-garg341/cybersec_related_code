def xor_hex(a: str, b: str) -> str:
    ba = bytes.fromhex(a)
    bb = bytes.fromhex(b)
    if len(ba) != len(bb):
        raise ValueError("Hex strings must be same length")

    msg_hex = bytes(x ^ y for x, y in zip(ba, bb)).hex()
    ascii_str = bytes.fromhex(msg_hex).decode("ascii")
    return ascii_str


if __name__ == "__main__":
    otp = "1a0fd9d9a359040df04b114e4c2803b3087fbbfc1631f48d3153ff586232775670e0e41d3d95a0c5c5b29ebb3840ea3e4b4f55f9e3cef319b7313dfa"
    ct = "6a78b7f7c0366861952c7435054f35f25c1beec44162aee5403dd269296035265da2b35767f6e4eb94eaaed8420d904922022dacb7818a5ccd6640f0"

    print(xor_hex(otp, ct))

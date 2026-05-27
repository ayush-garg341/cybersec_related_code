with open("program.cimg", "wb") as f:
    # Header
    f.write(b"cIMG")

    # version = 2
    f.write((2).to_bytes(2, "little"))

    # width = 39
    f.write((2).to_bytes(1, "little"))

    # height = 21
    f.write((2).to_bytes(1, "little"))

    total_pixels = 2 * 2

    f.write(bytes([0x6D, 0xE7, 0xDE, 0x63]))
    f.write(bytes([0x68, 0xE6, 0x89, 0x49]))
    f.write(bytes([0x84, 0xC2, 0x18, 0x4D]))
    f.write(bytes([0x48, 0x73, 0x7B, 0x47]))

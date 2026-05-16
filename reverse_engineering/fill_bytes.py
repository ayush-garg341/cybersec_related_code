with open("program.cimg", "wb") as f:
    f.write(b"Cm@g")
    f.write(b"\x01\x00")
    f.write(b"\x47")
    f.write(b"\x15\x00")

    total_bytes = 71 * 21
    for i in range(total_bytes):
        f.write(b"\x00")


with open("program.cimg", "rb") as f:
    data = f.read()
    print(len(data))

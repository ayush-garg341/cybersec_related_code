def get_message_hex():
    while True:
        inp = input("Enter the secret key and encrypted message, separated by spaces ")
        inputs = inp.split(" ")
        key = inputs[0]
        enc_mess = inputs[1]
        key_int = int(key, 16)
        enc_mess_int = int(enc_mess, 16)
        plain_mess = key_int ^ enc_mess_int

        print("The plain message", hex(plain_mess))


if __name__ == "__main__":
    get_message_hex()

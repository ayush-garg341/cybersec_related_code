def get_message_ascii():
    while True:
        inp = input("Enter the encrypted message and secret key separated by spaces ")
        inputs = inp.split(" ")
        enc_char = inputs[0]
        key = int(inputs[1], 16)
        enc_char_hex = int(hex(ord(enc_char)), 16)
        plain_mess = key ^ enc_char_hex
        print(chr(plain_mess))


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
    # get_message_hex()
    get_message_ascii()

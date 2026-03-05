import requests
from base64 import b64decode


BASE_URL = "http://challenge.localhost:80/"


def retrieve_encryption_from_response(res):
    enc = ""
    split_res = res.split("<pre>")
    flag_res = split_res[1]
    for char in flag_res:
        if char != "<":
            enc += char
        else:
            break
    return enc


def get_block(msg):
    return msg[96:128]


def get_encrypted_msg(content):
    res = requests.post(BASE_URL, data={"content": content})
    encryption = retrieve_encryption_from_response(res.text)
    hex_val = b64decode(encryption).hex()
    return hex_val


def reset_data():
    url = "http://challenge.localhost:80/reset"
    requests.post(url)


def get_flag():
    msg = "A" * 62
    length = len(msg)
    flag = ""
    while True:
        # Make a post request and get the encrypted msg
        em = get_encrypted_msg(msg)

        # get the block
        em_block = get_block(em)

        # delete the data
        reset_data()

        for i in range(33, 126):
            char = chr(i)
            to_be_checked = msg + "|" + flag + char
            pt_em = get_encrypted_msg(to_be_checked)
            pt_em_block = get_block(pt_em)
            reset_data()
            if em_block == pt_em_block:
                flag += char
                length -= 1
                msg = "A" * length

        if flag[-1] == "}":
            break

    print("flag:: ", flag)


if __name__ == "__main__":
    reset_data()
    get_flag()

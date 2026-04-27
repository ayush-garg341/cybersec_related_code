from pwn import *
import re

p = process("/challenge/run")

LEVELS = {"TS": 4, "S": 3, "C": 2, "UC": 1}


def parse_set(s):
    return set(x.strip() for x in s.split(",") if x.strip())


def parse_ques(question: str):
    # Extract levels
    levels = re.findall(r"level (\w+)", question)
    subject_level, object_level = levels

    # Extract categories
    cats = re.findall(r"\{([^}]*)\}", question)
    subject_cats = parse_set(cats[0])
    object_cats = parse_set(cats[1])
    print(subject_level, subject_cats)
    print(object_level, object_cats)

    return subject_level, object_level, subject_cats, object_cats


if __name__ == "__main__":
    answer = p.recvuntil("your goal is to answer ")
    qs_line = p.recvline().strip().decode("utf-8")
    qs = int(qs_line.split(" ")[0])
    print(qs)
    for i in range(qs):
        num = i + 1
        q1_line = p.recvuntil(f"Q {num}.").strip()
        q1 = p.recvline().strip().decode("utf-8")
        print(q1)
        subject_level, object_level, subject_cat, object_cat = parse_ques(q1)

        action = None
        if "read" in q1.lower():
            action = "read"
        if "write" in q1.lower():
            action = "write"

        if action == "read":
            if LEVELS[subject_level] - LEVELS[
                object_level
            ] >= 0 and object_cat.issubset(subject_cat):
                p.sendline(b"yes")
            else:
                p.sendline(b"no")

        if action == "write":
            if LEVELS[object_level] - LEVELS[
                subject_level
            ] >= 0 and subject_cat.issubset(object_cat):
                p.sendline(b"yes")
            else:
                p.sendline(b"no")

    print(p.recvline())
    print(p.recvline())
    print(p.recvline())
    print(p.recvline())

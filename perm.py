#!/usr/bin/env python3

import os
import stat

SEARCH_DIRS = [
    "/bin",
    "/sbin",
    "/usr/bin",
    "/usr/sbin",
    "/usr/local/bin",
    "/usr/local/sbin",
]


def find_suid_binaries():
    results = []

    for base in SEARCH_DIRS:
        if not os.path.isdir(base):
            continue

        for root, dirs, files in os.walk(base):
            for name in files:
                path = os.path.join(root, name)
                try:
                    st = os.stat(path)
                except (PermissionError, FileNotFoundError):
                    continue

                if stat.S_ISREG(st.st_mode) and (st.st_mode & stat.S_ISUID):
                    results.append(path)

    return results


if __name__ == "__main__":
    suid_bins = find_suid_binaries()

    for path in suid_bins:
        print(path)

    print(f"\nTotal SUID binaries found: {len(suid_bins)}")

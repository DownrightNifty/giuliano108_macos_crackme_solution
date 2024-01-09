#!/usr/bin/env python3

# check if the provided (email, code) combo is valid

import hashlib
import sys

usage = (
    "usage: ./valid.py EMAIL CODE"
)

# s is a hexstring
def flip_byte_order(s):
    bytes_ = []
    i = 0
    for _ in range(len(s) // 2):
        byte = s[i:i+2]
        bytes_.append(byte)
        i += 2
    return "".join(list(reversed(bytes_)))

# email and code are strings
def isValidLicense(email, code):
    print("check 1")
    if len(code) != 24:
        return False

    h = hashlib.md5(email.encode('utf-8')).digest().hex()
    first_4_bytes = h[:4*2]
    uint_s = str(int(flip_byte_order(first_4_bytes), 16))

    print("check 2")
    if code[0:len(uint_s)] != uint_s:
        return False

    print("check 3")
    newCode = []
    for i in range(24):
        # convert string "0" to "9" to int 0 to 9
        if not (0x30 <= ord(code[i]) <= 0x39):
            return False
        v = ord(code[i]) - 0x30
        newCode.append(v)
    
    print("check 4: sum of newCode[10 to 14] == 21")
    sum_ = 0
    for i in range(5):
        sum_ += newCode[10 + i]
    print(f"calculated sum: {sum_}")
    if sum_ != 21:
        return False

    print("check 5: product of newCode[15 to 19] == 480")
    product = 1
    for i in range(5):
        product *= newCode[15 + i]
    print(f"calculated product: {product}")
    if product != 480:
        return False

    print("check 6: sum of odd-placed items == 3, 19, 35, or ...")
    sum_ = 0
    # range(start, stop, step)
    for i in range(0, 24, 2):
        sum_ += newCode[i]
    print(f"calculated sum: {sum_}")
    if sum_ & 15 != 3:
        return False

    print("check 7: sum of even-placed items == 7, 23, 39, or ...")
    sum_ = 0
    for i in range(1, 24, 2):
        sum_ += newCode[i]
    print(f"calculated sum: {sum_}")
    if sum_ & 15 != 7:
        return False

    return True

def main():
    if len(sys.argv) != 3:
        print(usage)
        sys.exit(1)
    email = sys.argv[1]
    code = sys.argv[2]

    if isValidLicense(email, code):
        print("passed all checks!")
    else:
        print("failed")

main()

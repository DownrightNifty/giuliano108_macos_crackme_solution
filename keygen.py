#!/usr/bin/env python3

# generate a valid code using the provided email

import sys
import hashlib

usage = (
    "usage: ./keygen.py EMAIL"
)

# first 6 of 3+16*n, n >= 0
F1 = [3, 19, 35, 51, 67, 83]

# first 6 of 7+16*n, n >= 0
F2 = [7, 23, 39, 55, 71, 87]

# s is a hexstring
def flip_byte_order(s):
    bytes_ = []
    i = 0
    for _ in range(len(s) // 2):
        byte = s[i:i+2]
        bytes_.append(byte)
        i += 2
    return "".join(list(reversed(bytes_)))

def codegen(email):
    # the final code = code_fixed + code_var
    # len(code_fixed) == 10, len(code_var) == 14, len(code) == 24

    h = hashlib.md5(email.encode('utf-8')).digest().hex()
    first_4_bytes = h[:4*2]
    # convert first 4 bytes to a string (as a uint)
    # max len of uint_s == 10
    uint_s = str(int(flip_byte_order(first_4_bytes), 16))
    # pad with zeroes if length != 10
    code_fixed = uint_s + ("0" * (10 - len(uint_s)))

    # initial code passes checks 1-5, will be adjusted to pass checks 6 and 7
    code_var = "99300" + "86521" + "0000"
    code = code_fixed + code_var

    # convert code to int array (i.e. "34..." -> [3, 4, ...])
    code = [int(c) for c in code]

    # adjust for check 6

    sum_ = 0
    for i in range(0, 24, 2):
        sum_ += code[i]
    # if sum & 15 == 3, then sum == 3+16*n
    target = None
    for f in F1:
        if f >= sum_:
            target = f
            break

    diff = target - sum_
    if diff != 0:
        # we have two values in code we can freely change that only affect check 6: code[20] and code[22]
        # as a sum they can be at max 18, which means we can always get to the nearest value of F1 because it will be at max 15 away
        if diff > 9:
            diff_1 = 9
            diff_2 = diff - 9
            code[20] = diff_1
            code[22] = diff_2
        else:
            code[20] = diff

    # adjust for check 7

    sum_ = 0
    for i in range(1, 24, 2):
        sum_ += code[i]
    # if sum & 15 == 7, then sum == 7+16*n
    target = None
    for f in F2:
        if f >= sum_:
            target = f
            break

    diff = target - sum_
    if diff != 0:
        if diff > 9:
            diff_1 = 9
            diff_2 = diff - 9
            code[21] = diff_1
            code[23] = diff_2
        else:
            code[21] = diff

    # convert code back into a string
    code = "".join([str(v) for v in code])

    return code

def main():
    if len(sys.argv) != 2:
        print(usage)
        sys.exit(1)
    email = sys.argv[1]
    print(codegen(email))

main()

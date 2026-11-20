import random

from engine.pygrader import grade_function

FUNC = "number_base_converter"
FORBIDDEN = []

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def reference(number, from_base, to_base):
    if not (2 <= from_base <= 36 and 2 <= to_base <= 36) or not number:
        return "ERROR"
    value = 0
    for ch in number:
        d = DIGITS.find(ch)
        if d < 0 or d >= from_base:
            return "ERROR"
        value = value * from_base + d
    if value == 0:
        return "0"
    out = ""
    while value:
        out = DIGITS[value % to_base] + out
        value //= to_base
    return out


def cases():
    c = [("1010", 2, 10), ("FF", 16, 10), ("255", 10, 16), ("123", 10, 2), ("Z", 36, 10), ("35", 10, 36),
         ("123", 1, 10), ("G", 16, 10), ("0", 10, 2), ("0", 2, 36), ("10", 10, 37), ("10", 37, 10), ("10", 10, 1),
         ("2", 2, 10), ("ZZ", 36, 2), ("1", 2, 2), ("777", 8, 16), ("1111111111111111", 2, 16),
         ("12345678901234567890", 10, 36), ("00101", 2, 10)]
    rng = random.Random(4307)
    for _ in range(30):
        fb, tb = rng.randint(2, 36), rng.randint(2, 36)
        n = rng.randint(0, 10 ** 9)
        s = ""
        while True:
            s = DIGITS[n % fb] + s
            n //= fb
            if not n:
                break
        c.append((s, fb, tb))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

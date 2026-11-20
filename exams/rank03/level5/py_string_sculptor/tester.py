import random

from engine.pygrader import grade_function

FUNC = "string_sculptor"
FORBIDDEN = []

def reference(text):
    out, n = "", 0
    for ch in text:
        if ch.isalpha():
            out += ch.upper() if n % 2 else ch.lower()
            n += 1
        else:
            out += ch
    return out


def cases():
    c = [("hello",), ("Hello World",), ("   hello   ",), ("abc123def",), ("Python3.9!",), ("",), ("A",), ("1234",),
         ("ALL CAPS HERE",), ("a-b-c-d",), ("x y z",)]
    rng = random.Random(4312)
    for _ in range(25):
        c.append(("".join(rng.choice("abcXYZ 1.!") for _ in range(rng.randint(0, 15))),))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

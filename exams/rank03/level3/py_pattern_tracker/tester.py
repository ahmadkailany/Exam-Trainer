import random

from engine.pygrader import grade_function

FUNC = "pattern_tracker"
FORBIDDEN = []

def reference(text):
    count = 0
    for i in range(len(text) - 1):
        a, b = text[i], text[i + 1]
        if a.isdigit() and b.isdigit() and int(b) == int(a) + 1:
            count += 1
    return count


def cases():
    c = [("123",), ("12a34",), ("987654321",), ("01234567",), ("abc",), ("1a2b3c4",), ("112233",), ("",),
         ("9",), ("90",), ("89",), ("0123456789",), ("1212",), ("12 23 34",), ("x12x",)]
    rng = random.Random(4308)
    for _ in range(30):
        c.append(("".join(rng.choice("0123456789a ") for _ in range(rng.randint(0, 15))),))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

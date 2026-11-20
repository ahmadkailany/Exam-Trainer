import random

from engine.pygrader import grade_function

FUNC = "whisper_cipher"
FORBIDDEN = []

def reference(text, shift):
    out = ""
    for ch in text:
        if "a" <= ch <= "z":
            out += chr((ord(ch) - 97 + shift) % 26 + 97)
        elif "A" <= ch <= "Z":
            out += chr((ord(ch) - 65 + shift) % 26 + 65)
        else:
            out += ch
    return out


def cases():
    c = [("hello", 3), ("Hello World!", 1), ("xyz", 3), ("ABC123def", 5), ("", 10), ("abc", -3), ("abc", 26),
         ("abc", 0), ("Zz", 1), ("Aa", -1), ("hello", 52), ("hello", -27), ("The quick brown fox!", 13)]
    rng = random.Random(4314)
    for _ in range(25):
        c.append(("".join(rng.choice("abcxyzABCXYZ 1!") for _ in range(rng.randint(0, 15))), rng.randint(-60, 60)))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

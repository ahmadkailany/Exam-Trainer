import random

from engine.pygrader import grade_function

FUNC = "inter"
FORBIDDEN = []

def reference(s1, s2):
    out = ""
    for ch in s1:
        if ch in s2 and ch not in out:
            out += ch
    return out


def cases():
    c = [("hello", "world"), ("banana", "band"), ("abcabc", "bc"), ("abc", "xyz"), ("", "abc"), ("abc", ""),
         ("", ""), ("padinton", "paqefwtdjetyiytjneytjoeyjnejeyj"), ("aAbB", "AB"), ("a b", " "), ("1122", "21")]
    rng = random.Random(4306)
    for _ in range(25):
        c.append(("".join(rng.choice("abcdeAB 12") for _ in range(rng.randint(0, 12))),
                  "".join(rng.choice("abcdeAB 12") for _ in range(rng.randint(0, 12)))))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

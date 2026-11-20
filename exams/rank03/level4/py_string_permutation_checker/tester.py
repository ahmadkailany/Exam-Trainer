import random

from engine.pygrader import grade_function

FUNC = "string_permutation_checker"
FORBIDDEN = []

def reference(s1, s2):
    counts = {}
    for ch in s1:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in s2:
        counts[ch] = counts.get(ch, 0) - 1
    return all(v == 0 for v in counts.values())


def cases():
    c = [("abc", "bca"), ("abc", "def"), ("listen", "silent"), ("hello", "bello"), ("", ""), ("a", ""),
         ("Abc", "abc"), ("a gentleman", "elegant man"), ("a b", "ab "), ("a b", "ab"), ("!?", "?!"), ("aab", "abb")]
    rng = random.Random(4311)
    for _ in range(25):
        s = "".join(rng.choice("abcAB !") for _ in range(rng.randint(0, 10)))
        t = list(s)
        rng.shuffle(t)
        t = "".join(t)
        if rng.random() < .35:
            t = t[:-1] + rng.choice("abcAB !") if t else "x"
        c.append((s, t))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

import random

from engine.pygrader import grade_function

FUNC = "anagram"
FORBIDDEN = []

def _norm(s):
    counts = {}
    for ch in s.lower():
        if ch != " ":
            counts[ch] = counts.get(ch, 0) + 1
    return counts


def reference(s1, s2):
    return _norm(s1) == _norm(s2)


def cases():
    c = [("listen", "silent"), ("Triangle", "Integral"), ("Dormitory", "Dirty Room"), ("hello", "world"),
         ("", ""), ("abc", "abcc"), ("a", "A"), ("  ", ""), ("abc", "cab "), ("aab", "abb"), ("School master", "The classroom"),
         ("Astronomer", "Moon starer"), ("abc", "abd")]
    rng = random.Random(4309)
    for _ in range(25):
        s = "".join(rng.choice("abcdeAB") for _ in range(rng.randint(0, 10)))
        t = list(s)
        rng.shuffle(t)
        t = "".join(t)
        if rng.random() < .3:
            t = t.swapcase()
        if rng.random() < .3:
            t = t.replace("a", "a ", 1)
        if rng.random() < .3:
            t += rng.choice("abz")
        c.append((s, t))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

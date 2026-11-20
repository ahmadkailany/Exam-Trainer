import random

from engine.pygrader import grade_function

FUNC = "hidenp"
FORBIDDEN = []

def reference(small, big):
    i = 0
    for ch in big:
        if i < len(small) and small[i] == ch:
            i += 1
    return i == len(small)


def cases():
    c = [("abc", "a1b2c3"), ("ace", "abcde"), ("aec", "abcde"), ("", "abc"), ("abc", "ab"), ("aaaa", "aaa"),
         ("sing", "subsequence testing"), ("", ""), ("a", ""), ("ABC", "abc"), ("abc", "abc"), ("cba", "abc"),
         ("aa", "a_a"), (" ", "a b")]
    rng = random.Random(4305)
    for _ in range(30):
        big = "".join(rng.choice("abcAB ") for _ in range(rng.randint(0, 15)))
        if big and rng.random() < .6:
            idx = sorted(rng.sample(range(len(big)), rng.randint(1, len(big))))
            small = "".join(big[i] for i in idx)
        else:
            small = "".join(rng.choice("abc") for _ in range(rng.randint(0, 4)))
        c.append((small, big))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

import random

from engine.pygrader import grade_function

FUNC = "palindrome_partitioner"


def reference(s):
    n = len(s)
    if n <= 1:
        return 0
    # pal[i][j] -> s[i..j] is a palindrome
    pal = [[False] * n for _ in range(n)]
    cuts = [0] * n
    for j in range(n):
        best = j
        for i in range(j + 1):
            if s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1]):
                pal[i][j] = True
                best = 0 if i == 0 else min(best, cuts[i - 1] + 1)
        cuts[j] = best
    return cuts[-1]


def cases():
    c = [
        # subject examples
        ("aab",), ("aba",), ("abc",),
        # edge cases
        ("",), ("a",), ("aa",), ("ab",),
        ("racecar",), ("abba",), ("abcd",),
        ("aabb",), ("abacdc",), ("banana",),
        ("noonabbad",), ("abcba",), ("aaaaaaaaab",),
        ("ababbbabbababa",),              # classic: answer 3
        ("cabababcbc",),                  # greedy-longest-first gives the wrong answer here
        ("efe",), ("coder",), ("leet",),
        ("AbA",), ("Aa",),                # case-sensitive
        ("a b a",), ("12321",),
    ]
    rng = random.Random(4246)
    for _ in range(30):
        n = rng.randint(1, 18)
        c.append(("".join(rng.choice("ab" if rng.random() < 0.5 else "abc") for _ in range(n)),))
    return c


def grade(path):
    rng = random.Random(99)
    big1 = "".join(rng.choice("ab") for _ in range(600))
    big2 = "a" * 400 + "b" + "a" * 399
    big3 = "".join(chr(97 + i % 26) for i in range(500))
    return grade_function(path, FUNC, reference, cases(), no_imports=True,
                          perf_cases=[(big1,), (big2,), (big3,)])

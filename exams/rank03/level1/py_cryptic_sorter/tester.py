import random

from engine.pygrader import grade_function

FUNC = "cryptic_sorter"
FORBIDDEN = ['sorted', '.sort']

VOWELS = "aeiouAEIOU"


def _key(s, fold):
    return (len(s), "".join(fold(ch) if ch.isalpha() else ch for ch in s), sum(ch in VOWELS for ch in s))


def _stable_sort(strings, fold):
    out = []
    for s in strings:  # insertion sort keeps equal strings in input order
        k = _key(s, fold)
        i = len(out)
        while i > 0 and _key(out[i - 1], fold) > k:
            i -= 1
        out.insert(i, s)
    return out


def reference(strings):
    return _stable_sort(strings, str.lower)


def reference_upper(strings):
    """Also accepted: letters folded to UPPER case (only differs for symbols between Z and a)."""
    return _stable_sort(strings, str.upper)


def cases():
    c = [(["apple", "cat", "banana", "dog", "elephant"],), (["aaa", "bbb", "AAA", "BBB"],),
         (["hello", "world", "hi", "test"],), ([],), ([""],), (["b", "a", "B", "A"],), (["same", "same", "SAME"],),
         (["abc", "ab", "a", ""],), (["Zeta", "alpha", "Beta", "gamma"],), (["x1", "x0", "X2", "10", "9"],)]
    rng = random.Random(4302)
    for _ in range(25):
        c.append(([("".join(rng.choice("abcABCxyz019") for _ in range(rng.randint(0, 5))))
                   for _ in range(rng.randint(0, 9))],))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True, alt_references=[reference_upper])

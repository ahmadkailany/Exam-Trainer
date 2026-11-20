import random

from engine.pygrader import grade_function

NAMES = ['trie_autocomplete']
FORBIDDEN = []

def reference(words, prefix):
    found = []
    for w in words:
        if w.startswith(prefix) and w not in found:
            found.append(w)
    out = []
    for w in found:  # insertion sort -> alphabetical
        i = len(out)
        while i > 0 and out[i - 1] > w:
            i -= 1
        out.insert(i, w)
    return out


def cases():
    c = [(["apple", "app", "apricot", "banana"], "app"), (["apple", "app", "apricot", "banana"], "ban"),
         (["hello", "world", "help", "heap"], "he"), (["test"], "xyz"), (["cat", "car", "card", "care"], "car"),
         ([], "test"), (["a", "ab", "abc"], ""), (["dup", "dup", "duo"], "du"), (["Apple", "apple"], "a"),
         (["Apple", "apple"], "A"), (["zeta", "alpha", "beta"], ""), (["abc"], "abcd")]
    rng = random.Random(4608)
    for _ in range(20):
        words = ["".join(rng.choice("abAB") for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(0, 10))]
        c.append((words, "".join(rng.choice("abA") for _ in range(rng.randint(0, 2)))))
    return c


def grade(path):
    return grade_function(path, NAMES, reference, cases(), forbidden=FORBIDDEN)

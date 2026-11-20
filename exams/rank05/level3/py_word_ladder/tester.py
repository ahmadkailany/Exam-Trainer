import random

from engine.pygrader import grade_function

NAMES = ['word_ladder']
FORBIDDEN = []

def reference(start, end, sentence):
    words = set(sentence)
    if end not in words:
        return 0
    frontier, seen, depth = [start], {start}, 1
    while frontier:
        nxt = []
        for w in frontier:
            if w == end:
                return depth
            for i in range(len(w)):
                for ch in "abcdefghijklmnopqrstuvwxyz":
                    cand = w[:i] + ch + w[i + 1:]
                    if cand in words and cand not in seen:
                        seen.add(cand)
                        nxt.append(cand)
        frontier, depth = nxt, depth + 1
    return 0


def cases():
    c = [("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), ("hit", "cog", ["hot", "dot", "dog", "lot", "log"]),
         ("a", "c", ["a", "b", "c"]), ("hot", "dog", ["hot", "dog"]), ("hot", "dot", ["dot"]), ("abc", "xyz", []),
         ("lost", "cost", ["most", "fist", "lost", "cost", "fish"]), ("cold", "warm", ["cord", "card", "ward", "warm", "wold", "word", "worm", "corm"])]
    rng = random.Random(4506)
    for _ in range(15):
        L = rng.randint(2, 3)
        words = ["".join(rng.choice("abc") for _ in range(L)) for _ in range(rng.randint(3, 12))]
        start = "".join(rng.choice("abc") for _ in range(L))
        end = rng.choice(words)
        if end != start:
            c.append((start, end, words))
    return c


def grade(path):
    return grade_function(path, NAMES, reference, cases(), forbidden=FORBIDDEN)

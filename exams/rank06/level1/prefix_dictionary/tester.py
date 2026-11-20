import random

from engine.pygrader import grade_function

NAMES = ['PrefixDictionary']
FORBIDDEN = []

class PrefixDictionary:
    def __init__(self):
        self.words = set()

    def insert(self, word):
        self.words.add(word)

    def search(self, word):
        return word in self.words

    def starts_with(self, prefix):
        return any(w.startswith(prefix) for w in self.words)


REF_NS = {"PrefixDictionary": PrefixDictionary}


def cases():
    c = [{"cls": "PrefixDictionary", "ops": [["insert", ["apple"]], ["search", ["apple"]], ["search", ["app"]],
                                             ["starts_with", ["app"]], ["insert", ["app"]], ["search", ["app"]]]},
         {"cls": "PrefixDictionary", "ops": [["search", ["a"]], ["starts_with", ["a"]]]},
         {"cls": "PrefixDictionary", "ops": [["insert", ["abc"]], ["starts_with", ["abcd"]], ["search", ["ab"]],
                                             ["starts_with", ["abc"]], ["insert", ["abc"]], ["search", ["abc"]]]}]
    rng = random.Random(4601)
    w = lambda: "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
    for _ in range(20):
        ops = []
        for _ in range(rng.randint(3, 15)):
            ops.append([rng.choice(["insert", "insert", "search", "starts_with"]), [w()]])
        c.append({"cls": "PrefixDictionary", "ops": ops})
    return c


def grade(path):
    return grade_function(path, NAMES, None, cases(), forbidden=FORBIDDEN, ref_ns=REF_NS)

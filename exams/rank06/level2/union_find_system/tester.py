import random

from engine.pygrader import grade_function

NAMES = ['UnionFind']
FORBIDDEN = []

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)


REF_NS = {"UnionFind": UnionFind}


def cases():
    c = [{"cls": "UnionFind", "init": [5], "ops": [["connected", [0, 1]]]},
         {"cls": "UnionFind", "init": [5], "ops": [["union", [0, 1]], ["connected", [0, 1]], ["union", [1, 2]],
                                                    ["connected", [0, 2]], ["union", [0, 1]], ["union", [0, 2]]]},
         {"cls": "UnionFind", "init": [3], "ops": [["union", [0, 1]], ["union", [1, 2]], ["__same__", [0, 2]]]},
         {"cls": "UnionFind", "init": [1], "ops": [["connected", [0, 0]], ["union", [0, 0]], ["__same__", [0, 0]]]}]
    rng = random.Random(4605)
    for _ in range(20):
        n = rng.randint(2, 12)
        ops = []
        for _ in range(rng.randint(3, 20)):
            op = rng.choice(["union", "union", "connected", "__same__"])
            ops.append([op, [rng.randrange(n), rng.randrange(n)]])
        c.append({"cls": "UnionFind", "init": [n], "ops": ops})
    return c


def grade(path):
    return grade_function(path, NAMES, None, cases(), forbidden=FORBIDDEN, ref_ns=REF_NS)

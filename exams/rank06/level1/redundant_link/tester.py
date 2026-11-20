import random

from engine.pygrader import grade_function

NAMES = ['redundant_link']
FORBIDDEN = []

def reference(edges):
    parent = list(range(len(edges) + 2))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return [u, v]
        parent[ru] = rv
    return []


def cases():
    c = [([[1, 2], [1, 3], [2, 3]],), ([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],), ([[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]],),
         ([[1, 2], [2, 1]],), ([[2, 3], [1, 2], [1, 3]],)]
    rng = random.Random(4604)
    for _ in range(20):
        n = rng.randint(3, 10)
        edges = [[rng.randint(1, i - 1), i] for i in range(2, n + 1)]
        u, v = rng.sample(range(1, n + 1), 2)
        while [u, v] in edges or [v, u] in edges:
            u, v = rng.sample(range(1, n + 1), 2)
        edges.append([u, v])
        rng.shuffle(edges)
        c.append(([e if rng.random() < .5 else e[::-1] for e in edges],))
    return c


def grade(path):
    return grade_function(path, NAMES, reference, cases(), forbidden=FORBIDDEN)

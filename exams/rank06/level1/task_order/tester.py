import random

from engine.pygrader import grade_function

NAMES = ['task_order']
FORBIDDEN = ['graphlib.TopologicalSorter']

def reference(n, prereqs):
    indeg = [0] * n
    nxt = [[] for _ in range(n)]
    for a, b in prereqs:
        nxt[b].append(a)
        indeg[a] += 1
    ready = [i for i in range(n) if indeg[i] == 0]
    order = []
    while ready:
        u = min(ready)
        ready.remove(u)
        order.append(u)
        for v in nxt[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    return order if len(order) == n else []


def cases():
    c = [(2, [[1, 0]]), (4, [[1, 0], [2, 0], [3, 1], [3, 2]]), (2, [[0, 1], [1, 0]]), (3, []), (1, []), (0, []),
         (1, [[0, 0]]), (3, [[0, 2], [1, 2]]), (5, [[0, 4], [4, 3], [3, 2], [2, 1]]), (4, [[3, 0], [1, 3], [2, 1]]),
         (3, [[1, 0], [2, 1], [0, 2]])]
    rng = random.Random(4603)
    for _ in range(20):
        n = rng.randint(1, 8)
        perm = list(range(n))
        rng.shuffle(perm)
        pairs = set()
        for _ in range(rng.randint(0, n * 2)):
            i, j = sorted(rng.sample(range(n), 2)) if n > 1 else (0, 0)
            if i != j:
                pairs.add((perm[j], perm[i]))
        if rng.random() < .25 and n > 1:
            i, j = rng.sample(range(n), 2)
            pairs.add((perm[i], perm[j]))
            pairs.add((perm[j], perm[i]))
        c.append((n, [list(p) for p in sorted(pairs)]))
    return c


def grade(path):
    return grade_function(path, NAMES, reference, cases(), forbidden=FORBIDDEN)

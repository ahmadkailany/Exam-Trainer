import random

from engine.pygrader import grade_function

NAMES = ['bridge_finder']
FORBIDDEN = []

def reference(graph):
    nodes = set(graph)
    for vs in graph.values():
        nodes.update(vs)
    edges = {(min(u, v), max(u, v)) for u in graph for v in graph[u] if u != v}

    def components(skip):
        adj = {n: set() for n in nodes}
        for a, b in edges:
            if (a, b) != skip:
                adj[a].add(b)
                adj[b].add(a)
        seen, count = set(), 0
        for n in nodes:
            if n not in seen:
                count += 1
                stack = [n]
                seen.add(n)
                while stack:
                    x = stack.pop()
                    for y in adj[x]:
                        if y not in seen:
                            seen.add(y)
                            stack.append(y)
        return count

    base = components(None)
    return sorted(e for e in edges if components(e) > base)


def cases():
    c = [({0: [1, 2], 1: [0, 2], 2: [0, 1]},), ({0: [1], 1: [0, 2], 2: [1]},), ({0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1]},),
         ({},), ({0: [1], 1: [0]},), ({0: [1, 2], 1: [0, 2, 3, 4], 2: [0, 1], 3: [1, 4], 4: [1, 3]},),
         ({0: []},), ({0: [1], 1: [0], 2: [3], 3: [2]},), ({3: [1], 1: [3, 2], 2: [1]},)]
    rng = random.Random(4609)
    for _ in range(20):
        n = rng.randint(2, 9)
        g = {i: [] for i in range(n)}
        for _ in range(rng.randint(1, n + 3)):
            a, b = rng.sample(range(n), 2)
            if b not in g[a]:
                g[a].append(b)
                g[b].append(a)
        c.append((g,))
    return c


def grade(path):
    return grade_function(path, NAMES, reference, cases(), forbidden=FORBIDDEN)

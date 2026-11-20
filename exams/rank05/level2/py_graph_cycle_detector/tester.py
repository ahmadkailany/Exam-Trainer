import random

from engine.pygrader import grade_function

NAMES = ['py_graph_cycle_detector']
FORBIDDEN = ['graphlib.TopologicalSorter']

def reference(graph):
    nodes = set(graph)
    for vs in graph.values():
        nodes.update(vs)
    state = {n: 0 for n in nodes}       # 0 new, 1 in stack, 2 done

    def dfs(u):
        state[u] = 1
        for v in graph.get(u, []):
            if state[v] == 1 or (state[v] == 0 and dfs(v)):
                return True
        state[u] = 2
        return False

    return any(state[n] == 0 and dfs(n) for n in sorted(nodes))


def cases():
    c = [({0: [1], 1: [2], 2: [0]},), ({0: [1], 1: [2], 2: []},), ({},), ({0: [0]},), ({0: [1], 1: [0]},),
         ({0: [1, 2], 1: [3], 2: [3], 3: []},), ({0: [1], 1: [], 2: [3], 3: [2]},), ({0: [1]},), ({5: []},),
         ({0: [1], 1: [2], 2: [3], 3: [1]},), ({0: [], 1: [], 2: []},)]
    rng = random.Random(4502)
    for _ in range(25):
        n = rng.randint(1, 8)
        dag = rng.random() < .5
        g = {}
        for u in range(n):
            pool = list(range(u + 1, n)) if dag else list(range(n))
            g[u] = rng.sample(pool, rng.randint(0, min(3, len(pool))))
        c.append((g,))
    return c


def grade(path):
    return grade_function(path, NAMES, reference, cases(), forbidden=FORBIDDEN)

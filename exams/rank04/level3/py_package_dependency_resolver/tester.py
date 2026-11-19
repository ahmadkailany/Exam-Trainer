import random

from engine.pygrader import grade_function

FUNC = "package_dependency_resolver"
FORBIDDEN = ["graphlib", "TopologicalSorter"]


def _graph(packages):
    indeg = {p: 0 for p in packages}
    users = {p: [] for p in packages}
    for p, deps in packages.items():
        for d in set(deps):
            if d in packages:
                indeg[p] += 1
                users[d].append(p)
    return indeg, users


def reference(packages):
    """Kahn's algorithm, FIFO queue, alphabetical tie-breaking."""
    indeg, users = _graph(packages)
    queue = sorted(p for p in packages if indeg[p] == 0)
    order = []
    while queue:
        p = queue.pop(0)
        order.append(p)
        for u in sorted(users[p]):
            indeg[u] -= 1
            if indeg[u] == 0:
                queue.append(u)
    return order if len(order) == len(packages) else []


def reference_waves(packages):
    """Also accepted: process level by level, each level sorted alphabetically."""
    indeg, users = _graph(packages)
    wave = sorted(p for p in packages if indeg[p] == 0)
    order = []
    while wave:
        order.extend(wave)
        nxt = []
        for p in wave:
            for u in users[p]:
                indeg[u] -= 1
                if indeg[u] == 0:
                    nxt.append(u)
        wave = sorted(nxt)
    return order if len(order) == len(packages) else []


def cases():
    c = [
        # subject examples
        ({"app": ["database"], "database": ["driver"], "driver": []},),
        ({"A": [], "B": ["A"], "C": ["A", "B"]},),
        ({},),
        ({"X": ["Y"], "Y": ["X"]},),
        ({"web": [], "api": [], "frontend": ["web"], "backend": ["api"]},),
        # edge cases
        ({"solo": []},),
        ({"A": ["A"]},),                                  # self dependency
        ({"A": [], "B": ["B"]},),                         # self dependency elsewhere
        ({"A": ["ghost"]},),                              # missing dependency ignored
        ({"b": ["missing", "a"], "a": ["nope"]},),
        ({"c": [], "b": [], "a": []},),                   # all independent -> alphabetical
        ({"A": ["B"], "B": ["C"], "C": ["A"]},),          # 3-cycle
        ({"A": [], "B": ["A"], "C": ["D"], "D": ["C"]},), # cycle in one part only
        ({"z": ["y"], "y": ["x"], "x": []},),
        ({"lib": [], "app": ["lib", "util"], "util": ["lib"]},),
        ({"d": ["b", "c"], "c": ["a"], "b": ["a"], "a": []},),
        ({"m": [], "n": ["m"], "a": [], "b": ["a"]},),
    ]
    rng = random.Random(4247)
    for _ in range(30):
        n = rng.randint(1, 8)
        names = rng.sample(["alpha", "beta", "core", "delta", "echo", "fox", "gui", "http", "io", "json"], n)
        acyclic = rng.random() < 0.75
        pkgs = {}
        for i, name in enumerate(names):
            pool = names[:i] if acyclic else names
            deps = rng.sample(pool, rng.randint(0, min(3, len(pool)))) if pool else []
            if rng.random() < 0.15:
                deps.append("missing_pkg")
            pkgs[name] = deps
        c.append((pkgs,))
    return c


def grade(path):
    big = {f"p{i:04d}": ([f"p{i - 1:04d}"] if i else []) for i in range(1500)}
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN,
                          alt_references=[reference_waves], perf_cases=[(big,)])

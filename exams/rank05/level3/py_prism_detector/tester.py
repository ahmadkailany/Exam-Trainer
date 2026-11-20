import random

from engine.pygrader import grade_function

NAMES = ['prism_detector']
FORBIDDEN = []

DIRS = [((1, 0), "H"), ((-1, 0), "H-"), ((0, 1), "V"), ((0, -1), "V-"),
        ((1, 1), "D1"), ((-1, -1), "D1-"), ((-1, 1), "D2"), ((1, -1), "D2-")]


def _search(grid, pattern, dirs):
    out = []
    if not grid or not pattern:
        return out
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            for (dx, dy), code in dirs:
                ok = True
                for k, ch in enumerate(pattern):
                    nx, ny = x + dx * k, y + dy * k
                    if not (0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and grid[ny][nx] == ch):
                        ok = False
                        break
                if ok:
                    out.append((x, y, code))
    return out


def reference(grid, pattern):
    return _search(grid, pattern, DIRS)


def ref_swapped_d2(grid, pattern):
    """The subject's D2 / D2- descriptions contradict their vectors: accept both readings."""
    swap = {"D2": "D2-", "D2-": "D2"}
    return _search(grid, pattern, [(v, swap.get(c, c)) for v, c in DIRS])


def cases():
    c = [(["CAT", "A..", "T.."], "CAT"), ([], "CAT"), (["CAT"], ""), (["TAC"], "CAT"), (["ABA"], "ABA"),
         (["C..", ".A.", "..T"], "CAT"), (["..T", ".A.", "C.."], "CAT"), (["T..", ".A.", "..C"], "CAT"),
         (["..C", ".A.", "T.."], "CAT"), (["CATS"], "CATSS"), (["XX", "XX"], "XX")]
    rng = random.Random(4505)
    for _ in range(20):
        w, h = rng.randint(2, 7), rng.randint(2, 6)
        grid = ["".join(rng.choice("ABC") for _ in range(w)) for _ in range(h)]
        c.append((grid, "".join(rng.choice("ABC") for _ in range(rng.randint(2, 3)))))
    return c


def grade(path):
    return grade_function(path, NAMES, reference, cases(), forbidden=FORBIDDEN, compare="value", normalize=sorted, alt_references=[ref_swapped_d2])

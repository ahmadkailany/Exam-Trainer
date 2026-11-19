import random

from engine.pygrader import grade_function

FUNC = "constellation_mapper"


def reference(stars, dim):
    grid = [["."] * dim for _ in range(dim)]
    for r, c in stars:
        if 0 <= r < dim and 0 <= c < dim:
            grid[r][c] = "*"
    return ["".join(row) for row in grid]


def cases():
    c = [
        # subject examples
        ([(0, 0), (1, 1), (2, 2)], 3),
        ([(1, 1), (0, 1), (2, 1), (1, 0), (1, 2)], 3),
        ([], 2),
        ([(0, 0), (0, 0), (1, 1)], 2),
        ([(0, 0), (5, 5)], 3),
        ([(1, 0), (1, 1), (1, 2)], 3),
        # edge cases
        ([], 0),
        ([(0, 0)], 0),
        ([(0, 0)], 1),
        ([], 1),
        ([(-1, 0), (0, -1)], 3),          # negative coords must be ignored (no wrap-around!)
        ([(-1, -1)], 2),
        ([(3, 0), (0, 3)], 3),            # exactly on the boundary -> outside
        ([(2, 0)], 3),                    # (row, col): row 2, col 0 -> bottom-left
        ([(0, 2)], 3),                    # top-right
        ([(0, 0), (0, 1), (1, 0), (1, 1)], 2),
        ([(4, 4), (0, 4), (4, 0)], 5),
        ([(1, 2), (1, 2), (1, 2)], 4),
    ]
    rng = random.Random(4243)
    for _ in range(25):
        dim = rng.randint(1, 8)
        stars = [(rng.randint(-2, dim + 1), rng.randint(-2, dim + 1)) for _ in range(rng.randint(0, 12))]
        c.append((stars, dim))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), no_imports=True,
                          perf_cases=[([(i, i) for i in range(300)], 300)])

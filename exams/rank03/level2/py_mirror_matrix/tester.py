import random

from engine.pygrader import grade_function

FUNC = "mirror_matrix"
FORBIDDEN = []

def reference(matrix):
    return [row[::-1] for row in matrix]


def cases():
    c = [([[1, 2, 3], [4, 5, 6]],), ([[1, 2], [3, 4], [5, 6]],), ([[7]],), ([[1, 2, 3, 4]],),
         ([[-1, -2], [-3, -4]],), ([],), ([[]],), ([[1], [2], [3]],), ([[0, 0, 1], [1, 0, 0]],)]
    rng = random.Random(4304)
    for _ in range(15):
        w, h = rng.randint(1, 6), rng.randint(1, 6)
        c.append(([[rng.randint(-9, 9) for _ in range(w)] for _ in range(h)],))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

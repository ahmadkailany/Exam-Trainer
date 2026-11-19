import random

from engine.pygrader import grade_function

FUNC = "list_intersection_finder"


def reference(lists):
    if not lists:
        return []
    common = set(lists[0])
    for lst in lists[1:]:
        common &= set(lst)
    return sorted(common)


def cases():
    c = [
        # subject examples
        ([[1, 2, 3], [2, 3, 4], [2, 3, 5]],),
        ([[1, 2, 3, 4], [2, 4, 6, 8], [4, 8, 12]],),
        ([[1, 1, 2, 3], [1, 2, 2, 3], [1, 2, 3, 3]],),
        ([[1, 2, 3], [4, 5, 6]],),
        ([],),
        ([[1, 2, 3], []],),
        ([[5]],),
        # edge cases
        ([[]],),
        ([[], [1, 2]],),
        ([[1, 1, 1]],),                   # single list with duplicates -> deduped
        ([[3, 3, 2, 1]],),                # single list -> still sorted + unique
        ([[1, 2, 3], [1, 2, 3]],),
        ([[-3, -1, 0, 2], [-3, 0, 5], [-5, -3, 0]],),
        ([[1, 2], [2, 3], [3, 4]],),
        ([[1, 2, 3], [2], [2, 2, 2]],),
        ([[0], [0], [0], [0]],),
        ([[1, 5, 9], [1, 5, 9], [9]],),
    ]
    rng = random.Random(4244)
    for _ in range(30):
        lists = [sorted(rng.randint(-5, 15) for _ in range(rng.randint(0, 12)))
                 for _ in range(rng.randint(1, 5))]
        c.append((lists,))
    return c


def grade(path):
    big = [list(range(i, 20000, 1 + i % 3)) for i in range(5)]
    return grade_function(path, FUNC, reference, cases(), no_imports=True, perf_cases=[(big,)])

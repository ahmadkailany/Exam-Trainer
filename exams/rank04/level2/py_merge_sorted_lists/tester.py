import heapq
import random

from engine.pygrader import grade_function

FUNC = "merge_sorted_lists"
FORBIDDEN = ["sorted", ".sort", "heapq.merge"]


def reference(lists):
    return list(heapq.merge(*lists))


def cases():
    c = [
        # subject examples
        ([[1, 3, 5], [2, 4, 6]],),
        ([[1, 5, 9], [2, 3, 8], [4, 6, 7]],),
        ([[5], [1, 3], [2, 4]],),
        ([[1, 1, 2], [2, 3, 3]],),
        ([[], [1, 2, 3]],),
        ([[]],),
        ([[-5, -1, 0], [-3, 2, 4]],),
        ([[10], [10], [10]],),
        # edge cases
        ([],),
        ([[], [], []],),
        ([[1, 2, 3]],),
        ([[1, 2, 3], []],),
        ([[], [], [7]],),
        ([[1, 1, 1], [1, 1]],),
        ([[1, 2, 3], [4, 5, 6]],),
        ([[4, 5, 6], [1, 2, 3]],),
        ([[-10, -10], [-10, 0], [0, 10]],),
        ([[0]],),
        ([[1], [2], [3], [4], [5], [0]],),
    ]
    rng = random.Random(4245)
    for _ in range(30):
        lists = []
        for _ in range(rng.randint(0, 6)):
            lst = [rng.randint(-20, 20) for _ in range(rng.randint(0, 10))]
            lst.sort()
            lists.append(lst)
        c.append((lists,))
    return c


def _big():
    rng = random.Random(7)
    lists = []
    for _ in range(100):
        lst = [rng.randint(-10 ** 6, 10 ** 6) for _ in range(1000)]
        lst.sort()
        lists.append(lst)
    return lists


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN,
                          perf_cases=[(_big(),)])

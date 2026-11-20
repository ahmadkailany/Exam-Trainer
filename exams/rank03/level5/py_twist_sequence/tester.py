import random

from engine.pygrader import grade_function

FUNC = "twist_sequence"
FORBIDDEN = []

def reference(arr, k):
    if not arr:
        return []
    k %= len(arr)
    return arr[len(arr) - k:] + arr[:len(arr) - k]


def cases():
    c = [([1, 2, 3, 4, 5], 2), ([1, 2, 3], 1), ([1, 2, 3, 4], 0), ([1, 2, 3], 5), ([], 3), ([], 0), ([7], 100),
         ([1, 2], 2), ([1, 2, 3, 4, 5, 6], 6), ([1, 2, 3, 4, 5, 6], 7), ([9, 8, 7], 3)]
    rng = random.Random(4313)
    for _ in range(25):
        c.append(([rng.randint(-9, 9) for _ in range(rng.randint(0, 9))], rng.randint(0, 20)))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

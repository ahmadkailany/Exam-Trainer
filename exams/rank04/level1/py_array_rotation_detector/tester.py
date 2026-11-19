import random

from engine.pygrader import grade_function

FUNC = "array_rotation_detector"
FORBIDDEN = ["collections.deque.rotate", ".rotate"]


def reference(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    if not arr1:
        return True
    n = len(arr1)
    return any(arr1[i:] + arr1[:i] == arr2 for i in range(n))


def cases():
    c = [
        # subject examples
        ([1, 2, 3, 4, 5], [4, 5, 1, 2, 3]),
        ([1, 2, 3, 4, 5], [5, 1, 2, 3, 4]),
        ([1, 2, 3], [3, 2, 1]),
        ([1, 2], [1, 2, 3]),
        ([], []),
        # edge cases
        ([1, 2, 3], [1, 2, 3]),          # rotation by 0
        ([1], [1]),
        ([1], [2]),
        ([], [1]),
        ([1], []),
        ([1, 2, 3], [2, 3, 1]),          # left rotation
        ([1, 2, 3], [3, 1, 2]),          # right rotation
        ([1, 1, 2], [1, 2, 1]),          # duplicates
        ([1, 1, 2], [2, 1, 1]),
        ([1, 1, 2], [1, 2, 2]),          # same length, same set, not a rotation
        ([1, 2, 1, 2], [2, 1, 2, 1]),
        ([1, 2, 3, 4], [1, 3, 2, 4]),
        ([1, 2, 3, 4], [4, 3, 2, 1]),
        ([0, 0, 0], [0, 0, 0]),
        ([1, 2, 3], [1, 2, 4]),
        (["a", "b", "c"], ["c", "a", "b"]),
        (["a", "b", "c"], ["b", "a", "c"]),
        ([-1, -2, -3], [-3, -1, -2]),
        ([1, 2, 3, 4, 5, 6], [4, 5, 6, 1, 2, 3]),
        ([12, 3], [1, 23]),              # catches string-join tricks
        ([1, 23], [12, 3]),
    ]
    rng = random.Random(4242)
    for _ in range(40):
        n = rng.randint(1, 12)
        a = [rng.randint(0, 4) for _ in range(n)]
        k = rng.randint(0, n - 1)
        b = a[k:] + a[:k]
        if rng.random() < 0.4:
            b = b[:]
            b[rng.randrange(n)] = rng.randint(0, 4)
        c.append((a, b))
    return c


def grade(path):
    big = list(range(3000))
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN,
                          perf_cases=[(big, big[1234:] + big[:1234])])

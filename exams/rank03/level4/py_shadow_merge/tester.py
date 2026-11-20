import random

from engine.pygrader import grade_function

FUNC = "shadow_merge"
FORBIDDEN = []

def reference(list1, list2):
    out, i, j = [], 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            out.append(list1[i])
            i += 1
        else:
            out.append(list2[j])
            j += 1
    return out + list1[i:] + list2[j:]


def cases():
    c = [([1, 3, 5], [2, 4, 6]), ([1, 2, 3], [4, 5, 6]), ([1], [2, 3, 4]), ([], [1, 2, 3]), ([1, 1, 2], [1, 3, 3]),
         ([], []), ([1, 2, 3], []), ([-5, 0, 5], [-10, 10]), ([4, 5, 6], [1, 2, 3]), ([2, 2], [2, 2])]
    rng = random.Random(4310)
    for _ in range(25):
        a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 10))]
        b = [rng.randint(-20, 20) for _ in range(rng.randint(0, 10))]
        a.sort()
        b.sort()
        c.append((a, b))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

import random
from collections import deque

from engine.pygrader import grade_function

FUNC = "sliding_window_maximum"


def reference(nums, k):
    if not nums or k <= 0 or k > len(nums):
        return []
    dq, out = deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


def cases():
    c = [
        # subject examples
        ([1, 3, -1, -3, 5, 3, 6, 7], 3),
        ([1, 2, 3, 4, 5], 2),
        ([5, 4, 3, 2, 1], 1),
        ([1, 2, 3], 3),
        ([1, 2, 3], 4),
        ([], 2),
        ([1, 2, 3], 0),
        # edge cases
        ([], 0),
        ([1, 2, 3], -1),
        ([7], 1),
        ([7], 2),
        ([-1, -5, -3], 2),
        ([-7, -8, -9, -1], 4),
        ([2, 2, 2, 2], 2),
        ([9, 1, 1, 1, 1], 2),
        ([1, 1, 1, 1, 9], 4),
        ([4, 3, 5, 4, 3, 3, 6, 7], 3),
        ([1, -1], 1),
        ([10, 9, 8, 7, 6, 5], 3),
        ([1, 3, 1, 2, 0, 5], 3),
    ]
    rng = random.Random(4248)
    for _ in range(40):
        n = rng.randint(0, 20)
        nums = [rng.randint(-10, 10) for _ in range(n)]
        c.append((nums, rng.randint(-1, n + 1)))
    return c


def grade(path):
    # No big-input / complexity check for this subject: correctness only.
    return grade_function(path, FUNC, reference, cases(), no_imports=True)

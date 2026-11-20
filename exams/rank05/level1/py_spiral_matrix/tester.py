import random

from engine.pygrader import grade_function

NAMES = ['generate_spiral']
FORBIDDEN = []

def reference(n):
    m = [[0] * n for _ in range(n)]
    top, bottom, left, right, k = 0, n - 1, 0, n - 1, 1
    while top <= bottom and left <= right:
        for x in range(left, right + 1):
            m[top][x] = k; k += 1
        top += 1
        for y in range(top, bottom + 1):
            m[y][right] = k; k += 1
        right -= 1
        if top <= bottom:
            for x in range(right, left - 1, -1):
                m[bottom][x] = k; k += 1
            bottom -= 1
        if left <= right:
            for y in range(bottom, top - 1, -1):
                m[y][left] = k; k += 1
            left += 1
    return m


def cases():
    return [(n,) for n in (3, 1, 2, 4, 5, 6, 7, 8, 10, 13)]


def grade(path):
    return grade_function(path, NAMES, reference, cases(), forbidden=FORBIDDEN)

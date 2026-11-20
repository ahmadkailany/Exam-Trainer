import random

from engine.pygrader import grade_function

NAMES = ['island_matrix_counter']
FORBIDDEN = []

def reference(matrix):
    if not matrix:
        return 0
    seen = set()
    count = 0
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == "1" and (y, x) not in seen:
                count += 1
                stack = [(y, x)]
                seen.add((y, x))
                while stack:
                    cy, cx = stack.pop()
                    for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                        if 0 <= ny < len(matrix) and 0 <= nx < len(matrix[ny]) and matrix[ny][nx] == "1" \
                                and (ny, nx) not in seen:
                            seen.add((ny, nx))
                            stack.append((ny, nx))
    return count


def cases():
    c = [([["1", "1", "1", "1", "0"], ["1", "1", "1", "0", "0"], ["1", "1", "1", "1", "0"], ["0", "0", "0", "0", "0"]],),
         ([["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]],),
         ([],), ([[]],), ([["0"]],), ([["1"]],), ([["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]],),
         ([["1", "1", "1"], ["1", "0", "1"], ["1", "1", "1"]],)]
    rng = random.Random(4504)
    for _ in range(20):
        w, h = rng.randint(1, 9), rng.randint(1, 7)
        c.append(([[rng.choice("0011") for _ in range(w)] for _ in range(h)],))
    return c


def grade(path):
    return grade_function(path, NAMES, reference, cases(), forbidden=FORBIDDEN)

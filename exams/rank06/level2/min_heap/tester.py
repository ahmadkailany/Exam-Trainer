import random

from engine.pygrader import grade_function

NAMES = ['MinHeap']
FORBIDDEN = ['heapq']

class MinHeap:
    def __init__(self):
        self.items = []

    def push(self, val):
        self.items.append(val)

    def pop(self):
        if not self.items:
            return None
        m = min(self.items)
        self.items.remove(m)
        return m

    def peek(self):
        return min(self.items) if self.items else None

    def size(self):
        return len(self.items)


REF_NS = {"MinHeap": MinHeap}


def cases():
    c = [{"cls": "MinHeap", "ops": [["push", [5]], ["push", [3]], ["push", [8]], ["peek", []], ["pop", []], ["peek", []],
                                    ["size", []]]},
         {"cls": "MinHeap", "ops": [["pop", []], ["peek", []], ["size", []]]},
         {"cls": "MinHeap", "ops": [["push", [1]], ["push", [1]], ["pop", []], ["pop", []], ["pop", []], ["size", []]]},
         {"cls": "MinHeap", "ops": [["push", [-5]], ["push", [0]], ["push", [-10]], ["pop", []], ["pop", []], ["pop", []]]}]
    rng = random.Random(4607)
    for _ in range(20):
        ops = []
        for _ in range(rng.randint(5, 40)):
            ops.append(rng.choice([["push", [rng.randint(-50, 50)]], ["push", [rng.randint(-50, 50)]],
                                   ["pop", []], ["peek", []], ["size", []]]))
        c.append({"cls": "MinHeap", "ops": ops})
    return c


def grade(path):
    return grade_function(path, NAMES, None, cases(), forbidden=FORBIDDEN, ref_ns=REF_NS)

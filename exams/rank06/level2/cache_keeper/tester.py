import random

from engine.pygrader import grade_function

NAMES = ['CacheKeeper']
FORBIDDEN = ['collections.OrderedDict']

class CacheKeeper:
    def __init__(self, capacity):
        self.cap = capacity
        self.data = {}

    def get(self, key):
        if key not in self.data:
            return -1
        v = self.data.pop(key)
        self.data[key] = v
        return v

    def put(self, key, value):
        self.data.pop(key, None)
        self.data[key] = value
        if len(self.data) > self.cap:
            del self.data[next(iter(self.data))]


REF_NS = {"CacheKeeper": CacheKeeper}


def cases():
    c = [{"cls": "CacheKeeper", "init": [2], "ops": [["put", [1, 1]], ["put", [2, 2]], ["get", [1]]]},
         {"cls": "CacheKeeper", "init": [2], "ops": [["put", [1, 1]], ["put", [2, 2]], ["put", [3, 3]], ["get", [1]]]},
         {"cls": "CacheKeeper", "init": [2], "ops": [["put", [1, 1]], ["put", [2, 2]], ["get", [1]], ["put", [3, 3]],
                                                     ["get", [2]], ["get", [1]], ["get", [3]]]},
         {"cls": "CacheKeeper", "init": [2], "ops": [["put", [1, 1]], ["put", [2, 2]], ["put", [1, 10]], ["put", [3, 3]],
                                                     ["get", [1]], ["get", [2]]]},
         {"cls": "CacheKeeper", "init": [1], "ops": [["put", [1, 1]], ["put", [2, 2]], ["get", [1]], ["get", [2]]]},
         {"cls": "CacheKeeper", "init": [3], "ops": [["get", [7]]]}]
    rng = random.Random(4606)
    for _ in range(20):
        ops = []
        for _ in range(rng.randint(4, 25)):
            if rng.random() < .55:
                ops.append(["put", [rng.randint(1, 6), rng.randint(0, 99)]])
            else:
                ops.append(["get", [rng.randint(1, 6)]])
        c.append({"cls": "CacheKeeper", "init": [rng.randint(1, 4)], "ops": ops})
    return c


def grade(path):
    return grade_function(path, NAMES, None, cases(), forbidden=FORBIDDEN, ref_ns=REF_NS)

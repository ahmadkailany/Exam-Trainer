import random

from engine.pygrader import grade_function

FUNC = "bracket_validator"
FORBIDDEN = []

def reference(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for c in s:
        if c in "([{":
            stack.append(c)
        elif c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
    return not stack


def cases():
    c = [("()",), ("()[]{}",), ("(]",), ("([)]",), ("{[]}",), ("hello(world)",), ("((())",), ("",),
         (")(",), ("]",), ("[",), ("{[()()]}",), ("{[(])}",), ("no brackets at all",), ("((((((((((",),
         ("a(b[c{d}e]f)g",), ("())",), ("(()",), ("}{",)]
    rng = random.Random(4301)
    for _ in range(40):
        c.append(("".join(rng.choice("()[]{}ab") for _ in range(rng.randint(0, 14))),))
    for _ in range(10):  # some guaranteed-valid ones
        s = ""
        for _ in range(rng.randint(1, 5)):
            o, cl = rng.choice(["()", "[]", "{}"])
            s = rng.choice([o + s + cl, s + o + cl])
        c.append((s,))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

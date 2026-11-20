import random

from engine.pygrader import grade_function

FUNC = "echo_validator"
FORBIDDEN = []

def reference(text):
    cleaned = [c.lower() for c in text if c.isalpha()]
    return len(cleaned) > 0 and cleaned == cleaned[::-1]


def cases():
    c = [("racecar",), ("A man a plan a canal Panama",), ("race a car",), ("Was it a car or a cat I saw",),
         ("hello",), ("Madam Im Adam",), ("madam",), ("Able was I ere I saw Elba",), ("",),
         ("a",), ("Aa",), ("ab",), ("No lemon, no melon",), ("Step on no pets!",), ("abcba1",), ("ab1ba",),
         ("Never odd or even",), ("palindrome",)]
    rng = random.Random(4303)
    for _ in range(20):
        half = "".join(rng.choice("abcAB") for _ in range(rng.randint(1, 5)))
        s = half + rng.choice(["", "x", "Y"]) + half[::-1].swapcase()
        if rng.random() < .4:
            s = s.replace("a", " a", 1)
        if rng.random() < .3:
            s += "q"
        c.append((s,))
    return c


def grade(path):
    return grade_function(path, FUNC, reference, cases(), forbidden=FORBIDDEN, no_imports=True)

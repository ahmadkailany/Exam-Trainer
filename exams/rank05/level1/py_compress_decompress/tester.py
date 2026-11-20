import random

from engine.pygrader import grade_function

NAMES = ['compress', 'decompress']
FORBIDDEN = []

def compress(s):
    out, i = "", 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out += s[i] + (str(j - i) if j - i > 1 else "")
        i = j
    return out


def decompress(s):
    out, i = "", 0
    while i < len(s):
        ch = s[i]
        i += 1
        num = ""
        while i < len(s) and s[i].isdigit():
            num += s[i]
            i += 1
        out += ch * (int(num) if num else 1)
    return out


REF_NS = {"compress": compress, "decompress": decompress}


def cases():
    rng = random.Random(4501)
    words = ["aabcccccaaa", "", "a", "abc", "aaaaaaaaaaaa", "zzzzzzzzzzzzzzzzzzzzzzzzz", "aAaA", "  !!  ",
             "abbbbbbbbbbbbbbbc", "xyz" * 3]
    for _ in range(15):
        words.append("".join(rng.choice("ab xY!") * rng.choice([1, 1, 2, 3, 11]) for _ in range(rng.randint(0, 8))))
    c = []
    for w in words:
        c.append({"call": "compress", "args": [w]})
        c.append({"call": "decompress", "args": [compress(w)]})
    c += [{"call": "decompress", "args": ["a12"]}, {"call": "decompress", "args": ["abc"]},
          {"call": "decompress", "args": ["x100"]}, {"call": "decompress", "args": [""]}]
    return c


def grade(path):
    return grade_function(path, NAMES, None, cases(), forbidden=FORBIDDEN, ref_ns=REF_NS)

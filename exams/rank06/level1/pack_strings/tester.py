import random

from engine.pygrader import grade_function

NAMES = ['pack', 'unpack']
FORBIDDEN = ['json', 'pickle', 'eval']

def pack(strs):
    return "".join(f"{len(s)}:{s}" for s in strs)


def unpack(s):
    out, i = [], 0
    while i < len(s):
        j = s.index(":", i)
        n = int(s[i:j])
        out.append(s[j + 1:j + 1 + n])
        i = j + 1 + n
    return out


REF_NS = {"pack": pack, "unpack": unpack}


def cases():
    lists = [["hello", "world"], [], [""], ["42", "exam#net", "level:6"], ["", ""], ["", "a", ""],
             ["3:abc", "#", "##", "::"], ["line\nbreak", "tab\there"], ["12", "", "1:2:3"], ["   "], ["\\", "'", '"']]
    rng = random.Random(4602)
    for _ in range(20):
        lists.append(["".join(rng.choice("ab1:#, \n9") for _ in range(rng.randint(0, 8)))
                      for _ in range(rng.randint(0, 6))])
    return [{"pipe": ["pack", "unpack"], "args": [l]} for l in lists]


def grade(path):
    return grade_function(path, NAMES, None, cases(), forbidden=FORBIDDEN, ref_ns=REF_NS)

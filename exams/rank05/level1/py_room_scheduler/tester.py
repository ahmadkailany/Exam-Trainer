import random

from engine.pygrader import grade_function

NAMES = ['py_room_scheduler']
FORBIDDEN = []

def _schedule(meetings, heap_choice, touching_ok):
    rooms = []
    for m in sorted(meetings, key=lambda m: m[0]):
        free = (lambda r: r[-1][1] <= m[0]) if touching_ok else (lambda r: r[-1][1] < m[0])
        target = None
        if heap_choice:
            if rooms:
                best = min(rooms, key=lambda r: r[-1][1])
                target = best if free(best) else None
        else:
            target = next((r for r in rooms if free(r)), None)
        if target is None:
            rooms.append([list(m)])
        else:
            target.append(list(m))
    return {"total_rooms": len(rooms), "schedule": rooms}


def reference(meetings):
    return _schedule(meetings, heap_choice=False, touching_ok=True)


def ref_first_fit_strict(meetings):
    return _schedule(meetings, False, False)


def ref_earliest_end(meetings):
    return _schedule(meetings, True, True)


def ref_earliest_end_strict(meetings):
    return _schedule(meetings, True, False)


def cases():
    c = [([[0, 30], [5, 10], [15, 20]],), ([],), ([[1, 2]],), ([[7, 10], [2, 4]],), ([[1, 5], [2, 6], [3, 7]],),
         ([[0, 10], [10, 20], [20, 30]],), ([[5, 8], [1, 3], [2, 9], [4, 6]],)]
    rng = random.Random(4503)
    for _ in range(25):
        starts = rng.sample(range(0, 60), rng.randint(1, 8))
        c.append(([[s, s + rng.randint(1, 20)] for s in starts],))
    return c


def grade(path):
    return grade_function(path, NAMES, reference, cases(), forbidden=FORBIDDEN, compare="value", alt_references=[ref_first_fit_strict, ref_earliest_end, ref_earliest_end_strict])

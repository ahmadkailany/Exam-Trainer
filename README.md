# Exam Trainer v1.0.0

*made by Ahmad Kailany for 42 Students*

A practice **examshell** for 42 exams. Questions are picked at random per level;
you write the solution, type `grademe`, and it is tested against many hidden cases
(subject examples + edge cases + random cases).

## Quick start

Only **Python 3** is needed. Everything else installs itself into a local `.venv`
the first time you run it (takes ~15 seconds, once).

| | Command |
|---|---|
| With make (Linux / macOS / Windows) | `make` |
| Without make | `python examshell.py` (`python3` on Linux / macOS) |
| Windows shortcut | `.\examshell` |

Only want to install? `make install`, `.\install.cmd` (Windows) or `./install.sh` (Linux / macOS).

### Make commands

| Command | What it does |
|---|---|
| `make` | install if needed, then start the examshell |
| `make install` | create `.venv` and install the requirements |
| `make grademe` | grade your current exercise (from a second terminal) |
| `make status` | level, score, timer, history |
| `make subject` | print the current subject |
| `make clean` | remove traces, subject copy, caches |
| `make fclean` | clean + remove `.venv` and saved progress (your `grademe/` files are kept) |
| `make re` | fclean + install |
| `make version` | print the version |

The interface uses [rich](https://github.com/Textualize/rich) for the boxes and colours.
Best viewed in **Windows Terminal** (or any modern terminal) with a window at least 100 columns wide.
Set `EXAM_TRAINER_NO_VENV=1` to skip the venv and use your current Python.

**Icons:** Linux / macOS get colour emoji. Windows gets symbols its console fonts can draw
(√ × ► ≡ ←). Force one or the other with `EXAM_TRAINER_ICONS=emoji` or `EXAM_TRAINER_ICONS=safe`.

**Navigation:** every menu has **`b`** to go back one step
(exercise → level → mode → main menu). In the examshell, `b` / `exit` returns to the main menu.

## How an exam works

1. **Main menu**: pick the rank, then the mode:
   - **Exam mode** - 3 hour timer. When time runs out the exam ends with the points you have.
   - **Practice exam** - no timer (time used is still shown).
   - **Train one exercise** - choose a level, then the exercise (or `r` for a random one).
     Pass it → congrats → Enter → back to the main menu.
2. The screen clears and a random question for **level 1** is shown
   (a copy is also put in `subject/<name>/subject.txt`).
3. Write your solution in **`grademe/<name>.py`** (the exact filename is printed).
4. Type `grademe` at the `examshell>` prompt.
   - **FAILURE** → you see the failing input, expected and actual output, and the timer. Fix and retry.
   - **SUCCESS** → congrats + timer, press Enter → screen clears and the next level starts.
5. Pass all levels → **EXAM PASSED 100/100**, press Enter → back to the main menu.

You can also grade from another terminal: `python examshell.py grademe` (or `.\grademe`).

Other commands at the prompt: `subject`, `status` (level, points, timer, history), `clear`,
`help`, `exit` or `b` (back to the menu - progress is saved, choose `r` to resume), `giveup`.

## What the grader checks

- File exists with the exact name, and defines the function.
- **Forbidden functions** from the subject (e.g. `sorted()` / `.sort()` in merge_sorted_lists).
  Subjects marked "Allowed functions: None" must not use any `import`.
- Output must match exactly, **including type** (`True` ≠ `1`, list ≠ tuple).
- Crashes, infinite loops (10s timeout) and slow algorithms on big inputs (6s) fail.
- Your `print`s are ignored, and `if __name__ == "__main__":` test code is fine.

Traces of each attempt are saved in `traces/`.

## Current content

| Rank   | Level | Questions |
|--------|-------|-----------|
| rank04 (Python) | 1 | py_array_rotation_detector, py_constellation_mapper |
|        | 2 | py_list_intersection_finder, py_merge_sorted_lists |
|        | 3 | py_palindrome_partitioner, py_package_dependency_resolver |
|        | 4 | py_sliding_window_maximum |

## Adding ranks / questions

```
exams/<rankXX>/level<N>/<question_name>/
    subject.txt   what the student sees
    meta.json     {"name": ..., "file": "<expected file>", "function": ...}
    tester.py     must define grade(student_file_path) -> Result
```

Ranks and levels are discovered automatically. For Python function subjects,
`tester.py` defines a `reference` solution and test `cases()` and calls
`engine.pygrader.grade_function(...)` (see any rank04 tester). For C ranks later,
a tester only needs to provide its own `grade()` (compile with gcc, compare output).

> The `tester.py` files contain reference solutions - don't peek if you want a real exam feeling!

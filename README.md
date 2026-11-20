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

## Current content

| Rank | Language | Levels | Exercises |
|---|---|---|---|
| Rank 02 | C | 4 | 57 (12 / 20 / 15 / 10 per level) |
| Rank 03 | Python | 6 | 14 |
| Rank 04 | Python | 4 | 7 |
| Rank 05 | Python | 3 | 7 |
| Rank 06 | Python | 2 | 9 (classes: Trie, Union-Find, LRU cache, Min-heap...) |


## What the grader checks

**Python exercises** (`grademe/<name>.py`)
- The file exists with the exact name and defines every function / class the subject asks for.
- **Forbidden functions** from the subject (e.g. `sorted()`, `json`, `heapq`, `collections.OrderedDict`).
  Subjects marked "Allowed functions: None" must not use any `import` (`typing` is always fine).
- Classes (rank 06) are tested with sequences of method calls; every return value must match.
- Output must match exactly, **including type** (`True` ≠ `1`, list ≠ tuple).
- Crashes and infinite loops (10s timeout) fail. Some rank 04 subjects also test big inputs for speed.
- Your `print`s are ignored, and `if __name__ == "__main__":` test code is fine.

**C exercises** (`grademe/<name>.c`, plus your `.h` if the subject asks for one) - needs a C compiler
(`cc`/`gcc`; Ubuntu: `sudo apt install build-essential`, Windows: [w64devkit](https://github.com/skeeto/w64devkit) or MSYS2).
- Compiled with **`-Wall -Wextra -Werror`** - any warning is a failure, just like the exam.
- **Allowed functions** are checked on the compiled object (`nm`): calling anything not listed fails.
- **Programs** are run with many argument lists; **functions** are linked with a hidden test `main()`
  (so your file must *not* contain a `main`).
- Output is compared byte for byte with a reference solution and shown `| cat -e` style.
- Segfaults, crashes and infinite loops (5s timeout) fail.

Traces of each attempt are saved in `traces/`.

## Adding ranks / questions

```
exams/<rankXX>/rank.json                 {"title", "language", "description", "final": true for the last rank}
exams/<rankXX>/level<N>/<question_name>/
    subject.txt   what the student sees
    meta.json     {"name", "file": "<expected file>", ...}
    tester.py     must define grade(student_file_path) -> Result
```

Ranks and levels are discovered automatically.
- **Python** subjects: `tester.py` defines a `reference` solution and test `cases()` and calls
  `engine.pygrader.grade_function(...)`.
- **C** subjects: `tester.py` calls `engine.cgrader.grade_dir(...)`, which uses `ref.c`
  (reference solution), `tests.json` (argv lists), `driver.c` (test `main` for function exercises)
  and `include/` (headers the subject provides). `meta.json` adds `kind` and `allowed`.

> The exam folders contain the reference solutions - don't peek if you want a real exam feeling!

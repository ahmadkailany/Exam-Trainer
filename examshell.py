#!/usr/bin/env python3
"""42-style practice examshell.

    python examshell.py            main menu: exam (3h), practice exam (no timer), train one exercise
    python examshell.py grademe    grade your current question from any terminal
    python examshell.py status     show the current exam state

Layout:
    exams/<rank>/rank.json                        - optional {title, language, description}
    exams/<rank>/level<N>/<question>/subject.txt  - the subject
    exams/<rank>/level<N>/<question>/tester.py    - grade(student_file) -> Result
    subject/<question>/subject.txt                - copy of your current subject
    grademe/<question>.py                         - put your solution here
    traces/                                       - details of every grading
"""
import importlib.util
import json
import os
import random
import re
import shutil
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from engine import APP_NAME, CREDIT, VERSION, bootstrap  # noqa: E402

if "--version" in sys.argv or "-v" in sys.argv:
    print(f"{APP_NAME} v{VERSION} - {CREDIT}")
    sys.exit(0)

bootstrap.ensure(ROOT)  # creates .venv + installs rich on first run, then restarts inside it

from engine import ui  # noqa: E402

EXAMS_DIR = os.path.join(ROOT, "exams")
GRADEME_DIR = os.path.join(ROOT, "grademe")
SUBJECT_DIR = os.path.join(ROOT, "subject")
TRACES_DIR = os.path.join(ROOT, "traces")
STATE_FILE = os.path.join(ROOT, ".exam_state.json")
EXAM_DURATION = 3 * 60 * 60  # 3 hours, like the real exam

COMMANDS = [
    ("grademe", "grade the file in grademe/ for the current subject"),
    ("subject", "clear the screen and show the subject again"),
    ("status", "level, score, timer, history"),
    ("clear", "clear the screen"),
    ("help", "this help"),
    ("exit / b", "back to the main menu (progress saved - resume with r)"),
    ("giveup", "abandon this exam / training"),
]


# --------------------------------------------------------------------------- #
# Exam content discovery                                                       #
# --------------------------------------------------------------------------- #
def _num(name):
    m = re.search(r"\d+", name)
    return int(m.group()) if m else 0


def list_ranks():
    if not os.path.isdir(EXAMS_DIR):
        return []
    return sorted((d for d in os.listdir(EXAMS_DIR) if os.path.isdir(os.path.join(EXAMS_DIR, d))), key=_num)


def list_levels(rank):
    path = os.path.join(EXAMS_DIR, rank)
    return sorted((d for d in os.listdir(path)
                   if d.startswith("level") and os.path.isdir(os.path.join(path, d))), key=_num)


def list_questions(rank, level):
    path = os.path.join(EXAMS_DIR, rank, level)
    return sorted(d for d in os.listdir(path) if os.path.isfile(os.path.join(path, d, "subject.txt")))


def rank_info(rank):
    info = {"name": rank, "title": rank, "language": "?", "description": ""}
    path = os.path.join(EXAMS_DIR, rank, "rank.json")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            info.update(json.load(f))
    levels = list_levels(rank)
    info["levels"] = len(levels)
    info["exercises"] = sum(len(list_questions(rank, lv)) for lv in levels)
    return info


def question_dir(state):
    return os.path.join(EXAMS_DIR, state["rank"], state["level"], state["question"])


def read_meta(state):
    with open(os.path.join(question_dir(state), "meta.json"), encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------- #
# State                                                                        #
# --------------------------------------------------------------------------- #
def load_state():
    if os.path.isfile(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return None


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def clear_state():
    if os.path.isfile(STATE_FILE):
        os.remove(STATE_FILE)


def mode_of(state):
    if state.get("mode") == "train":
        return "train"
    return "exam" if state.get("timed", True) else "practice"


def is_training(state):
    return mode_of(state) == "train"


def rank_title(state):
    return rank_info(state["rank"])["title"]


# --------------------------------------------------------------------------- #
# Timer                                                                        #
# --------------------------------------------------------------------------- #
def elapsed(state):
    return time.time() - state["started"]


def remaining(state):
    return EXAM_DURATION - elapsed(state)


def time_is_up(state):
    return mode_of(state) == "exam" and remaining(state) <= 0


def timer_text(state):
    return ui.timer(mode_of(state) == "exam", remaining(state), elapsed(state))


def points(state):
    return round(100 * state["level_index"] / len(state["levels"]))


# --------------------------------------------------------------------------- #
# Exam flow                                                                    #
# --------------------------------------------------------------------------- #
def pick_question(state, question=None):
    level = state["levels"][state["level_index"]]
    question = question or random.choice(list_questions(state["rank"], level))
    state["level"] = level
    state["question"] = question
    state["attempts"] = 0

    # Copy the subject into ./subject/<question>/ like the real exam does.
    if os.path.isdir(SUBJECT_DIR):
        shutil.rmtree(SUBJECT_DIR)
    os.makedirs(os.path.join(SUBJECT_DIR, question))
    shutil.copy(os.path.join(question_dir(state), "subject.txt"),
                os.path.join(SUBJECT_DIR, question, "subject.txt"))
    os.makedirs(GRADEME_DIR, exist_ok=True)
    save_state(state)


def show_header(state):
    ui.header(rank_title(state), mode_of(state), len(state["levels"]), state["level_index"],
              points(state), timer_text(state),
              training_level=f"{state['level']} · {state['question']}" if is_training(state) else None)


def show_subject(state):
    with open(os.path.join(question_dir(state), "subject.txt"), encoding="utf-8") as f:
        text = f.read()
    show_header(state)
    ui.subject(text, "grademe/" + read_meta(state)["file"])


def show_status(state):
    rows = [("Exam", rank_title(state)),
            ("Mode", {"exam": "Exam (3h timer)", "practice": "Practice exam (no timer)",
                      "train": "Training one exercise"}[mode_of(state)]),
            ("Level", state["level"] if is_training(state)
             else f"{state['level_index'] + 1}/{len(state['levels'])}  ({state['level']})"),
            ("Subject", state["question"]),
            ("Attempts", str(state["attempts"]))]
    if not is_training(state):
        rows.append(("Score", f"{points(state)}/100"))
    ui.status(rows, state["history"], timer_text(state))


def load_tester(state):
    spec = importlib.util.spec_from_file_location("tester", os.path.join(question_dir(state), "tester.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def times_up(state, interactive):
    if interactive:
        ui.clear()
    ui.time_up(rank_title(state), points(state), state["history"])
    clear_state()
    if interactive:
        ui.pause("Press Enter to go back to the main menu")


def grademe(state, interactive=True):
    """Grades the current question. Returns True if the exam continues."""
    if time_is_up(state):
        times_up(state, interactive)
        return False

    meta = read_meta(state)
    student_file = os.path.join(GRADEME_DIR, meta["file"])
    if not os.path.isfile(student_file):
        others = [f for f in os.listdir(GRADEME_DIR) if f != "__pycache__"] if os.path.isdir(GRADEME_DIR) else []
        ui.file_missing("grademe/" + meta["file"], others)
        return True

    state["attempts"] += 1
    with ui.grading_spinner("grademe/" + meta["file"]):
        result = load_tester(state).grade(student_file)

    os.makedirs(TRACES_DIR, exist_ok=True)
    trace_name = f"{state['question']}_attempt{state['attempts']}.txt"
    with open(os.path.join(TRACES_DIR, trace_name), "w", encoding="utf-8") as f:
        f.write(f"{state['question']} - attempt {state['attempts']} - "
                f"{'SUCCESS' if result.ok else 'FAILURE'}\n\n{result.trace}\n")
    state["history"].append({"level": state["level"], "question": state["question"], "ok": result.ok})

    # ---------------- failure ----------------
    if not result.ok:
        save_state(state)
        ui.failure(result, state["attempts"], timer_text(state), trace_name)
        if time_is_up(state):
            if interactive:
                ui.pause()
            times_up(state, interactive)
            return False
        return True

    question, attempts = state["question"], state["attempts"]

    # ---------------- success: training ----------------
    if is_training(state):
        clear_state()
        ui.success(result, question, attempts, None, timer_text(state),
                   "Press Enter to go back to the main menu" if interactive else None)
        return False

    # ---------------- success: exam ----------------
    state["level_index"] += 1
    last = state["level_index"] >= len(state["levels"])
    next_msg = "Press Enter to finish the exam" if last else f"Press Enter to go to level {state['level_index'] + 1}"
    if not interactive:
        next_msg = None

    if last:
        save_state(state)
        ui.success(result, question, attempts, points(state), timer_text(state), next_msg)
        if interactive:
            ui.clear()
        total = ui.fmt_time(elapsed(state)) + (f" of {ui.fmt_time(EXAM_DURATION)}" if mode_of(state) == "exam" else "")
        ui.exam_passed(rank_title(state), total, state["history"])
        clear_state()
        if interactive:
            ui.pause("Press Enter to go back to the main menu")
        return False

    pick_question(state)
    ui.success(result, question, attempts, points(state), timer_text(state), next_msg)
    if interactive:
        ui.clear()
        show_subject(state)
    else:
        ui.info(f"Next: level {state['level_index'] + 1} - [bold]{state['question']}[/] "
                "(type [bold]subject[/] in the examshell to see it)")
    return True


def new_exam(rank, timed):
    state = {"rank": rank, "levels": list_levels(rank), "level_index": 0,
             "started": time.time(), "timed": timed, "mode": "exam", "history": []}
    # Empty the grademe folder so old solutions don't hang around.
    if os.path.isdir(GRADEME_DIR):
        for name in os.listdir(GRADEME_DIR):
            p = os.path.join(GRADEME_DIR, name)
            if os.path.isfile(p):
                os.remove(p)
    if os.path.isdir(TRACES_DIR):
        shutil.rmtree(TRACES_DIR)
    pick_question(state)
    return state


def new_training(rank, level, question):
    state = {"rank": rank, "levels": [level], "level_index": 0,
             "started": time.time(), "timed": False, "mode": "train", "history": []}
    pick_question(state, question)
    return state


# --------------------------------------------------------------------------- #
# Menus                                                                        #
# --------------------------------------------------------------------------- #
BACK = ("b", "back")


def choose_training(rank):
    """Level menu -> exercise menu. Returns (level, question), or None for back."""
    levels = list_levels(rank)
    while True:
        ui.clear()
        ui.level_menu([(lv, list_questions(rank, lv)) for lv in levels])
        c = ui.ask()
        if c in BACK:
            return None
        if not (c.isdigit() and 1 <= int(c) <= len(levels)):
            continue  # invalid -> show the level menu again
        level = levels[int(c) - 1]

        questions = list_questions(rank, level)
        while True:
            ui.clear()
            ui.exercise_menu(level, questions)
            c = ui.ask()
            if c in BACK:
                break  # back to the level menu
            if c == "r":
                return level, random.choice(questions)
            if c.isdigit() and 1 <= int(c) <= len(questions):
                return level, questions[int(c) - 1]


def choose_mode(rank):
    """Mode menu (and training menus). Returns a new state, or None for back."""
    while True:
        ui.clear()
        ui.mode_menu(rank_info(rank)["title"])
        mode = ui.ask()
        if mode in BACK:
            return None
        if mode in ("1", "2"):
            return new_exam(rank, timed=(mode == "1"))
        if mode == "3":
            pick = choose_training(rank)
            if pick:
                return new_training(rank, *pick)
            # back from the level menu -> show the mode menu again


def run_exam(state):
    """The examshell prompt. Returns when the exam ends or the user exits."""
    ui.clear()
    show_subject(state)
    while True:
        cmd = ui.exam_prompt()
        # Reload: the user may have graded from another terminal in the meantime.
        fresh = load_state()
        if fresh is None and cmd:
            ui.warn("This exam was finished or abandoned from another terminal.")
            ui.pause("Press Enter to go back to the main menu")
            return
        state = fresh or state

        if cmd == "grademe":
            if not grademe(state):
                return
        elif cmd == "subject":
            ui.clear()
            show_subject(state)
        elif cmd == "status":
            show_status(state)
        elif cmd == "clear":
            ui.clear()
        elif cmd in ("help", "?"):
            ui.help_panel(COMMANDS)
        elif cmd in ("exit", "quit", "b", "back"):
            return
        elif cmd == "giveup":
            if ui.ask(f"Really abandon? [y/N] {ui.I['prompt']}", kind="confirm") in ("y", "yes"):
                clear_state()
                return
        elif cmd:
            ui.error(f"Unknown command: [bold]{cmd}[/]  (type [bold]help[/])")


def main_menu():
    while True:
        ui.clear()
        state = load_state()
        ranks = list_ranks()
        if not ranks:
            ui.error("No exams found in ./exams")
            return

        progress = None
        if state:
            if is_training(state):
                progress = f"Training  {rank_title(state)} · {state['level']} · {state['question']}"
            else:
                progress = (f"{'Exam' if mode_of(state) == 'exam' else 'Practice exam'}  {rank_title(state)} · "
                            f"level {state['level_index'] + 1}/{len(state['levels'])} · {state['question']}")
        ui.main_menu([rank_info(r) for r in ranks], progress)
        choice = ui.ask()

        if choice in ("q", "quit", "exit"):
            ui.clear()
            return
        if choice == "r" and state:
            if time_is_up(state):
                times_up(state, True)
            else:
                run_exam(state)
            continue
        if not (choice.isdigit() and 1 <= int(choice) <= len(ranks)):
            continue
        rank = ranks[int(choice) - 1]

        if state and ui.ask("[yellow]Starting something new abandons the one in progress. Continue? [y/N][/] " + ui.I["prompt"],
                            kind="confirm") not in ("y", "yes"):
            continue

        state = choose_mode(rank)
        if state:          # None = user went back to the main menu
            run_exam(state)


def main():
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    state = load_state() if cmd else None
    if cmd in ("grademe", "status", "subject") and not state:
        ui.warn("No exam in progress. Start one with [bold]make[/] (or [bold]examshell[/]).")
        return
    if cmd == "grademe":
        grademe(state, interactive=False)
    elif cmd == "status":
        show_status(state)
    elif cmd == "subject":
        show_subject(state)
    else:
        ui.console.set_window_title(f"{APP_NAME} v{VERSION}")
        main_menu()


if __name__ == "__main__":
    main()

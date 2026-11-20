"""All the screen drawing for the examshell, built on `rich`."""
import os
import re
import sys
import textwrap

try:
    from rich import box
    from rich.align import Align
    from rich.columns import Columns
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.rule import Rule
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("This trainer needs the 'rich' package. Install it with:\n\n    python -m pip install rich\n")
    sys.exit(1)

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from engine import APP_NAME, AUTHOR, VERSION  # noqa: E402

console = Console(highlight=False)

ACCENT = "#00babc"      # 42 teal
ACCENT2 = "#a259ff"
OK = "bold green"
KO = "bold red"
WARN = "bold yellow"
MAX_WIDTH = 100

# Key / badge styles: explicit hex colours on both sides (never the theme's "black",
# which many terminal themes draw as grey) - every pair is >= 6:1 contrast.
KEY_TEAL = "bold #ffffff on #006a6c"
KEY_PURPLE = "bold #ffffff on #5b21b6"
KEY_RED = "bold #ffffff on #a3132a"
KEY_YELLOW = "bold #111111 on #ffd60a"
KEY_GREEN = "bold #0b2e13 on #5ee07a"
TRACK_TODO = "#c8c8c8 on #333333"

# Icons: colour emoji where the terminal can draw them (Linux / macOS), and symbols that
# exist in the default Windows console fonts (Consolas, Lucida Console, Cascadia) on Windows.
# Override with EXAM_TRAINER_ICONS=emoji or EXAM_TRAINER_ICONS=safe.
_ICON_SETS = {          # name: (emoji, windows-safe)
    "prompt": ("❯", ">"),
    "enter": ("⏎", "→"),
    "info": ("›", "»"),
    "ok": ("✔", "√"),
    "ko": ("✘", "×"),
    "current": ("●", "●"),
    "todo": ("○", "○"),
    "link": ("━━", "──"),
    "play": ("▶", "►"),
    "back": ("↩", "←"),
    "exams": ("📚", "≡"),
    "exam": ("⌛", "♦"),
    "practice": ("📝", "■"),
    "train": ("🎯", "►"),
    "timer": ("⌛", "»"),
    "file": ("📄", "≡"),
    "folder": ("📂", "→"),
    "status": ("📊", "≡"),
    "commands": ("💻", "≡"),
    "dice": ("🎲", "?"),
    "party": ("🎉", "*"),
    "hint": ("💡", "!"),
    "alarm": ("⏰", "!"),
}
_icon_mode = os.environ.get("EXAM_TRAINER_ICONS", "").lower()
USE_EMOJI = _icon_mode == "emoji" or (_icon_mode != "safe" and os.name != "nt")
I = {name: pair[0 if USE_EMOJI else 1] for name, pair in _ICON_SETS.items()}

LOGO = [
    "███████╗██╗  ██╗ █████╗ ███╗   ███╗",
    "██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║",
    "█████╗   ╚███╔╝ ███████║██╔████╔██║",
    "██╔══╝   ██╔██╗ ██╔══██║██║╚██╔╝██║",
    "███████╗██╔╝ ██╗██║  ██║██║ ╚═╝ ██║",
    "╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝",
]
GRADIENT = ["#00e5e8", "#00c8d0", "#2aa8e0", "#5a8af0", "#7f6cf8", "#a259ff"]


def width():
    return min(console.width, MAX_WIDTH)


def clear():
    console.clear()


def show(*renderables):
    for r in renderables:
        console.print(r, width=width())


# --------------------------------------------------------------------------- #
# Input                                                                        #
# --------------------------------------------------------------------------- #
def ask(prompt=None, kind="menu"):
    """Every user input goes through here (`kind` lets tests script answers)."""
    try:
        prompt = I["prompt"] if prompt is None else prompt
        return console.input(f"[bold {ACCENT}]{prompt}[/] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        console.print()
        raise SystemExit(0)


def pause(message="Press Enter to continue"):
    try:
        console.input(f"\n[dim]  {I['enter']}  {message}...[/] ")
    except (EOFError, KeyboardInterrupt):
        console.print()


def exam_prompt():
    return ask(f"examshell {I['prompt']}", kind="exam")


def info(msg):
    console.print(f"[{ACCENT}]{I['info']}[/]  {msg}")


def warn(msg):
    console.print(f"[{WARN}]![/]  {msg}")


def error(msg):
    console.print(f"[{KO}]{I['ko']}[/]  {msg}")


# --------------------------------------------------------------------------- #
# Small pieces                                                                 #
# --------------------------------------------------------------------------- #
def fmt_time(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 3600}h{(seconds % 3600) // 60:02d}m{seconds % 60:02d}s"


def timer(timed, left, used):
    t = Text()
    if timed:
        style = "bold green" if left > 30 * 60 else "bold yellow" if left > 5 * 60 else "bold red blink"
        t.append(f"{I['timer']}  ", style=style)
        t.append(f"{fmt_time(left)} left", style=style)
        t.append(f"   used {fmt_time(used)}", style="dim")
    else:
        t.append(f"{I['timer']}  ", style=ACCENT)
        t.append(f"{fmt_time(used)}", style=f"bold {ACCENT}")
        t.append("  no timer", style="dim")
    return t


def bar(done, total, size=30, colour="green"):
    total = max(total, 1)
    filled = round(size * done / total)
    t = Text()
    t.append("█" * filled, style=colour)
    t.append("░" * (size - filled), style="grey35")
    t.append(f"  {done}/{total}", style="bold")
    return t


def level_track(n_levels, current, finished=False):
    t = Text()
    for i in range(n_levels):
        if i < current or finished:
            t.append(f" {I['ok']} L{i + 1} ", style=KEY_GREEN)
        elif i == current:
            t.append(f" {I['current']} L{i + 1} ", style=KEY_YELLOW)
        else:
            t.append(f" {I['todo']} L{i + 1} ", style=TRACK_TODO)
        if i < n_levels - 1:
            t.append(I["link"], style="green" if i < current else "grey35")
    return t


def badge(text, style):
    return Text(f" {text} ", style=style)


# --------------------------------------------------------------------------- #
# Screens                                                                      #
# --------------------------------------------------------------------------- #
def logo():
    art = Text()
    for line, colour in zip(LOGO, GRADIENT):
        art.append(line + "\n", style=f"bold {colour}")
    sub = Text.assemble((" ".join(APP_NAME.upper()), f"bold {ACCENT}"), "   ",
                        (f" v{VERSION} ", KEY_TEAL))
    credit = Text.assemble(("made by ", "dim"), (AUTHOR, f"bold {ACCENT2}"), (" for ", "dim"),
                           ("42 Students", "bold white"))
    tag = Text("practice examshell  ·  grademe  ·  moulinette-style tests", style="dim italic")
    show(Panel(Align.center(Group(Align.center(art), Align.center(sub), Align.center(credit),
                                  Text(), Align.center(tag))),
               box=box.DOUBLE, border_style=ACCENT, padding=(1, 2),
               subtitle=f"[dim]{APP_NAME} v{VERSION}[/]", subtitle_align="right"))


def main_menu(ranks, in_progress=None):
    """ranks: list of dicts {name, title, language, levels, exercises, description}."""
    logo()
    if in_progress:
        show(Panel(Text.assemble(("  r  ", KEY_YELLOW), "  ", in_progress),
                   title=f"[bold yellow]{I['play']} In progress[/]", title_align="left",
                   border_style="yellow", box=box.ROUNDED))

    table = Table(box=box.SIMPLE_HEAVY, expand=True, header_style=f"bold {ACCENT}", show_edge=False)
    table.add_column("", justify="center", width=5)
    table.add_column("Exam", style="bold")
    table.add_column("Language")
    table.add_column("Levels", justify="center")
    table.add_column("Exercises", justify="center")
    table.add_column("About", style="dim", ratio=2)
    for i, r in enumerate(ranks, 1):
        table.add_row(Text(f" {i} ", style=KEY_TEAL), r["title"],
                      r["language"], str(r["levels"]), str(r["exercises"]), r["description"])
    show(Panel(table, title=f"[bold]{I['exams']} Choose an exam[/]", title_align="left",
               border_style=ACCENT, box=box.ROUNDED, padding=(0, 1)))
    show(Align.center(Text.assemble(("number", f"bold {ACCENT}"), " select   ",
                                    *((("r", "bold yellow"), " resume   ") if in_progress else ()),
                                    ("q", "bold red"), " quit", style="dim")))


def mode_menu(rank_title):
    def card(key, icon, title, lines, colour, key_style):
        body = Text.assemble((f" {key} ", key_style), "\n\n",
                             (f"{icon}  {title}\n\n", f"bold {colour}"), (lines, "dim"))
        return Panel(Align.center(body), border_style=colour, box=box.ROUNDED, width=30, height=10)

    cards = [
        card("1", I["exam"], "Exam mode", "Real conditions.\n3 hour timer,\nrandom subject per level.", "red", KEY_RED),
        card("2", I["practice"], "Practice exam", "All levels, random\nsubjects, no timer.\nTake your time.", ACCENT, KEY_TEAL),
        card("3", I["train"], "Train one", "Pick a level and\nthe exercise you want\nto train on.", ACCENT2, KEY_PURPLE),
    ]
    show(Rule(f"[bold]{rank_title}[/]  ·  choose a mode", style=ACCENT))
    show(Align.center(Columns(cards, padding=(0, 1))))
    show(Align.center(Text.assemble(("1 / 2 / 3", f"bold {ACCENT}"), " select   ",
                                    ("b", "bold yellow"), f" {I['back']} back", style="dim")))


def level_menu(levels):
    """levels: list of (level_name, [questions])."""
    table = Table(box=box.ROUNDED, expand=True, border_style=ACCENT2, header_style=f"bold {ACCENT2}")
    table.add_column("", justify="center", width=5)
    table.add_column("Level", style="bold")
    table.add_column("Exercises")
    for i, (lv, qs) in enumerate(levels, 1):
        table.add_row(Text(f" {i} ", style=KEY_PURPLE), lv,
                      Text.assemble((f"{len(qs)} exercise{'s' if len(qs) != 1 else ''}: ", "bold"),
                                    (", ".join(qs), "dim")))
    table.add_row(Text(" b ", style=KEY_YELLOW), Text(f"{I['back']}  back", style="yellow"), "")
    show(Rule(f"[bold]{I['train']} Train one exercise[/]  ·  choose a level", style=ACCENT2), table)


def exercise_menu(level, questions):
    table = Table(box=box.ROUNDED, expand=True, border_style=ACCENT2, show_header=False)
    table.add_column("", justify="center", width=5)
    table.add_column("Exercise", style="bold")
    for i, q in enumerate(questions, 1):
        table.add_row(Text(f" {i} ", style=KEY_PURPLE), q)
    table.add_row(Text(" r ", style=KEY_YELLOW), Text(f"{I['dice']}  surprise me (random)", style="yellow"))
    table.add_row(Text(" b ", style=KEY_YELLOW), Text(f"{I['back']}  back to levels", style="yellow"))
    show(Rule(f"[bold]{I['train']} {level}[/]  ·  choose an exercise", style=ACCENT2), table)


def header(rank_title, mode, n_levels, level_index, pts, timer_text, training_level=None):
    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="right")
    mode_badge = {"exam": badge(f"{I['exam']} EXAM", KEY_RED),
                  "practice": badge(f"{I['practice']} PRACTICE", KEY_TEAL),
                  "train": badge(f"{I['train']} TRAINING", KEY_PURPLE)}[mode]
    left = Text.assemble((rank_title, "bold"), "  ", mode_badge)
    if training_level:
        right = Text(training_level, style=f"bold {ACCENT2}")
    else:
        right = Text.assemble(("score ", "dim"), (f"{pts}", "bold green" if pts else "bold"), ("/100", "dim"))
    grid.add_row(left, right)
    if training_level:
        grid.add_row(timer_text, Text(""))
    else:
        grid.add_row(level_track(n_levels, level_index), timer_text)
    show(Panel(grid, box=box.HEAVY, border_style=ACCENT, padding=(0, 1)))


def _parse_subject(text):
    head, _, rest = text.partition("-" * 80)
    desc, _, rest = rest.partition("Function signature:")
    sig, _, examples = rest.partition("Examples:")
    fields = []
    for line in head.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields.append((k.strip(), v.strip()))
    return fields, desc.strip("\n"), textwrap.dedent(sig).strip(), textwrap.dedent(examples).strip()


def subject(text, file_hint):
    fields, desc, sig, examples = _parse_subject(text)
    info_grid = Table.grid(padding=(0, 2))
    info_grid.add_column(style="dim", justify="right")
    info_grid.add_column()
    name = ""
    for k, v in fields:
        style = "bold " + ACCENT if k.startswith("Assignment") else \
            "bold red" if k.startswith("Forbidden") else "bold yellow" if k.startswith("Allowed") else "bold"
        info_grid.add_row(k, Text(v, style=style))
        if k.startswith("Assignment"):
            name = v

    body = Text()
    for line in desc.split("\n"):
        if line.lstrip().startswith("$>"):          # shell example (C subjects)
            body.append(line + "\n", style=f"bold {ACCENT}")
        elif re.match(r"\s*(int|void|char|size_t|unsigned|t_list|typedef)\b.*[;{]\s*$", line) and "(" in line:
            body.append(line + "\n", style="bold yellow")   # prototypes
        else:
            body.append(line + "\n")
    body.rstrip()
    parts = [info_grid, Rule(style="grey35"), body]
    if sig:
        parts += [Text(), Text("Function signature", style=f"bold {ACCENT}"),
                  Syntax(sig, "python", theme="monokai", background_color="default", word_wrap=True)]
    if examples:
        parts += [Text(), Text("Examples", style=f"bold {ACCENT}"),
                  Syntax(examples, "pycon", theme="monokai", background_color="default", word_wrap=True)]
    show(Panel(Group(*parts), title=f"[bold]{I['file']} {name}[/]", title_align="left",
               border_style="white", box=box.ROUNDED, padding=(1, 2)))
    show(Text.assemble((f"  {I['folder']} ", "dim"), (file_hint, f"bold {ACCENT}"),
                       ("   ·   ", "dim"), ("grademe", "bold green"), (" to grade", "dim"),
                       ("   ·   ", "dim"), ("help", "bold"), (" for commands", "dim")))
    console.print()


def grading_spinner(filename):
    return console.status(f"[bold {ACCENT}]Moulinette is grading [white]{filename}[/] ...", spinner="dots12")


def failure(result, attempt, timer_text, trace_name):
    parts = []
    if result.total:
        parts += [Text.assemble(("tests  ", "dim"), bar(result.passed, result.total, colour="red")), Text()]
    d = result.details
    if d:
        parts.append(Text(d["title"], style=KO))
        t = Table(box=box.SIMPLE, show_header=False, expand=True, padding=(0, 1))
        t.add_column(style="dim", width=10)
        t.add_column(overflow="fold")
        if "input" in d:
            t.add_row("Input", Text(d["input"], style="bold"))
        if "expected" in d:
            t.add_row("Expected", Text(d["expected"], style="green"))
        if "got" in d:
            t.add_row(d.get("got_label", "Got"), Text(d["got"], style="red"))
        if t.row_count:
            parts.append(t)
        if "hint" in d:
            parts.append(Text(f"{I['hint']} " + d["hint"], style="yellow"))
    else:
        parts.append(Text(result.trace, style="red"))
    parts += [Text(), Text.assemble(timer_text, ("    attempt ", "dim"), (f"#{attempt}", "bold"),
                                    ("    trace: ", "dim"), (f"traces/{trace_name}", "dim underline"))]
    show(Panel(Group(*parts), title=f"[bold red]{I['ko']}  FAILURE[/]", title_align="left",
               border_style="red", box=box.HEAVY, padding=(1, 2)))
    console.print("  [yellow]Fix your code and type[/] [bold green]grademe[/] [yellow]again.[/]\n")


def success(result, question, attempts, pts, timer_text, next_msg):
    body = Group(
        Align.center(Text(f"{I['ok']}  S U C C E S S  {I['ok']}", style="bold green")),
        Text(),
        Align.center(Text.assemble(("tests  ", "dim"), bar(result.total, result.total))),
        Text(),
        Align.center(Text.assemble(f"{I['party']} Congratulations! ", (question, "bold"),
                                   f" validated in {attempts} attempt{'s' if attempts != 1 else ''}.")),
        Align.center(Text.assemble(("score ", "dim"), (f"{pts}/100", "bold green")) if pts is not None else Text()),
        Align.center(timer_text),
    )
    show(Panel(body, border_style="green", box=box.HEAVY, padding=(1, 2)))
    if next_msg:
        pause(next_msg)


def history_table(history):
    t = Table(box=box.SIMPLE_HEAD, expand=True, header_style="bold")
    t.add_column("#", justify="right", style="dim", width=3)
    t.add_column("Level")
    t.add_column("Exercise")
    t.add_column("Result", justify="center")
    for i, h in enumerate(history, 1):
        t.add_row(str(i), h["level"], h["question"],
                  Text(f"{I['ok']} OK", style=OK) if h["ok"] else Text(f"{I['ko']} FAIL", style=KO))
    return t


def exam_passed(rank_title, total_time, history):
    trophy = Text("\n".join([
        "   ___________   ",
        "  '._==_==_=_.'  ",
        "  .-\\:      /-.  ",
        " | (|:.     |) | ",
        "  '-|:.     |-'  ",
        "    \\::.    /    ",
        "     '::. .'     ",
        "       ) (       ",
        "     _.' '._     ",
        "    '-------'    ",
    ]), style="bold yellow")
    body = Group(Align.center(trophy), Text(),
                 Align.center(Text("E X A M   P A S S E D", style="bold green")),
                 Align.center(Text.assemble((rank_title, "bold"), "   ·   ", ("100/100", "bold green"),
                                            "   ·   ", (total_time, f"bold {ACCENT}"))),
                 Text(), history_table(history))
    show(Panel(body, border_style="green", box=box.DOUBLE, padding=(1, 2)))


def time_up(rank_title, pts, history):
    body = Group(Align.center(Text(f"{I['alarm']}  T I M E ' S   U P", style="bold red")), Text(),
                 Align.center(Text.assemble((rank_title, "bold"), "   ·   final score ",
                                            (f"{pts}/100", "bold yellow"))),
                 Text(), history_table(history))
    show(Panel(body, border_style="red", box=box.DOUBLE, padding=(1, 2)))


def status(rows, history, timer_text):
    t = Table.grid(padding=(0, 2))
    t.add_column(style="dim", justify="right")
    t.add_column(style="bold")
    for k, v in rows:
        t.add_row(k, v)
    t.add_row("Timer", timer_text)
    parts = [t]
    if history:
        parts += [Text(), history_table(history)]
    show(Panel(Group(*parts), title=f"[bold]{I['status']} Status[/]", title_align="left",
               border_style=ACCENT, box=box.ROUNDED, padding=(1, 2)))


def help_panel(commands):
    t = Table(box=None, show_header=False, padding=(0, 2))
    t.add_column(style="bold green")
    t.add_column(style="dim")
    for c, d in commands:
        t.add_row(c, d)
    show(Panel(t, title=f"[bold]{I['commands']} Commands[/]", title_align="left", border_style=ACCENT, box=box.ROUNDED))


def file_missing(expected, others):
    body = [Text.assemble("File not found: ", (expected, "bold red"))]
    if others:
        body.append(Text("Files in grademe/: " + ", ".join(others), style="dim"))
    body.append(Text("The file must be named exactly as in the subject.", style="yellow"))
    show(Panel(Group(*body), title=f"[bold red]{I['ko']} No file[/]", title_align="left",
               border_style="red", box=box.ROUNDED))

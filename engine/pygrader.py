"""Generic grader for "write a Python function" exam subjects.

A question's tester.py calls grade_function(...) with:
  - the function name,
  - a hidden reference solution,
  - the list of test cases (each case = tuple of arguments),
  - forbidden functions / modules.

The student's output is compared with repr() equality, so types matter
(True is not 1, a tuple is not a list) - just like the moulinette.
"""
import ast
import copy
import json
import os
import subprocess
import sys
import tempfile

RUNNER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runner.py")
MAX_SHOWN = 400


class Result:
    """ok/trace/passed/total, plus `details` for pretty display:
    {"title": "Test 11/44 FAILED", "input": ..., "expected": ..., "got": ..., "hint": ...}
    (only the keys that apply are present; None when the failure is just a message)."""

    def __init__(self, ok, trace, passed=0, total=0, details=None):
        self.ok = ok
        self.trace = trace
        self.passed = passed
        self.total = total
        self.details = details


def _fail(title, passed, total, call=None, expected=None, got=None, got_label="Got", hint=None):
    details = {"title": title}
    lines = [title]
    if call is not None:
        details["input"] = call
        lines.append(f"  Input    : {call}")
    if expected is not None:
        details["expected"] = _short(expected)
        lines.append(f"  Expected : {_short(expected)}")
    if got is not None:
        details["got"] = _short(got)
        details["got_label"] = got_label
        lines.append(f"  {got_label:<9}: {_short(got)}")
    if hint:
        details["hint"] = hint
        lines.append(f"  {hint}")
    return Result(False, "\n".join(lines), passed, total, details)


def _short(text):
    text = str(text)
    return text if len(text) <= MAX_SHOWN else text[:MAX_SHOWN] + f"... ({len(text)} chars)"


def _call_str(func, args):
    return _short(f"{func}({', '.join(repr(a) for a in args)})")


# --------------------------------------------------------------------------- #
# Static checks                                                                #
# --------------------------------------------------------------------------- #
def _dotted(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return None


def check_source(path, func, forbidden=(), no_imports=False):
    """Returns an error string, or None if the file is acceptable.

    forbidden entries:
      "sorted"       -> the name sorted (builtin call / reference)
      ".sort"        -> any attribute named sort  (x.sort())
      "heapq.merge"  -> heapq.merge, or `from heapq import merge`
      "graphlib"     -> importing that module at all
    """
    try:
        with open(path, encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=os.path.basename(path))
    except SyntaxError as e:
        return f"Syntax error line {e.lineno}: {e.msg}"
    except UnicodeDecodeError:
        return "File is not valid UTF-8 text."

    if not any(isinstance(n, ast.FunctionDef) and n.name == func for n in tree.body):
        return f"No top-level function named '{func}' in your file."

    names, attrs, dotted, modules = set(), set(), set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            attrs.add(node.attr)
            d = _dotted(node)
            if d:
                dotted.add(d)
        elif isinstance(node, ast.Import):
            for a in node.names:
                modules.add(a.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            modules.add(mod)
            for a in node.names:
                dotted.add(f"{mod}.{a.name}")

    if no_imports and modules:
        return ("Imports are not allowed for this subject (Allowed functions: None).\n"
                f"Found import of: {', '.join(sorted(modules))}")

    for item in forbidden:
        hit = False
        if item.startswith("."):
            hit = item[1:] in attrs
        elif "." in item:
            hit = item in dotted or any(d.endswith("." + item) for d in dotted)
        else:
            hit = item in names or any(m == item or m.startswith(item + ".") for m in modules)
        if hit:
            return f"Forbidden function / module used: {item}"
    return None


# --------------------------------------------------------------------------- #
# Running                                                                      #
# --------------------------------------------------------------------------- #
def _run_student(path, func, cases, timeout):
    """Returns (data, error). data = runner output dict."""
    with tempfile.TemporaryDirectory() as tmp:
        cases_file = os.path.join(tmp, "cases.txt")
        out_file = os.path.join(tmp, "out.json")
        with open(cases_file, "w", encoding="utf-8") as f:
            f.write(repr(list(cases)))
        try:
            subprocess.run(
                [sys.executable, "-I", "-B", RUNNER, os.path.abspath(path), func, cases_file, out_file],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                timeout=timeout, cwd=tmp,
            )
        except subprocess.TimeoutExpired:
            return None, "TIMEOUT"
        if not os.path.exists(out_file):
            return None, "Your code crashed the interpreter (or called exit())."
        with open(out_file, encoding="utf-8") as f:
            return json.load(f), None


def grade_function(student_path, func, reference, cases, forbidden=(), no_imports=False,
                   alt_references=(), perf_cases=(), timeout=10, perf_timeout=6):
    if not os.path.isfile(student_path):
        return Result(False, f"File not found: {student_path}")

    err = check_source(student_path, func, forbidden, no_imports)
    if err:
        return Result(False, err)

    refs = [reference, *alt_references]

    def accepted(args):
        return {repr(r(*copy.deepcopy(args))) for r in refs}

    all_cases = list(cases)
    total = len(all_cases) + len(perf_cases)

    data, err = _run_student(student_path, func, all_cases, timeout)
    if err == "TIMEOUT":
        return _fail(f"TIMEOUT (> {timeout}s)", 0, total,
                     hint="Your function never finished on the normal tests - infinite loop?")
    if err:
        return Result(False, err, 0, total)
    if data["load_error"]:
        return Result(False, data["load_error"], 0, total)

    for i, (args, res) in enumerate(zip(all_cases, data["results"])):
        expected = repr(reference(*copy.deepcopy(args)))
        if "error" in res:
            return _fail(f"Test {i + 1}/{total} CRASHED", i, total, _call_str(func, args),
                         expected, res["error"], got_label="Error")
        if res["repr"] not in accepted(args):
            return _fail(f"Test {i + 1}/{total} FAILED", i, total, _call_str(func, args),
                         expected, res["repr"])

    passed = len(all_cases)
    for args in perf_cases:
        data, err = _run_student(student_path, func, [args], perf_timeout)
        if err == "TIMEOUT":
            return _fail(f"Test {passed + 1}/{total} TIMEOUT (> {perf_timeout}s) on a big input",
                         passed, total, _call_str(func, args),
                         hint="Your algorithm is too slow - think about complexity.")
        if err or data["load_error"]:
            return Result(False, err or data["load_error"], passed, total)
        res = data["results"][0]
        expected = repr(reference(*copy.deepcopy(args)))
        if "error" in res or res["repr"] not in accepted(args):
            return _fail(f"Test {passed + 1}/{total} FAILED on a big input", passed, total,
                         _call_str(func, args), expected, res.get("error") or res["repr"],
                         got_label="Error" if "error" in res else "Got")
        passed += 1

    return Result(True, f"All {total} tests passed.", total, total)

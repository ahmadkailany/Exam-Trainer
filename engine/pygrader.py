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

from engine.runner import execute

RUNNER =os.path.join(os.path.dirname(os.path.abspath(__file__)), "runner.py")
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

    required = [func] if isinstance(func, str) else list(func)
    defined = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    for name in required:
        if name not in defined:
            return f"No top-level function or class named '{name}' in your file."

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

    real_imports = {m for m in modules if m.split(".")[0] not in ("typing", "__future__")}  # type hints are fine
    if no_imports and real_imports:
        return ("Imports are not allowed for this subject (Allowed functions: None).\n"
                f"Found import of: {', '.join(sorted(real_imports))}")

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


def _case_str(func, case):
    """Human readable form of a test case."""
    if not isinstance(case, dict):
        return _call_str(func, case)
    if "call" in case:
        return _call_str(case["call"], case["args"])
    if "pipe" in case:
        f, g = case["pipe"]
        return _short(f"{g}({_call_str(f, case['args'])})   [+ type of {f}(...)]")
    if "cls" in case:
        parts = [f"x = {_call_str(case['cls'], case.get('init', []))}"]
        for name, args in case["ops"]:
            if name == "__same__":
                parts.append(f"x.find({args[0]}) == x.find({args[1]})")
            else:
                parts.append(_call_str("x." + name, args))
        return _short("; ".join(parts) + "   -> list of every return value")
    return _short(repr(case))


def grade_function(student_path, func, reference, cases, forbidden=(), no_imports=False,
                   alt_references=(), perf_cases=(), timeout=10, perf_timeout=6,
                   ref_ns=None, alt_ns=(), compare="repr", normalize=None):
    """func: the function name, or a list of required names (first = default function).
    reference: reference for the default function (plain argument-tuple cases).
    ref_ns: {name: reference} for dict cases ({"call"}, {"pipe"}, {"cls"} - see runner.py).
    compare: "repr" (exact, type-strict) or "value" (== after ast.literal_eval, e.g. dict order free).
    normalize: optional function applied to both sides before a "value" comparison."""
    if not os.path.isfile(student_path):
        return Result(False, f"File not found: {student_path}")

    names = [func] if isinstance(func, str) else list(func)
    default = names[0]
    err = check_source(student_path, names, forbidden, no_imports)
    if err:
        return Result(False, err)

    primary = dict(ref_ns or {})
    if reference is not None:
        primary[default] = reference
    namespaces = [primary] + [{**primary, default: r} for r in alt_references] + [{**primary, **ns} for ns in alt_ns]
    norm = normalize or (lambda v: v)

    def expected_repr(args):
        return repr(execute(primary, args, default))

    def matches(args, got_repr):
        if compare == "repr":
            return got_repr in {repr(execute(ns, args, default)) for ns in namespaces}
        try:
            got = ast.literal_eval(got_repr)
        except (ValueError, SyntaxError):
            return False
        for ns in namespaces:
            exp = execute(ns, args, default)
            try:
                if type(got) is type(exp) and norm(got) == norm(exp):
                    return True
            except TypeError:
                pass
        return False

    all_cases = list(cases)
    total = len(all_cases) + len(perf_cases)

    data, err = _run_student(student_path, default, all_cases, timeout)
    if err == "TIMEOUT":
        return _fail(f"TIMEOUT (> {timeout}s)", 0, total,
                     hint="Your function never finished on the normal tests - infinite loop?")
    if err:
        return Result(False, err, 0, total)
    if data["load_error"]:
        return Result(False, data["load_error"], 0, total)

    for i, (args, res) in enumerate(zip(all_cases, data["results"])):
        expected = expected_repr(args)
        if "error" in res:
            return _fail(f"Test {i + 1}/{total} CRASHED", i, total, _case_str(default, args),
                         expected, res["error"], got_label="Error")
        if not matches(args, res["repr"]):
            return _fail(f"Test {i + 1}/{total} FAILED", i, total, _case_str(default, args),
                         expected, res["repr"])

    passed = len(all_cases)
    for args in perf_cases:
        data, err = _run_student(student_path, default, [args], perf_timeout)
        if err == "TIMEOUT":
            return _fail(f"Test {passed + 1}/{total} TIMEOUT (> {perf_timeout}s) on a big input",
                         passed, total, _case_str(default, args),
                         hint="Your algorithm is too slow - think about complexity.")
        if err or data["load_error"]:
            return Result(False, err or data["load_error"], passed, total)
        res = data["results"][0]
        expected = expected_repr(args)
        if "error" in res or not matches(args, res["repr"]):
            return _fail(f"Test {passed + 1}/{total} FAILED on a big input", passed, total,
                         _case_str(default, args), expected, res.get("error") or res["repr"],
                         got_label="Error" if "error" in res else "Got")
        passed += 1

    return Result(True, f"All {total} tests passed.", total, total)

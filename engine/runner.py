"""Child process: imports the student's file and runs every test case.

Usage: python runner.py <student_file> <default_function> <cases_file> <out_file>

Runs in its own process so an infinite loop / crash / sys.exit in the student's
code can never take down the examshell. Anything the student prints is swallowed.

A case can be:
  (arg, arg, ...)                                   -> default_function(*args)
  {"call": "name", "args": [...]}                  -> name(*args)
  {"pipe": ["f", "g"], "args": [...]}              -> [type(f(*args)).__name__, g(f(*args))]
  {"cls": "Name", "init": [...], "ops": [[m, [args]], ...]}
                                                    -> [obj.m(*args) for each op]
     special op "__same__" [x, y]                   -> obj.find(x) == obj.find(y)
"""
import ast
import copy
import importlib.util
import io
import json
import sys
import traceback


def execute(ns, case, default):
    """Runs one case against a namespace (module or object with attributes). Shared with the grader."""
    get = (lambda n: ns[n]) if isinstance(ns, dict) else (lambda n: getattr(ns, n))
    if isinstance(case, dict):
        if "call" in case:
            return get(case["call"])(*copy.deepcopy(case["args"]))
        if "pipe" in case:
            f, g = (get(n) for n in case["pipe"])
            mid = f(*copy.deepcopy(case["args"]))
            return [type(mid).__name__, g(mid)]
        if "cls" in case:
            obj = get(case["cls"])(*copy.deepcopy(case.get("init", [])))
            out = []
            for name, args in case["ops"]:
                if name == "__same__":
                    out.append(obj.find(args[0]) == obj.find(args[1]))
                else:
                    out.append(getattr(obj, name)(*copy.deepcopy(args)))
            return out
        raise ValueError(f"bad case {case!r}")
    return get(default)(*copy.deepcopy(case))


def main():
    student_path, func_name, cases_path, out_path = sys.argv[1:5]
    with open(cases_path, encoding="utf-8") as f:
        cases = ast.literal_eval(f.read())

    result = {"load_error": None, "results": []}
    real_out, real_err = sys.stdout, sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    try:
        try:
            spec = importlib.util.spec_from_file_location("student_module", student_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except BaseException:
            result["load_error"] = "Your file crashed while being imported:\n" + traceback.format_exc(limit=3)
            return result, out_path

        for case in cases:
            try:
                got = execute(module, case, func_name)
                result["results"].append({"repr": repr(got)})
            except AttributeError as e:
                result["results"].append({"error": f"AttributeError: {e} (check the names in the subject)"})
            except BaseException as e:
                result["results"].append({"error": f"{type(e).__name__}: {e}"})
        return result, out_path
    finally:
        sys.stdout, sys.stderr = real_out, real_err


if __name__ == "__main__":
    res, out = main()
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f)

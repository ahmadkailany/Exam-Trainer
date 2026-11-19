"""Child process: imports the student's file and runs the function on every case.

Usage: python runner.py <student_file> <function_name> <cases_file> <out_file>

Runs in its own process so an infinite loop / crash / sys.exit in the student's
code can never take down the examshell. Anything the student prints is swallowed.
"""
import ast
import copy
import importlib.util
import io
import json
import sys
import traceback


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

        func = getattr(module, func_name, None)
        if not callable(func):
            result["load_error"] = f"Function '{func_name}' not found in your file."
            return result, out_path

        for args in cases:
            try:
                got = func(*copy.deepcopy(args))
                result["results"].append({"repr": repr(got)})
            except BaseException as e:
                result["results"].append({"error": f"{type(e).__name__}: {e}"})
        return result, out_path
    finally:
        sys.stdout, sys.stderr = real_out, real_err


if __name__ == "__main__":
    res, out = main()
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f)

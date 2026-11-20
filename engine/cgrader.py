"""Grader for C exam subjects (programs and functions), moulinette style.

Each C exercise folder contains:
    meta.json   {"name", "file", "kind": "program"|"function", "allowed": [...],
                 "headers_first": bool (our include/ wins over the student's headers)}
    ref.c       hidden reference solution (same form as the student file)
    driver.c    (function exercises) a main() that calls the function using argv
    include/    headers the subject provides (ft_list.h, list.h, ...)
    tests.json  [[arg, arg, ...], ...]  - argv for every test run

Grading:
  1. compile the student's file with  cc -Wall -Wextra -Werror
  2. check the undefined symbols (nm) against the allowed functions
  3. link (with driver.c for functions) and build the reference the same way
  4. run both with every argv in tests.json and compare stdout byte for byte
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from engine.pygrader import Result, _fail, _short

STD = ["-std=gnu11"]  # pin the C standard: newer gcc defaults to C23 where `int (*f)()` means (void)
CFLAGS = ["-Wall", "-Wextra", "-Werror", "-fno-builtin"]
# The compiler itself may emit calls to these (struct copies, big zero-inits): only count them
# as forbidden when the student's source really calls them.
COMPILER_EMITTED = ("memset", "memcpy", "memmove")
RUN_TIMEOUT = 5
IS_WIN = os.name == "nt"
EXE = ".exe" if IS_WIN else ""


def find_cc():
    for cc in (os.environ.get("CC"), "cc", "gcc", "clang"):
        if cc and shutil.which(cc):
            return shutil.which(cc)
    return None


def find_nm(cc):
    cands = ["nm", "gcc-nm", "llvm-nm"]
    if cc:
        cands.insert(0, os.path.join(os.path.dirname(cc), "nm" + EXE))
    for c in cands:
        if c and (os.path.isfile(c) or shutil.which(c)):
            return c if os.path.isfile(c) else shutil.which(c)
    return None


def _run(cmd, timeout=60, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd,
                          stdin=subprocess.DEVNULL)


def _compile(cc, sources, out, includes, obj_only=False, strict=True):
    cmd = [cc, *STD, *(CFLAGS if strict else ["-w"])]
    for inc in includes:
        cmd += ["-I", inc]
    cmd += (["-c"] if obj_only else []) + sources + ["-o", out]
    p = _run(cmd)
    return p.returncode == 0, (p.stderr or p.stdout).strip()


def _undefined_symbols(nm, obj):
    p = _run([nm, "-u", obj])
    syms = set()
    for line in p.stdout.splitlines():
        parts = line.split()
        if not parts:
            continue
        name = parts[-1]
        if sys.platform == "darwin" and name.startswith("_"):
            name = name[1:]
        if name.startswith("__imp_"):
            name = name[6:]
        m = re.match(r"__mingw_v?((?:f|s|sn|as)?printf|(?:f|s)?scanf)$", name)
        if m:
            name = m.group(1)
        if name.startswith("__") or name.startswith("_GLOBAL_") or name in ("_alloca", "___chkstk_ms"):
            continue  # compiler / C runtime internals
        syms.add(name)
    return syms


def _crash_reason(rc):
    if rc is None:
        return None
    if IS_WIN:
        codes = {0xC0000005: "Segmentation fault (access violation)", 0xC00000FD: "Stack overflow",
                 0xC0000094: "Division by zero", 0xC0000374: "Heap corruption (bad free?)",
                 0xC0000409: "Stack buffer overrun / abort()"}
        u = rc & 0xFFFFFFFF
        if u in codes:
            return codes[u]
        if u >= 0xC0000000:
            return f"Crashed (exception 0x{u:08X})"
        if rc == 3:
            return "abort() called"
        return None
    if rc < 0:
        import signal
        try:
            return f"{signal.Signals(-rc).name} ({'segfault' if -rc == 11 else 'signal'})"
        except ValueError:
            return f"Killed by signal {-rc}"
    return None


def _exec(exe, args):
    """Returns (stdout_bytes_normalised, crash_reason or 'TIMEOUT' or None)."""
    try:
        p = subprocess.run([exe, *args], capture_output=True, timeout=RUN_TIMEOUT, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return b"", "TIMEOUT"
    out = p.stdout.replace(b"\r\n", b"\n")
    return out, _crash_reason(p.returncode)


def cat_e(data):
    """Show output like `| cat -e`: '$' marks each line end."""
    text = data.decode("utf-8", errors="replace")
    if text == "":
        return "(nothing)"
    shown = text.replace("\t", "^I").replace("\n", "$\n")
    return shown.rstrip("\n")


def _cmdline(name, args, kind):
    def q(a):
        if a == "" or re.search(r"[\s'\"$*?;|&<>()\\!]", a):
            return '"' + a.replace("\\", "\\\\").replace('"', '\\"') + '"'
        return a
    prog = f"./{name}" if kind == "program" else f"./test_{name}"
    return " ".join([prog, *(q(a) for a in args)])


def grade_dir(student_file, exercise_dir):
    with open(os.path.join(exercise_dir, "meta.json"), encoding="utf-8") as f:
        meta = json.load(f)
    with open(os.path.join(exercise_dir, "tests.json"), encoding="utf-8") as f:
        tests = json.load(f)
    name, kind = meta["name"], meta.get("kind", "program")
    total = len(tests)

    if not os.path.isfile(student_file):
        return Result(False, f"File not found: {student_file}")
    cc = find_cc()
    if not cc:
        return Result(False, "No C compiler found. Install gcc (Ubuntu: sudo apt install build-essential, "
                             "Windows: w64devkit or MSYS2) or set the CC environment variable.")

    student_dir = os.path.dirname(os.path.abspath(student_file))
    our_inc = os.path.join(exercise_dir, "include")
    includes = [our_inc, student_dir] if meta.get("headers_first") else [student_dir, our_inc]
    driver = os.path.join(exercise_dir, "driver.c")

    with tempfile.TemporaryDirectory() as tmp:
        # 1. compile student object with the 42 flags
        s_obj = os.path.join(tmp, "student.o")
        ok, err = _compile(cc, [os.path.abspath(student_file)], s_obj, includes, obj_only=True)
        shown = "grademe/" + os.path.basename(student_file)
        err = err.replace(os.path.abspath(student_file), shown).replace(student_file, shown)
        if not ok:
            return Result(False, "Compilation failed (cc -Wall -Wextra -Werror):\n\n" + _short(err), 0, total,
                          {"title": "COMPILATION ERROR", "hint": "Fix every error AND warning - "
                                                                  "the exam compiles with -Wall -Wextra -Werror.",
                           "got": err[:1500], "got_label": "Compiler"})

        # 2. allowed functions
        nm = find_nm(cc)
        allowed = set(meta.get("allowed", []))
        if nm:
            used = _undefined_symbols(nm, s_obj)
            if kind == "function":
                used -= set(meta.get("provided", []))
            with open(student_file, encoding="utf-8", errors="replace") as f:
                source = f.read()
            bad = sorted(s for s in used - allowed
                         if s not in COMPILER_EMITTED or re.search(r"\b" + s + r"\s*\(", source))
            if bad:
                return _fail("FORBIDDEN FUNCTION", 0, total,
                             expected="allowed: " + (", ".join(sorted(allowed)) or "none"),
                             got=", ".join(bad), got_label="You used",
                             hint="Only the functions listed in 'Allowed functions' may be called.")

        # 3. link student + build reference
        s_exe = os.path.join(tmp, "student" + EXE)
        r_exe = os.path.join(tmp, "ref" + EXE)
        extra = [driver] if kind == "function" else []
        ok, err = _compile(cc, [s_obj, *extra], s_exe, includes, strict=False)
        if not ok:
            hint = "Link error."
            if "multiple definition of `main'" in err or "multiple definition of 'main'" in err:
                hint = "Your file must not contain a main() for a function exercise."
            elif "undefined reference" in err:
                hint = f"Check the function name and prototype - it must match the subject exactly."
            return Result(False, hint + "\n\n" + _short(err), 0, total,
                          {"title": "LINK ERROR", "hint": hint, "got": err[:1500], "got_label": "Linker"})
        ref_includes = [our_inc]
        ok, err = _compile(cc, [os.path.join(exercise_dir, "ref.c"), *extra], r_exe, ref_includes, strict=False)
        if not ok:
            return Result(False, "Internal error: reference solution does not compile:\n" + err, 0, total)

        # 4. run every test
        for i, args in enumerate(tests):
            exp, rcrash = _exec(r_exe, args)
            got, crash = _exec(s_exe, args)
            call = _cmdline(name, args, kind) + "  | cat -e"
            if crash == "TIMEOUT":
                return _fail(f"Test {i + 1}/{total} TIMEOUT (> {RUN_TIMEOUT}s)", i, total, call,
                             hint="Infinite loop? (or waiting for input)")
            if crash:
                return _fail(f"Test {i + 1}/{total} CRASHED", i, total, call, cat_e(exp), crash,
                             got_label="Crash")
            if got != exp:
                return _fail(f"Test {i + 1}/{total} FAILED", i, total, call, cat_e(exp), cat_e(got))

    return Result(True, f"All {total} tests passed.", total, total)

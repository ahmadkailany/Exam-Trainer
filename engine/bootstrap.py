"""Auto-installer: makes sure we run inside ./.venv with the requirements installed.

Standard library only - this runs before `rich` exists.

    python examshell.py            -> creates .venv + installs deps on first run, then restarts inside it
    python examshell.py --install  -> only (re)install, then exit
    EXAM_TRAINER_NO_VENV=1         -> skip the venv and use the current Python
"""
import os
import subprocess
import sys

TAG = "[Exam Trainer]"

if os.name == "nt":
    os.system("")  # enable ANSI colours on older Windows consoles


def _venv_python(venv):
    if os.name == "nt":
        return os.path.join(venv, "Scripts", "python.exe")
    return os.path.join(venv, "bin", "python")


def _same(a, b):
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))


def _has_deps(python):
    return subprocess.call([python, "-c", "import rich"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


def _say(msg):
    print(f"\033[1;36m{TAG}\033[0m {msg}", flush=True)


def install(root, force=False):
    """Creates .venv and installs requirements. Returns the venv python path, or None on failure."""
    venv = os.path.join(root, ".venv")
    py = _venv_python(venv)
    req = os.path.join(root, "requirements.txt")

    if not os.path.isfile(py):
        _say("First run: creating a virtual environment in .venv ...")
        if subprocess.call([sys.executable, "-m", "venv", venv]) != 0 or not os.path.isfile(py):
            _say("Could not create the virtual environment.")
            _say("On Debian/Ubuntu: sudo apt install python3-venv   (or set EXAM_TRAINER_NO_VENV=1)")
            return None

    if force or not _has_deps(py):
        _say("Installing dependencies (rich) ... this only happens once.")
        cmd = [py, "-m", "pip", "install", "--disable-pip-version-check", "-q", "-r", req]
        if subprocess.call(cmd) != 0:
            _say("pip install failed - check your internet connection and try again.")
            return None
        _say("Installation complete.")
    # Same stamp the Makefile uses, so `make` knows the venv is ready.
    open(os.path.join(venv, ".installed"), "w").close()
    return py


def ensure(root):
    """Call at the very top of the entry script, before importing rich."""
    if "--install" in sys.argv:
        ok = install(root, force=True)
        sys.exit(0 if ok else 1)

    if os.environ.get("EXAM_TRAINER_NO_VENV"):
        return

    venv = os.path.join(root, ".venv")
    if _same(sys.prefix, venv):
        return  # already inside our venv

    py = install(root)
    if py is None:
        try:
            import rich  # noqa: F401  - system python has it, carry on without the venv
            _say("Continuing with the system Python.")
            return
        except ImportError:
            sys.exit(1)

    # Restart the program with the venv's python (subprocess, not exec: keeps the console on Windows).
    script = os.path.abspath(sys.argv[0])
    try:
        sys.exit(subprocess.call([py, script, *sys.argv[1:]]))
    except KeyboardInterrupt:
        sys.exit(130)

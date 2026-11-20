import os

from engine.cgrader import grade_dir


def grade(path):
    return grade_dir(path, os.path.dirname(os.path.abspath(__file__)))

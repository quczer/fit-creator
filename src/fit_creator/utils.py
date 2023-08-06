import json
from pathlib import Path

from fit_creator.workout.model import Workout


def fix_file_name(name: str) -> str:
    return name.replace(" ", "_").replace("/", "|")

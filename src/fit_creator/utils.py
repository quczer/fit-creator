import json
from pathlib import Path

from fit_creator.workout.model import Workout


def load_wkt(wkt_file_path: Path) -> Workout:
    with open(wkt_file_path, "r") as f:
        wkt_dict = json.load(f)
        return Workout.deserialize(wkt_dict)


def save_wkt(workout: Workout, wkt_file_path: Path) -> None:
    with open(wkt_file_path, "w") as f:
        wkt_dict = workout.serialize()
        json.dump(wkt_dict, f, indent=2)


def fix_file_name(name: str) -> str:
    return name.replace(" ", "_").replace("/", "|")

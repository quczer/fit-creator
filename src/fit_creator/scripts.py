import json
import os
import subprocess
from pathlib import Path

import click

from fit_creator.config import ROOT_DIR
from fit_creator.converter import fit_workout_to_fit_dict, workout_to_fit_dict
from fit_creator.utils import load_wkt


@click.group()
def cli():
    """This is the main entry point for the CLI."""
    pass


@cli.command()
@click.option("--fit_file_path", type=Path, required=True)
@click.option("--out_json_path", type=Path, required=True)
def convert_fit_workout_to_json(fit_file_path: Path, out_json_path: Path) -> None:
    with open(fit_file_path, "rb") as f:
        fit_bytes = bytearray(f.read())
    fit_dict = fit_workout_to_fit_dict(fit_bytes)

    with open(out_json_path, "w") as f:
        json.dump(fit_dict, f, indent=2)


@cli.command()
@click.option("--wkt_file_path", type=Path, required=True)
@click.option("--out_json_path", type=Path, required=True)
def convert_wkt_workout_to_json(wkt_file_path: Path, out_json_path: Path) -> None:
    workout = load_wkt(wkt_file_path)
    fit_dict = workout_to_fit_dict(workout)
    with open(out_json_path, "w") as f:
        json.dump(fit_dict, f, indent=2)


@cli.command()
def convert_all_fit_files_to_jsons() -> None:
    for file in os.listdir(ROOT_DIR / "generated" / "fit"):
        subprocess.run(
            [
                "python",
                ROOT_DIR / "src" / "fit_creator" / "scripts.py",
                "convert-fit-workout-to-json",
                "--fit_file_path",
                ROOT_DIR / "generated" / "fit" / file,
                "--out_json_path",
                ROOT_DIR
                / "generated"
                / "json_from_fit"
                / file.replace(".fit", ".json"),
            ]
        )


@cli.command()
@click.option("--json_file_path", type=Path, required=True)
@click.option("--out_fit_path", type=Path, required=True)
def convert_json_workout_to_fit(json_file_path: Path, out_fit_path: Path) -> None:
    subprocess.run(
        [
            "dotnet",
            "run",
            "--project",
            ROOT_DIR / "dotnet",
            "--property",
            "WarningLevel=0",
            json_file_path,
            out_fit_path,
        ]
    )


if __name__ == "__main__":
    cli()

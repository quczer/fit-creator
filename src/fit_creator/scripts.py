import json
from pathlib import Path

import click

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


if __name__ == "__main__":
    cli()

import json
import os
import subprocess
import tempfile
from pathlib import Path

import click

from fit_creator.config import DATA_DIR, DOTNET_DIR
from fit_creator.constants import ZWIFT_WORKOUTS_URL
from fit_creator.fit.converter import fit_workout_to_fit_dict
from fit_creator.utils import fix_file_name, load_wkt, save_wkt
from fit_creator.workout.converter import workout_to_fit_dict
from fit_creator.zwift.converter import zwift_raw_workout_to_wkt
from fit_creator.zwift.extractor import (
    extract_workout_plan_urls,
    extract_zwift_workouts,
)
from fit_creator.zwift.utils import download_html_page, save_html_page


def export_fit_workout_to_json_cmd(fit_file_path: Path, out_json_path: Path) -> None:
    with open(fit_file_path, "rb") as f:
        fit_bytes = bytearray(f.read())
    fit_dict = fit_workout_to_fit_dict(fit_bytes)

    with open(out_json_path, "w") as f:
        json.dump(fit_dict, f, indent=2)


def export_wkt_workout_to_json_cmd(wkt_file_path: Path, out_json_path: Path) -> None:
    workout = load_wkt(wkt_file_path)
    fit_dict = workout_to_fit_dict(workout)
    with open(out_json_path, "w") as f:
        json.dump(fit_dict, f, indent=2)


def export_json_workout_to_fit_cmd(
    json_file_path: Path, out_fit_path: Path, verbose: bool
) -> None:
    cmd = [
        "dotnet",
        "run",
        "--project",
        DOTNET_DIR,
        "--property",
        "WarningLevel=0",
        json_file_path,
        out_fit_path,
    ]
    if verbose:
        cmd += ["--verbose"]
    subprocess.run(cmd)


def export_wkt_workout_to_fit_cmd(wkt_file_path: Path, out_fit_path: Path) -> None:
    with tempfile.NamedTemporaryFile() as tmp_json:
        tmp_json_path = Path(tmp_json.name)
        export_wkt_workout_to_json_cmd(wkt_file_path, tmp_json_path)
        export_json_workout_to_fit_cmd(tmp_json_path, out_fit_path, False)


def export_zwift_workout_to_wkt_cmd(html_file_path: Path, out_wkt_dir: Path) -> None:
    with open(html_file_path, "r") as f:
        zwift_workouts = extract_zwift_workouts(f.read())
    subdir_name = fix_file_name(html_file_path.name).removesuffix(".html")
    save_dir = out_wkt_dir / subdir_name  # let the subdir be the name of the html file
    save_dir.mkdir(parents=True, exist_ok=True)

    for zwift_workout in zwift_workouts:
        wkt_workout = zwift_raw_workout_to_wkt(zwift_workout)
        save_wkt(wkt_workout, save_dir / f"{fix_file_name(wkt_workout.name)}.wkt")


def download_all_workout_pages_cmd(verbose: bool) -> None:
    # assert that these folders exist
    target_dir = DATA_DIR / "html" / "zwift" / "workout_plans"
    target_dir.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"Downloading page with all workouts from {ZWIFT_WORKOUTS_URL}")
    workouts_html = download_html_page(ZWIFT_WORKOUTS_URL)
    save_html_page(workouts_html, DATA_DIR / "html" / "zwift" / "workouts_main.html")
    urls = extract_workout_plan_urls(workouts_html)

    if verbose:
        print(f"Found {len(urls)} workout pages")
        print(f"All workouts will be saved in {target_dir}")
    for name, url in urls.items():
        if verbose:
            print(f"Downloading page for workout {name} from {url}")
        workout_html = download_html_page(url)
        target_file_path = target_dir / f"{fix_file_name(name)}.html"
        if verbose:
            print(f"Saving in {target_file_path}")
        save_html_page(workout_html, target_file_path)


@click.group()
def cli():
    """This is the main entry point for the CLI."""
    pass


@cli.command()
@click.option("--fit_file_path", type=Path, required=True)
@click.option("--out_json_path", type=Path, required=True)
def export_fit_workout_to_json(fit_file_path: Path, out_json_path: Path) -> None:
    export_fit_workout_to_json_cmd(fit_file_path, out_json_path)


@cli.command()
@click.option("--wkt_file_path", type=Path, required=True)
@click.option("--out_json_path", type=Path, required=True)
def export_wkt_workout_to_json(wkt_file_path: Path, out_json_path: Path) -> None:
    export_wkt_workout_to_json_cmd(wkt_file_path, out_json_path)


@cli.command()
@click.option("--json_file_path", type=Path, required=True)
@click.option("--out_fit_path", type=Path, required=True)
def export_json_workout_to_fit(json_file_path: Path, out_fit_path: Path) -> None:
    export_json_workout_to_fit_cmd(json_file_path, out_fit_path, True)


@cli.command()
def export_all_fit_files_to_jsons() -> None:
    for file in os.listdir(DATA_DIR / "generated" / "fit"):
        export_fit_workout_to_json_cmd(
            DATA_DIR / "generated" / "fit" / file,
            (DATA_DIR / "generated" / "json_from_fit" / file).with_suffix(".json"),
        )


@cli.command()
@click.option("--verbose", is_flag=True, default=False)
def download_all_workout_pages(verbose: bool) -> None:
    download_all_workout_pages_cmd(verbose)


@cli.command()
@click.option("--html_path", type=Path, required=True)
@click.option("--out_wkt_dir", type=Path, required=True)
@click.option("--verbose", is_flag=True, default=False)
def export_zwift_workout_to_wkt(
    html_path: Path, out_wkt_dir: Path, verbose: bool
) -> None:
    """If `html_path` is a file, it will be converted to a fit file and saved in `out_wkt_dir`.
    If `html_path` is a directory, all wkt files in it will be converted to fit files and saved in `out_wkt_dir`.
    """
    if verbose:
        print(f"Searching for .html files in {html_path}")
    for html_file in html_path.rglob("*.html"):
        target_dir = out_wkt_dir.joinpath(html_file.relative_to(html_path)).parent
        if verbose:
            print(f"Exporting {html_file} -> {target_dir}")
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        export_zwift_workout_to_wkt_cmd(html_file, target_dir)


@cli.command()
@click.option("--wkt_path", type=Path, required=True)
@click.option("--out_fit_dir", type=Path, required=True)
@click.option("--verbose", is_flag=True, default=False)
def export_wkt_workouts_to_fit(
    wkt_path: Path, out_fit_dir: Path, verbose: bool
) -> None:
    """If `wkt_path` is a file, it will be converted to a fit file and saved in `out_fit_dir`.
    If `wkt_path` is a directory, all wkt files in it will be converted to fit files and saved in `out_fit_dir`.
    """
    if verbose:
        print(f"Searching for .wkt files in {wkt_path}")
    for wkt_file in wkt_path.rglob("*.wkt"):
        target_file = out_fit_dir.joinpath(wkt_file.relative_to(wkt_path)).with_suffix(
            ".fit"
        )
        if verbose:
            print(f"Converting {wkt_file} -> {target_file}")
        target_file.parent.mkdir(parents=True, exist_ok=True)
        export_wkt_workout_to_fit_cmd(wkt_file, target_file)


if __name__ == "__main__":
    cli()

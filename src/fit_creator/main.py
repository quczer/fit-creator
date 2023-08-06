from pathlib import Path

import click

from fit_creator.scripts import (
    download_all_workout_pages_cmd,
    export_wkt_workout_to_fit_cmd,
    export_zwift_workout_to_wkt_cmd,
)
from fit_creator.utils import fix_file_name


@click.group()
def cli():
    """This is the main entry point for the CLI."""
    pass


@cli.command()
@click.option("--verbose", is_flag=True, default=False)
def download_all_workout_pages(verbose: bool) -> None:
    download_all_workout_pages_cmd(verbose)


@cli.command()
@click.option("--html_path", type=Path, required=True)
@click.option("--out_wkt_dir", type=Path, required=True)
@click.option("--verbose", is_flag=True, default=False)
def export_zwift_workouts_to_wkt(
    html_path: Path, out_wkt_dir: Path, verbose: bool
) -> None:
    """If `html_path` is a file, it will be converted to a fit file and saved in `out_wkt_dir`.
    If `html_path` is a directory, all wkt files in it will be converted to fit files and saved in `out_wkt_dir`.
    """
    if verbose:
        print(f"Searching for .html files in {html_path}")

    files = [html_path] if html_path.is_file() else html_path.rglob("*.html")
    for html_file in files:
        target_file = out_wkt_dir.joinpath(html_file.relative_to(html_path))
        target_dir = target_file.parent / fix_file_name(target_file.name).removesuffix(
            ".html"
        )
        if verbose:
            print(f"Exporting {html_file} -> {target_dir}")
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
    files = [wkt_path] if wkt_path.is_file() else wkt_path.rglob("*.wkt")
    for wkt_file in files:
        target_file = out_fit_dir.joinpath(wkt_file.relative_to(wkt_path)).with_suffix(
            ".fit"
        )
        if verbose:
            print(f"Converting {wkt_file} -> {target_file}")
        target_file.parent.mkdir(parents=True, exist_ok=True)
        export_wkt_workout_to_fit_cmd(wkt_file, target_file)


if __name__ == "__main__":
    cli()

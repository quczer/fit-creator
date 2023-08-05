from pathlib import Path

import requests

from fit_creator.config import DATA_DIR
from fit_creator.constants import ZWIFT_WORKOUTS_URL


def download_html_page(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def save_html_page(html_file: str, file_path: Path) -> None:
    with open(file_path.with_suffix(".html"), "w") as file:
        file.write(html_file)

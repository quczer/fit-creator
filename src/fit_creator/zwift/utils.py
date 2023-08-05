import requests

from fit_creator.config import DATA_DIR
from fit_creator.constants import ZWIFT_WORKOUTS_URL


def download_html_page(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def save_html_page(html_file: str, file_name: str, subdir: str | None = None) -> None:
    path = DATA_DIR / "html" / "zwift"
    if subdir is not None:
        path = path / subdir
    with open(path / f"{file_name}.html", "w") as file:
        file.write(html_file)

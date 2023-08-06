from pathlib import Path

import requests


def download_html_page(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def save_html_page(html_file: str, file_path: Path) -> None:
    with open(file_path.with_suffix(".html"), "w") as file:
        file.write(html_file)

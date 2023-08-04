import requests

from fit_creator.constants import ZWIFT_WORKOUTS_URL


def download_html_page(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def download_all_workout_urls() -> list[str]:
    ...

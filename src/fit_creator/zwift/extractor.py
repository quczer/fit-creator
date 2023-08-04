from bs4 import BeautifulSoup

from fit_creator.zwift.model import ZwiftRawWorkout


def exctract_zwift_workouts(html_file: str) -> list[ZwiftRawWorkout]:
    soup = BeautifulSoup(html_file, "html.parser")
    workouts = []
    for article in soup.find_all("article"):
        if {"id", "class"}.issuperset(article.attrs.keys()):
            data = dict(
                **_extract_workout_names(article),
                steps=_extract_workout_routine(article)
            )
            workouts.append(ZwiftRawWorkout(**data))
        # break
    return workouts


def _extract_workout_names(article) -> dict[str, str | int]:
    breadcrumbs = article.find("div", {"class": "breadcrumbs"})
    plan, week = breadcrumbs.find_all("a")
    workout = breadcrumbs.find("h4")
    return {
        "plan_name": plan.text,
        "week_name": week.text,
        "workout_name": workout.text,
    }


def _extract_workout_routine(article) -> list[str]:
    container = article.find("div", {"class": "one-third column workoutlist"})
    steps = []
    for child in container.find_all("div"):
        steps.append(child.get_text())
    return steps

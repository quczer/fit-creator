import bs4

from fit_creator.zwift.model import ZwiftRawWorkout


def extract_zwift_bike_workouts(html_file: str) -> list[ZwiftRawWorkout]:
    soup = bs4.BeautifulSoup(html_file, "html.parser")
    workouts = []
    for article in soup.find_all("article"):
        if {"id", "class"}.issuperset(article.attrs.keys()):
            if "flaticon-run" in article.find("h4").get("class"):
                continue  # try to filter out run workouts
            data = dict(
                **_extract_workout_names(article),
                steps=_extract_workout_routine(article)
            )
            workouts.append(ZwiftRawWorkout(**data))
    return workouts


def extract_workout_plan_urls(html_file: str) -> dict[str, str]:
    soup = bs4.BeautifulSoup(html_file, "html.parser")
    urls = {}
    for card in soup.find_all("div", {"class": "card"}):
        name = card.find("div", {"class": "card-title"}).find("p").text
        url = card.find("div", {"class": "card-link"}).find("a").get("href")
        urls[name] = url
    return urls


def _extract_workout_names(article: bs4.Tag) -> dict[str, str | None]:
    breadcrumbs = article.find("div", {"class": "breadcrumbs"})
    a_tags = breadcrumbs.find_all("a")
    plan, week = a_tags[:2] if len(a_tags) > 1 else (a_tags[0], None)
    workout = breadcrumbs.find("h4")
    return {
        "plan_name": plan.text.strip(),
        "week_name": week.text.strip() if week else None,
        "workout_name": workout.text.strip(),
    }


def _extract_workout_routine(article) -> list[str]:
    container = article.find("div", {"class": "one-third column workoutlist"})
    steps = []
    for child in container.find_all("div"):
        steps.append(child.get_text())
    return steps

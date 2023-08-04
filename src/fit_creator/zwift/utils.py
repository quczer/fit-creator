from fit_creator.config import DATA_DIR


def save_html_page(html_file: str, file_name: str) -> None:
    with open(DATA_DIR / "html" / "zwift" / f"{file_name}.html", "w") as file:
        file.write(html_file)

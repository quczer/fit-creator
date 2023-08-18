from setuptools import find_packages, setup

setup(
    name="fit-creator",
    version="1.0.0",
    description="Python package capable of downloading workouts from whatsonzwift.com and converting them to garmin FIT workouts.",
    author="Michal Kucharczyk",
    author_email="kucharczi@gmail.com",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["garmin-fit-sdk", "click", "beautifulsoup4>=4.12", "requests>=2.31.0"],
    extras_require={"dev": ["black", "isort", "ipykernel", "pandas>=2.0"]},
    python_requires=">=3.10",
)

from setuptools import find_packages, setup

setup(
    name="wourkout-converter",
    version="0.0.0.dev0",
    description="Python package capable of downloading workouts from whatsonzwift.com and converting them to garmin workouts.",
    author="Michal Kucharczyk",
    author_email="kucharczi@gmail.com",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "fit-tool>=0.9.13"
    ],
    python_requires=">=3.10",
)
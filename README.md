# Python (and C#) project for scraping ZWIFT workouts and converting them to FIT Garmin workouts

## 1. Installation
### Using docker
### Manual
1. Install any C# executable and add `dotnet/Dynasream.FIT.Portable.dll` dependency
2. Install `fit_creator` python package e.g. using `pip` with
    ```
    pip install .
    ```
## 2. Basic usage
Just shell-execute
```
run.sh
```
It does three steps:
1. Download all available html workout pages from `whatsonzwift.com/workouts` and saves them in `data/html/zwift` directory (somewhat time consuming - the internet is the bottleneck).
2. Scrapes relevant info from each download page and saves workouts in `.wkt` format in `data/workouts/wkt` directory. (for all workouts, fast)
3. Converts workouts from _Build Me Up_ plan from `data/workouts/wkt/Build_Me_Up` from `.wkt` to `.fit` format and saves them in `data/workouts/fit` directory. This is veeeery time consuming. The work is done via `dotnet run` and it's C# code executed there - that's why I do this only for one (my favourite) plan. You can just run the last python command in `run.sh` with _your favourite plan_ in place of _Build_Me_Up_.

Time: (downloading excluded) \
real    2m44.838s \
user    2m59.810s \
sys     0m11.321s 
## 3. Interesting stuff
I wrote my own serialization decorator.
```python
@serializable
@dataclass
class Workout:
    name: str
    steps: list[WorkoutStep | WorkoutStepRepeat]
    created: datetime = datetime.now()
```
It solves the problem of flat deserializations performed by `@dataclasses_json` and maybe other libraries, as they don't seem to keep any information about the origin class. Therefore one can infer if a particular item in `steps` is `WorkoutStep` or `WorkoutStepRepeat`.
The decorator adds 4 methods `serialize`, `deserialize`, `load` and `save` to your dataclass object and is easily extensible to support other data types.
from dataclasses import dataclass


@dataclass
class ZwiftRawWorkout:
    workout_name: str
    week_name: str | None
    plan_name: str | None
    steps: list[str]

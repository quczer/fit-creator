from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from fit_creator.workout.serializable import serializable


class Intensity(Enum):
    WARMUP = "warmup"
    MAIN = "active"
    RECOVERY = "recovery"
    COOLDOWN = "cooldown"


class TargetType(Enum):
    NONE = "open"
    POWER = "power"
    # POWER_3S = "power_3s" # not supported by Garmin
    # POWER_10S = "power_10s"
    # POWER_30S = "power_30s"


class DurationType(Enum):
    NONE = "open"
    TIME = "time"
    REPEAT = "repeat_until_steps_cmplt"


@serializable
@dataclass
class WorkoutStep:
    duration: timedelta
    target_type: TargetType
    intensity: Intensity
    power_ftp_percent: int | None = None
    power_absolute: int | None = None
    cadence: int | None = None

    def __post_init__(self):
        powers_present = (self.power_absolute is not None) + (
            self.power_ftp_percent is not None
        )
        assert powers_present < 2
        if self.target_type == TargetType.POWER:
            assert powers_present == 1


@serializable
@dataclass
class WorkoutStepRepeat:
    steps: list[WorkoutStep]
    repeats: int


@serializable
@dataclass
class Workout:
    name: str
    steps: list[WorkoutStep | WorkoutStepRepeat]
    created: datetime = datetime.now()

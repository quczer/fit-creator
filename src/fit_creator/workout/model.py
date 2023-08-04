from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from fit_creator.workout.serializer import ClassRegistry, JSONSerializableMixin


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


@dataclass
class WorkoutStep(JSONSerializableMixin):
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


@dataclass
class WorkoutStepRepeat(JSONSerializableMixin):
    steps: list[WorkoutStep]
    repeats: int


@dataclass
class Workout(JSONSerializableMixin):
    name: str
    steps: list[WorkoutStep | WorkoutStepRepeat]
    created: datetime = datetime.now()


ClassRegistry.register_class(Workout)
ClassRegistry.register_class(WorkoutStep)
ClassRegistry.register_class(WorkoutStepRepeat)

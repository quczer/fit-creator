from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from fit_creator.serializer import ClassRegistry, JSONSerializableMixin


class Intensity(Enum):
    WARMUP = "warmup"
    MAIN = "active"
    RECOVERY = "recovery"
    COOLDOWN = "cooldown"


class TargetType(Enum):
    NONE = "open"
    POWER_3S = "power_3s"
    POWER_10S = "power_10s"
    POWER_30S = "power_30s"


class DurationType(Enum):
    NONE = "open"
    TIME = "time"
    REPEAT = "repeat_until_steps_cmplt"


@dataclass
class WorkoutStep(JSONSerializableMixin):
    duration: timedelta
    power_ftp_percent: int | None
    cadence: int | None
    target_type: TargetType
    intensity: Intensity


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

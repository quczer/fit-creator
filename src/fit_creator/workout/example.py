from datetime import timedelta

from fit_creator.workout.model import (
    Intensity,
    TargetType,
    Workout,
    WorkoutStep,
    WorkoutStepRepeat,
)

SOME_WORKOUT = Workout(
    "some_workout",
    [
        WorkoutStep(timedelta(minutes=3), TargetType.NONE, Intensity.WARMUP),
        WorkoutStep(
            timedelta(minutes=2),
            TargetType.POWER,
            Intensity.WARMUP,
            power_ftp_percent=80,
        ),
        WorkoutStepRepeat(
            [
                WorkoutStep(
                    timedelta(minutes=1, seconds=30),
                    TargetType.POWER,
                    Intensity.MAIN,
                    power_ftp_percent=90,
                    cadence=100,
                ),
                WorkoutStep(
                    timedelta(minutes=3),
                    TargetType.POWER,
                    Intensity.MAIN,
                    power_absolute=400,
                    cadence=120,
                ),
            ],
            repeats=3,
        ),
        WorkoutStep(timedelta(minutes=10), TargetType.NONE, Intensity.COOLDOWN),
    ],
)

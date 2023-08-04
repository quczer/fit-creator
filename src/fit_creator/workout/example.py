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
        WorkoutStep(
            timedelta(minutes=3), None, None, TargetType.NONE, Intensity.WARMUP
        ),
        WorkoutStep(timedelta(minutes=2), 80, None, TargetType.POWER, Intensity.WARMUP),
        WorkoutStepRepeat(
            [
                WorkoutStep(
                    timedelta(minutes=1, seconds=30),
                    90,
                    100,
                    TargetType.POWER,
                    Intensity.MAIN,
                ),
                WorkoutStep(
                    timedelta(minutes=3), 100, 100, TargetType.POWER, Intensity.MAIN
                ),
            ],
            repeats=3,
        ),
        WorkoutStep(
            timedelta(minutes=10), None, None, TargetType.NONE, Intensity.COOLDOWN
        ),
    ],
)

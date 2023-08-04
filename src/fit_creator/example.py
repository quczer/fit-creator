from fit_creator.model import (
    DurationType,
    Intensity,
    TargetType,
    Workout,
    WorkoutStep,
    WorkoutStepRepeat,
)

SOME_WORKOUT = Workout(
    "some_workout",
    [
        WorkoutStep(3 * 60, None, None, TargetType.NONE, Intensity.WARMUP),
        WorkoutStep(2 * 60, 80, None, TargetType.POWER_3S, Intensity.WARMUP),
        WorkoutStepRepeat(
            [
                WorkoutStep(1 * 60, 90, 100, TargetType.POWER_3S, Intensity.MAIN),
                WorkoutStep(3 * 60, 100, 100, TargetType.POWER_3S, Intensity.MAIN),
            ],
            repeats=3,
        ),
        WorkoutStep(10 * 60, None, None, TargetType.NONE, Intensity.COOLDOWN),
    ],
)

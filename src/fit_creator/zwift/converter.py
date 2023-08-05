import re
from datetime import timedelta

from fit_creator.workout.model import (
    Intensity,
    TargetType,
    Workout,
    WorkoutStep,
    WorkoutStepRepeat,
)
from fit_creator.zwift.model import ZwiftRawWorkout


class ZwiftParseException(Exception):
    pass


def zwift_raw_workout_to_wkt(zwift_workout: ZwiftRawWorkout) -> Workout:
    name = f"{zwift_workout.plan_name} - {zwift_workout.week_name} - {zwift_workout.workout_name}"
    steps = [_zwift_to_workout_step(step) for step in zwift_workout.steps]
    return Workout(name=name, steps=steps)


def _zwift_to_workout_step(zwift_step: str) -> WorkoutStep | WorkoutStepRepeat:
    if (reps := _find_repetitions(zwift_step)) is not None:
        single_steps = _split_multiple_step(zwift_step)
        workout_steps = [_zwift_to_workout_step(step) for step in single_steps]
        return WorkoutStepRepeat(steps=workout_steps, repeats=reps)
    else:
        power = _find_power(zwift_step)
        power_ftp_pct = _find_power_ftp_pct(zwift_step)
        cadence = _find_cadence(zwift_step)
        duration = _find_duration(zwift_step)
        target_type = _find_target_type(zwift_step)
        if (power is not None) and (power_ftp_pct is not None):
            raise ZwiftParseException(
                f"Found both {power = } and {power_ftp_pct = } for {zwift_step}"
            )
        return WorkoutStep(
            duration=duration,
            power_absolute=power,
            power_ftp_percent=power_ftp_pct,
            cadence=cadence,
            intensity=Intensity.MAIN,  # TODO: fix later
            target_type=target_type,
        )


def _find_repetitions(zwift_step: str) -> int | None:
    match = re.search("(\d+)x", zwift_step)
    return int(match.group(1)) if match else None


def _find_duration(zwift_step: str) -> timedelta:
    hrs = re.search("(\d+)hr", zwift_step)
    mins = re.search("(\d+)min", zwift_step)
    secs = re.search("(\d+)sec", zwift_step)
    if (hrs is None) and (mins is None) and (secs is None):
        raise ZwiftParseException(f"Could not find duration for {zwift_step}")
    return timedelta(
        hours=int(hrs.group(1)) if hrs else 0,
        minutes=int(mins.group(1)) if mins else 0,
        seconds=int(secs.group(1)) if secs else 0,
    )


def _find_power(zwift_step: str) -> int | None:
    match_range = re.search("from (\d+) to (\d+)W", zwift_step)
    match_simple = re.search("(\d+)W", zwift_step)
    if match_range:
        # workaround for range
        return (int(match_range.group(1)) + int(match_range.group(2))) // 2
    if match_simple:
        return int(match_simple.group(1))
    return None


def _find_power_ftp_pct(zwift_step: str) -> int | None:
    match_range = re.search("from (\d+) to (\d+)% FTP", zwift_step)
    match_simple = re.search("(\d+)% FTP", zwift_step)
    if match_range:
        # workaround for range
        return (int(match_range.group(1)) + int(match_range.group(2))) // 2
    if match_simple:
        return int(match_simple.group(1))
    return None


def _find_cadence(zwift_step: str) -> int | None:
    match = re.search("(\d+)rpm", zwift_step)
    return int(match.group(1)) if match else None


def _find_target_type(zwift_step: str) -> TargetType:
    match = re.search("free ride", zwift_step)
    return TargetType.NONE if match else TargetType.POWER


def _split_multiple_step(zwift_step: str) -> list[str]:
    parts = re.split(r"(\d+hr[^,]+,|\d+min[^,]+,|\d+sec[^,]+,)", zwift_step)
    assert len(parts) % 2 == 1
    return [parts[i] + parts[i + 1].removesuffix(",") for i in range(1, len(parts), 2)]

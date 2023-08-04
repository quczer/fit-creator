import uuid
from datetime import datetime
from typing import Sequence

import fit_creator.constants as C
from fit_creator.workout.model import (
    DurationType,
    Workout,
    WorkoutStep,
    WorkoutStepRepeat,
)

MAX_UINT32 = 2**32 - 1


def workout_to_fit_dict(workout: Workout) -> dict:
    workout_steps = _create_workout_steps(workout.steps, 0)
    workout_dict = {
        "file_id_mesgs": [_create_file_id_mesg()],
        "workout_mesgs": [
            _create_workout_mesg(workout.name, len(workout_steps)),
        ],
        "workout_step_mesgs": workout_steps,
    }
    return workout_dict


def _create_workout_steps(
    steps: Sequence[WorkoutStep | WorkoutStepRepeat], idx: int
) -> list[dict[str, str | float]]:
    res = []
    for step in steps:
        new_steps = _create_workout_step(step, idx)
        res.extend(new_steps)
        idx += len(new_steps)
    return res


def _create_workout_step(
    step: WorkoutStep | WorkoutStepRepeat, idx: int
) -> list[dict[str, str | float]]:
    if isinstance(step, WorkoutStep):
        single_res = {
            "duration_value": int(step.duration.total_seconds()) * 1000,
            "target_value": 0,
            "message_index": idx,
            "duration_type": DurationType.TIME.value,
            "intensity": step.intensity.value,
            "target_type": step.target_type.value,
            # "duration_time": 600.0,
        }
        if step.power_ftp_percent is not None:
            single_res.update(
                **{
                    "custom_target_value_low": step.power_ftp_percent
                    - C.POWER_FTP_PCT_WIDTH,
                    "custom_target_value_high": step.power_ftp_percent
                    + C.POWER_FTP_PCT_WIDTH,
                }
            )
        elif step.power_absolute is not None:  # either absolute or percent
            single_res.update(
                **{
                    "custom_target_value_low": step.power_absolute
                    + C.POWER_ABSOLUTE_OFFSET
                    - C.POWER_ABSOLUTE_WIDTH,
                    "custom_target_value_high": step.power_absolute
                    + C.POWER_ABSOLUTE_OFFSET
                    + C.POWER_ABSOLUTE_WIDTH,
                }
            )
        if step.cadence is not None:
            single_res.update(
                **{
                    "secondary_custom_target_value_low": step.cadence - C.CADENCE_WIDTH,
                    "secondary_custom_target_value_high": step.cadence
                    + C.CADENCE_WIDTH,
                }
            )
        return [single_res]
    else:
        multi_res = _create_workout_steps(step.steps, idx)
        multi_res.append(
            {
                "duration_value": idx,
                "target_value": step.repeats,
                "message_index": idx + len(step.steps),
                "duration_type": DurationType.REPEAT.value,
                "duration_step": idx,
                "repeat_steps": step.repeats,
            }
        )
        return multi_res


def _create_file_id_mesg() -> dict[str, str | int]:
    return {
        "type": "workout",
        "manufacturer": "development",
        "product": 0,
        "time_created": int(datetime.now().timestamp()),
        "serial_number": uuid.uuid4().int % MAX_UINT32,
    }


def _create_workout_mesg(name: str, steps: int) -> dict[str, str | int]:
    return {"wkt_name": name, "sport": "cycling", "num_valid_steps": steps}

from datetime import datetime

from garmin_fit_sdk import Decoder, Stream


class FitDeserialiationError(Exception):
    pass


def fit_workout_to_fit_dict(fit_bytes: bytearray) -> dict:
    stream = Stream.from_byte_array(fit_bytes)
    decoder = Decoder(stream)
    messages, errors = decoder.read()

    if len(errors) > 0:
        raise FitDeserialiationError(errors)
    return _cast_types(messages)


def _cast_types(obj: object) -> object:
    if isinstance(obj, dict):
        return {key: _cast_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_cast_types(v) for v in obj]
    elif isinstance(obj, datetime):
        return int(obj.timestamp())
    return obj

import abc
import json
from dataclasses import fields, is_dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar, Type


class ClassRegistry:
    name_registry: ClassVar[dict[str, Type]] = {}
    class_registry: ClassVar[dict[Type, str]] = {}

    @classmethod
    def register_class(cls, class_: Type) -> None:
        class_name = cls._mangle_class_name(class_)
        cls.name_registry[class_name] = class_
        cls.class_registry[class_] = class_name

    @staticmethod
    def _mangle_class_name(class_: Type) -> str:
        return f"__{class_.__name__}__"


def serializable(cls: Type) -> Type:
    if not is_dataclass(cls):
        raise TypeError("Can only decorate dataclasses")
    ClassRegistry.register_class(cls)
    setattr(cls, "serialize", serialize)
    setattr(cls, "deserialize", deserialize)
    setattr(cls, "load", load)
    setattr(cls, "save", save)
    abc.update_abstractmethods(cls)  # is it required?
    return cls


def load(file_path: Path | str) -> object:
    with open(file_path, "r") as f:
        serialized = json.load(f)
        return deserialize(serialized)


def save(obj: object, file_path: Path | str) -> None:
    with open(file_path, "w") as f:
        serialized = obj.serialize()  # TODO: types
        json.dump(serialized, f, indent=2)


def serialize(obj: object) -> Any:
    if type(obj) in ClassRegistry.class_registry:  # registered classes
        class_name = ClassRegistry.class_registry[type(obj)]
        return {
            class_name: serialize({f.name: getattr(obj, f.name) for f in fields(obj)})
        }
    elif isinstance(obj, list):
        return [serialize(v) for v in obj]
    elif isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    elif isinstance(obj, timedelta):  # time for special types
        return int(obj.total_seconds())
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Enum):
        return obj.value
    assert isinstance(
        obj, (str, int, float, bool, type(None))
    ), f"uknown type of {obj}, {type(obj)}"
    return obj


def deserialize(
    obj: dict | list | str | float | bool | None,
) -> Any:  # TODO: type this
    if isinstance(obj, list):
        return [deserialize(v) for v in obj]
    elif isinstance(obj, dict) and len(obj) != 1:  # ordinary dictionary
        return {k: deserialize(v) for k, v in obj.items()}
    elif isinstance(obj, dict) and len(obj) == 1:  # maybe a class
        key, value = list(obj.items())[0]
        if key in ClassRegistry.name_registry:  # found a dataclass!
            cls = ClassRegistry.name_registry[key]
            return _create_dataclass(cls, value)
        else:  # ordinary dictionary
            return {key: deserialize(value)}
    return obj


def _create_dataclass(cls: Type, obj: dict) -> Any:
    assert is_dataclass(cls), "only dataclasses allowed here"
    assert isinstance(obj, dict)
    self_dict: dict = {}
    for field in fields(cls):
        if field.name not in obj:
            raise ValueError(f"field {field.name} not found in {cls.__name__} json")
        self_dict[field.name] = _deserialize_wrt_to_type(field.type, obj[field.name])
    if len(self_dict) != len(obj):
        raise ValueError(f"too many fields in {obj = }")

    return cls(**self_dict)


def _deserialize_wrt_to_type(type_: Type, value: Any) -> Any:
    if issubclass(type(type_), type):
        # works only for python types, not typing.types
        if issubclass(type_, timedelta):
            value = timedelta(seconds=value)
        elif issubclass(type_, datetime):
            value = datetime.fromisoformat(value)
        elif issubclass(type_, Enum):
            value = type_(value)
    return deserialize(value)

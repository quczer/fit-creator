from dataclasses import asdict, fields, is_dataclass
from datetime import datetime, timedelta
from enum import Enum
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


class JSONSerializableMixin:
    def serialize(self) -> dict:
        return self._serialize(self)

    @staticmethod
    def _serialize(obj: Any) -> Any:
        # print(f"{type(obj) = } {obj = }")
        if type(obj) in ClassRegistry.class_registry:  # registered classes
            class_name = ClassRegistry.class_registry[type(obj)]
            # print(f"creating registred class {class_name = } from {obj = }")
            return {
                class_name: JSONSerializableMixin._serialize(
                    {f.name: getattr(obj, f.name) for f in fields(obj)}
                )
            }
        elif isinstance(obj, list):
            return [JSONSerializableMixin._serialize(v) for v in obj]
        elif isinstance(obj, dict):
            return {k: JSONSerializableMixin._serialize(v) for k, v in obj.items()}
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

    @staticmethod
    def deserialize(
        obj: dict | list | str | float | bool | None,
    ) -> Any:  # TODO: type this
        if isinstance(obj, list):
            return [JSONSerializableMixin.deserialize(v) for v in obj]
        elif isinstance(obj, dict) and len(obj) != 1:  # ordinary dictionary
            return {k: JSONSerializableMixin.deserialize(v) for k, v in obj.items()}
        elif isinstance(obj, dict) and len(obj) == 1:  # maybe a class
            key, value = list(obj.items())[0]
            if key in ClassRegistry.name_registry:  # found a dataclass!
                cls = ClassRegistry.name_registry[key]
                return JSONSerializableMixin._create_dataclass(cls, value)
            else:  # ordinary dictionary
                return {key: JSONSerializableMixin.deserialize(value)}
        return obj

    @staticmethod
    def _create_dataclass(cls: Type, obj: dict) -> Any:
        # print(f"creating dataclass {cls = } from {obj = }")
        assert is_dataclass(cls), "only dataclasses allowed here"
        assert isinstance(obj, dict)
        self_dict: dict = {}
        for field in fields(cls):
            if field.name not in obj:
                raise ValueError(f"field {field.name} not found in {cls.__name__} json")
            self_dict[field.name] = JSONSerializableMixin._deserialize_wrt_to_type(
                field.type, obj[field.name]
            )
        if len(self_dict) != len(obj):
            raise ValueError(f"too many fields in {obj = }")

        # ret = cls(**self_dict)
        # print(ret)
        return cls(**self_dict)

    @staticmethod
    def _deserialize_wrt_to_type(type_: Type, value: Any) -> Any:
        if issubclass(type(type_), type):
            # works only for python types, not typing.types
            if issubclass(type_, timedelta):
                value = timedelta(seconds=value)
            elif issubclass(type_, datetime):
                value = datetime.fromisoformat(value)
            elif issubclass(type_, Enum):
                value = type_(value)
        return JSONSerializableMixin.deserialize(value)

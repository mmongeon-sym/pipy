from .logging import get_logger
import dataclasses
import json
from .assertions import assert_type


class DataClass(object):
    log = get_logger()

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            return None

    def __setitem__(self, key, value):
        if hasattr(self, key):
            return setattr(self, key, value)
        else:
            raise AttributeError(f"{key} is not a valid attribute")

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.__annotations__.keys())

    def __iter__(self):
        return (x for x in self.__annotations__.keys())

    def keys(self):
        return self.__annotations__.keys()

    def items(self):
        return self.as_dict().items

    def values(self):
        return self.as_dict().items

    def as_dict(self):
        return dataclasses.asdict(self)

    def as_tuple(self):
        return dataclasses.astuple(self)

    def as_json(self, indent: int = None):
        return json.dumps(self.as_dict(),
                          indent=indent,
                          ensure_ascii=False
                          )

    @property
    def __fields__(self) -> list:
        return self.__dataclass_fields__.keys()

    @property
    def __init_fields__(self) -> list:
        return [field.name for attr, field in self.__dataclass_fields__.items() if field.init is True]

    @property
    def __post_init_fields__(self) -> list:
        return [field.name for attr, field in self.__dataclass_fields__.items() if field.init is False]

    def __init_typecheck__(self, allow_none: bool = False) -> None:
        for attr, field in self.__dataclass_fields__.items():
            if field.init is True:
                value = assert_type(value=getattr(self, attr),
                                    value_type=field.type,
                                    name=field.name,
                                    allow_none=allow_none
                                    )
                setattr(self, attr, value)
        return None

    def __post_init_typecheck__(self, allow_none: bool = True) -> None:
        for attr, field in self.__dataclass_fields__.items():
            if field.init is False:
                value = assert_type(value=getattr(self, attr),
                                    value_type=field.type,
                                    name=field.name,
                                    allow_none=allow_none
                                    )
                setattr(self, attr, value)
        return None

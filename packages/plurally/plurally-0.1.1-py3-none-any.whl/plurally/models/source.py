from typing import Any

from pydantic import BaseModel

from plurally.models.node import Node


class ConstantSource(Node):
    class InputSchema(BaseModel): ...

    def __init__(self, name: str, value, pos_x: int = 0, pos_y: int = 0) -> None:
        super().__init__(name, pos_x=pos_x, pos_y=pos_y)
        self.outputs["value"] = value

    def __call__(self):
        """No evaluation needed, constant value is already set."""
        ...

    def serialize(self):
        payload = super().serialize()
        payload["value"] = self.outputs["value"]
        return payload

    @classmethod
    def _parse(cls, **kargs):
        return cls(**kargs)


class TextSource(ConstantSource):

    class OutputSchema(BaseModel):
        value: str

    def __init__(self, name: str, value: str, pos_x: int = 0, pos_y: int = 0) -> None:
        super().__init__(name, value, pos_x=pos_x, pos_y=pos_y)
        assert isinstance(value, str)


class IntegerSource(ConstantSource):

    class OutputSchema(BaseModel):
        value: int

    def __init__(self, name: str, value: int, pos_x: int = 0, pos_y: int = 0) -> None:
        super().__init__(name, value, pos_x=pos_x, pos_y=pos_y)
        assert isinstance(value, int)


class FloatSource(ConstantSource):

    class OutputSchema(BaseModel):
        value: float

    def __init__(self, value: float, pos_x: int = 0, pos_y: int = 0) -> None:
        super().__init__(value, pos_x=pos_x, pos_y=pos_y)
        assert isinstance(value, float)


class DataSource:
    def __init__(self) -> None:
        self.i = 0

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.i += 1
        return str(self.i)

import abc
import uuid
from typing import Union, get_args

from pydantic import BaseModel
from pydantic_core import ValidationError


def is_type_compatible(input_type, output_type):
    # If output_type is a Union, extract all possible types
    if hasattr(output_type, "__origin__") and output_type.__origin__ is Union:
        return any(
            issubclass(input_type, allowed_type)
            for allowed_type in get_args(output_type)
        )

    # Otherwise, simply check if input_type is a subclass of output_type
    return issubclass(input_type, output_type)


class Node(abc.ABC):
    InputSchema = None
    OutputSchema = None

    def __init__(self, name: str, pos_x: int = 0, pos_y: int = 0):
        self._node_id = f"nd-{str(uuid.uuid4())}"
        self.name = name
        self.outputs = {}
        self._set_schemas()
        self._check_schemas()

        self.pos_x = pos_x
        self.pos_y = pos_y

    def _check_schemas(self):
        if self.InputSchema is None or not issubclass(self.InputSchema, BaseModel):
            raise ValueError(f"{type(self).__name__} must have an InputSchema")
        if self.OutputSchema is None or not issubclass(self.OutputSchema, BaseModel):
            raise ValueError(f"{type(self).__name__} must have an OutputSchema")

    def _set_schemas(self): ...

    @property
    def node_id(self):
        return self._node_id

    def validate_connection(
        self, src_node: "Node", output_node_id: str, input_node_id: str
    ):
        output_node_schema = src_node.OutputSchema.__annotations__.get(output_node_id)
        input_node_schema = self.InputSchema.__annotations__.get(input_node_id)
        if output_node_schema is None or input_node_schema is None:
            return True
        return is_type_compatible(output_node_schema, input_node_schema)

    def validate_inputs(self, **kwargs):
        try:
            self.InputSchema(**kwargs)
        except ValidationError as e:
            raise ValueError(f"Invalid inputs for {self})") from e

    def __call__(self, **kwargs):
        """Override this method in child classes to define logic."""
        self.validate_inputs(**kwargs)
        self.forward(**kwargs)

    def forward(self, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and other.node_id == self.node_id

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, node_id={self.node_id[:7]})"

    def __hash__(self) -> int:
        return hash(self.node_id)

    @abc.abstractmethod
    def serialize(self):
        return {
            "kls": type(self).__name__,
            "name": self.name,
            "_node_id": self._node_id,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
        }

    @classmethod
    @abc.abstractmethod
    def _parse(cls, **kwargs): ...

    @classmethod
    def parse(cls, **kwargs):
        _node_id = kwargs.pop("_node_id")
        obj = cls._parse(**kwargs)
        obj._node_id = _node_id
        obj.pos_x = kwargs.get("pos_x", 0)
        obj.pos_y = kwargs.get("pos_y", 0)
        return obj

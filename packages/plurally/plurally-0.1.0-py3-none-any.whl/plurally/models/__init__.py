# ruff: noqa: F401
import inspect
from typing import Type

from pydantic import BaseModel, create_model

from .action import AddNode, MultiplyNode
from .flow import Flow
from .source import IntegerSource, TextSource


def generate_schema(cls: Type) -> Type[BaseModel]:
    sig = inspect.signature(cls.__init__)
    fields = {}

    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue

        annotation = param.annotation

        if annotation == inspect._empty:
            raise ValueError(f"Parameter '{param_name}' is missing type annotation.")

        if param.default != inspect.Parameter.empty:
            fields[param_name] = (annotation, param.default)
        else:
            fields[param_name] = (annotation, ...)

    model = create_model(f"{cls.__name__}Schema", **fields)
    return model


NODES = [
    AddNode,
    MultiplyNode,
    IntegerSource,
    TextSource,
]
MAP = {kls.__name__: (kls, generate_schema(kls)) for kls in NODES}


def create_node(**json_payload):
    node_kls = json_payload.pop("kls")
    return MAP[node_kls][0].parse(**json_payload)

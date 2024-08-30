"""
sorry :(
"""
from __future__ import annotations

from onnx import NodeProto, ValueInfoProto


class EggStrings:
    """
    Singleton for recording egg string
    """

    __string_dict: dict[str, str] = dict()
    """
    Map of egg output names to corresponding egg string
    """

    @classmethod
    def get(cls, key: str):
        return cls.__string_dict[key]

    @classmethod
    def put(cls, key: str, value: str):
        cls.__string_dict[key] = value

    @classmethod
    def inputs_satisfied(cls, node: NodeProto):
        return frozenset(node.input).issubset(cls.__string_dict.keys())

    @classmethod
    def join(cls, string_map: dict[str, str]):
        cls.__string_dict = cls.__string_dict | string_map


class PreservedNodes:
    """
    Singleton for recording mapping between constant names and values
    """

    __constant_dict = dict()

    @classmethod
    def get(cls, key: str):
        return cls.__constant_dict[key]

    @classmethod
    def get_nodes(cls):
        return cls.__constant_dict.values()

    @classmethod
    def put(cls, key: str, value: NodeProto):
        cls.__constant_dict[key] = value

    @classmethod
    def join(cls, constant_map: dict[str, str]):
        cls.__string_dict = cls.__constant_dict | constant_map


class PreservedIO:
    """
    Singleton for preserving IO data
    """

    __inputs: list[ValueInfoProto] = list()
    __outputs: list[ValueInfoProto] = list()

    @classmethod
    def add_input(cls, i):
        cls.__inputs.append(i)

    @classmethod
    def add_output(cls, o):
        cls.__outputs.append(o)

    @classmethod
    def get_inputs(cls):
        return cls.__inputs

    @classmethod
    def get_outputs(cls):
        return cls.__outputs

from __future__ import annotations

from onnx import ModelProto, ValueInfoProto, NodeProto
from typing import Dict, Type, List
from abc import ABC, abstractmethod

from .singleton_hell import EggStrings
from .helpers import extract_dimension_from_constant


# region Node serialization strategies
class NodeSerializeStrategy(ABC):
    @staticmethod
    @abstractmethod
    def serialize_node(node: NodeProto) -> Dict[str, str]:
        """
        :return: Map of output names to egg strings
        """
        pass

    @staticmethod
    @abstractmethod
    def check_node_compatibility(node: NodeProto) -> bool:
        """
        :return: Checks if strategy is compatible with provided node
        """
        pass


class ConstantNodeSerializeStrategy(NodeSerializeStrategy):
    @staticmethod
    def serialize_node(node: NodeProto) -> Dict[str, str]:
        # Dimension string
        dimensions_egg_string = extract_dimension_from_constant(node)

        return {output_name: "(input {}@T@{})".format(output_name, dimensions_egg_string) for output_name in
                node.output}

    @staticmethod
    def check_node_compatibility(node: NodeProto) -> bool:
        return node.op_type == "Constant"


class ScalarConstantNodeSerializeStrategy(NodeSerializeStrategy):
    @staticmethod
    def check_node_compatibility(node: NodeProto) -> bool:
        return node.op_type == "Constant" and extract_dimension_from_constant(node) in ["1", ""]

    @staticmethod
    def serialize_node(node: NodeProto) -> Dict[str, str]:
        return {output_name: "(input {})".format(node.attribute[0].t.double_data[0]) for output_name in node.output}


class OperationNodeSerializeStrategy(NodeSerializeStrategy):
    @staticmethod
    def serialize_node(node: NodeProto) -> Dict[str, str]:
        operands = []
        for input_node in node.input:
            operands.append(EggStrings.get(input_node))
        operand_egg_string = " ".join(operands)
        return {output_name: "({} {})".format(node.op_type, operand_egg_string) for output_name in node.output}

    @staticmethod
    def check_node_compatibility(node: NodeProto) -> bool:
        return True
# endregion


# region serializers
class NodeSerializer:
    __strategy_chain: List[Type[NodeSerializeStrategy]] = [
        ScalarConstantNodeSerializeStrategy,
        ConstantNodeSerializeStrategy,
        OperationNodeSerializeStrategy
    ]
    """
    Ordered list of strategies that will be checked for compatibility
    """

    @classmethod
    def serialize_node(cls, node: NodeProto) -> Dict[str, str]:
        """
        :return: Map of output names to egg strings
        """
        for strategy in cls.__strategy_chain:
            if strategy.check_node_compatibility(node):
                return strategy.serialize_node(node)

        assert False  # TODO: replace with actual error message indicating that no strategies were found
# endregion

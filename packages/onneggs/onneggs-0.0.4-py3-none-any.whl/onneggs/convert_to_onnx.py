"""
:(

sorry
"""

import re
from onnx import NodeProto, ModelProto
import onnx.helper as oh
import onnx
import numpy as np

from .singleton_hell import PreservedNodes, PreservedIO

generated_nodes: list[NodeProto] = []
"""
Stores generated nodes. very important.
"""


# region String manipulation
def clean_string(string: str) -> str:
    return ' '.join(string.strip().split())


def find_corresponding_end_parenthesis_index(string: str, open_parenthesis_index: int):
    # First character should be '('
    assert string[0] == '('

    depth = 1
    for i in range(open_parenthesis_index + 1, len(string)):
        if string[i] == '(':
            depth += 1
        elif string[i] == ')':
            depth -= 1
            if depth == 0:
                return i
    assert False


def separate_operand_string(operand_string: str) -> list[str]:
    if len(operand_string) == 0:
        return []

    operand_string = operand_string.strip()
    end_index = find_corresponding_end_parenthesis_index(operand_string, 0)
    return [operand_string[0:end_index + 1]] + separate_operand_string(operand_string[end_index + 1:])


# endregion


# region Regex
# Expression identifiers
scalar_expression_identifier = re.compile(r"^\(input\s(-?\d+(\.?\d+))\)$")
input_expression_identifier = re.compile(r"^\(input\s(\S+)\@[TF]\@\d+(\_\d+)*\)$")
operation_expression_identifier = re.compile(r"^\((\w+)\s(\(.+\))\)$")
noop_expression_identifier = re.compile(r"^\(noop((\s\(.+\))+)\)$")

# endregion


# region Extraction functions
# Operation expression
def extract_operator(operation_exp: str) -> str:
    return operation_expression_identifier.fullmatch(operation_exp).group(1)


def extract_operands_string(operation_exp: str) -> str:
    return operation_expression_identifier.fullmatch(operation_exp).group(2)


def extract_outputs_string(noop_exp: str) -> str:
    return noop_expression_identifier.fullmatch(noop_exp).group(1)


# Input expression
def extract_input_name(input_exp: str) -> str:
    return input_expression_identifier.fullmatch(input_exp).group(1)


def extract_scalar(scalar_exp: str) -> float:
    return float(scalar_expression_identifier.fullmatch(scalar_exp).group(1))

# endregion


def generate_tree(egg_string: str,
                  is_output_layer: bool = False,
                  output_name_list: list[str] = None) -> list[str]:
    global generated_nodes  # TODO bad

    # Case 0: noop wrapper
    if noop_expression_identifier.fullmatch(egg_string):
        # Recurse with is_output_layer set to true, with correct output given
        outputs_string = extract_outputs_string(egg_string)
        outputs_list = separate_operand_string(outputs_string)
        for i in range(len(outputs_list)):
            generate_tree(outputs_list[i], True, [output_name_list[i]])
        return output_name_list

    # Case 1: Operation expression
    elif operation_expression_identifier.fullmatch(egg_string):
        operation_type = extract_operator(egg_string)
        operands_string = extract_operands_string(egg_string)
        operands_list = separate_operand_string(operands_string)
        operand_ids = []
        for operand_string in operands_list:
            operand_ids += generate_tree(operand_string)

        current_id = output_name_list if is_output_layer else ["out" + str(len(generated_nodes))]

        if operation_type == "Mod":
            generated_nodes += [oh.make_node(
                op_type=operation_type,
                inputs=operand_ids,
                outputs=current_id,
                name=current_id[0] + "_node",
                fmod=1
            )]
        else:
            generated_nodes += [oh.make_node(
                op_type=operation_type,
                inputs=operand_ids,
                outputs=current_id,
                name=current_id[0] + "_node"
            )]
        return current_id

    # Case 2: scalar expression
    elif scalar_expression_identifier.fullmatch(egg_string):
        scalar = extract_scalar(egg_string)
        current_id = output_name_list if is_output_layer else ["out" + str(len(generated_nodes))]
        generated_nodes += [
            oh.make_node(
                op_type="Constant",
                inputs=[],
                outputs=current_id,
                name=current_id[0] + "_node",
                value=oh.make_tensor(
                    name=current_id[0] + "_value",
                    data_type=onnx.TensorProto.DOUBLE,
                    dims=[1],
                    vals=np.asarray([scalar])
                )
            )
        ]
        return current_id

    # Case 3: input expression
    elif input_expression_identifier.fullmatch(egg_string):
        input_id = extract_input_name(egg_string)
        return [input_id]


# region Onnx generation
def egg2onnx(egg_string: str) -> ModelProto:
    clean_egg = clean_string(egg_string)
    output_names = [output.name for output in PreservedIO.get_outputs()]
    generate_tree(clean_egg, True, output_names)
    # combine new and old nodes
    generated_graph = oh.make_graph(
        list(PreservedNodes.get_nodes()) + generated_nodes,
        name="Generated",
        inputs=PreservedIO.get_inputs(),
        outputs=PreservedIO.get_outputs()
    )
    generated_model = oh.make_model(generated_graph)
    onnx.checker.check_model(generated_model)
    return generated_model
# endregion



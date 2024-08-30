from io import BufferedReader
from onnx import ModelProto, ValueInfoProto

from .singleton_hell import EggStrings, PreservedNodes, PreservedIO
from .egg_conversion_strategies import NodeSerializer
from .helpers import *


def onnx2egg(file_reader: BufferedReader) -> str:
    # Load model from binary
    mp = ModelProto()
    mp.ParseFromString(file_reader.read())

    # Preserve constant and io nodes
    node_preservation(mp)

    # Serialize each of the onnx nodes
    serialize_nodes(mp)

    # Stitch multiple outputs into one egg string
    stitched_string = stitch_egg_string_outputs()
    return stitched_string


def node_preservation(mp: ModelProto):
    # Constant node preservation
    nodes = [node for node in mp.graph.node]
    for node in nodes:
        if node.op_type == "Constant":
            for out in node.output:
                PreservedNodes.put(out, node)

    # Input preservation
    for io in mp.graph.input:
        PreservedIO.add_input(io)

    # Output preservation
    for io in mp.graph.output:
        PreservedIO.add_output(io)


def serialize_nodes(mp: ModelProto):
    nodes = [node for node in mp.graph.node]
    # Input serialization
    for input_info in mp.graph.input:
        EggStrings.put(input_info.name, input_to_egg_string(input_info))

    while len(nodes) > 0:
        for node in nodes:
            # Need to ensure that the node is actually serializable
            if EggStrings.inputs_satisfied(node):
                EggStrings.join(NodeSerializer.serialize_node(node))
                nodes.remove(node)


def input_to_egg_string(input_proto: ValueInfoProto) -> str:
    # Dimension string
    dimensions_egg_string = extract_dimension_from_input(input_proto)

    return "(input {}@F@{})".format(input_proto.name, dimensions_egg_string)


def stitch_egg_string_outputs() -> str:
    # Retrieve corresponding
    output_names = [output.name for output in PreservedIO.get_outputs()]
    output_strings = [EggStrings.get(output_name) for output_name in output_names]
    noop_argument_string = " ".join(output_strings)
    return "(noop {})".format(noop_argument_string)
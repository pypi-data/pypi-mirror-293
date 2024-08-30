import onnx.helper as helper


def extract_dimension_from_input(input_proto: helper.ValueInfoProto):
    dimensions = []
    for n in input_proto.type.tensor_type.shape.dim:
        dimensions.append(str(n.dim_value))
    return "_".join(dimensions)


def extract_dimension_from_constant(node: helper.NodeProto):
    dimensions = []
    for attribute in node.attribute:
        for dim in attribute.t.dims:
            dimensions.append(str(dim))
    return "_".join(dimensions)

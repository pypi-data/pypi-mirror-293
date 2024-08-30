from onnx import helper as h
import onnx
import onnx.checker as checker
import numpy as np

rgb2xyz = np.array([
    [0.4124564323, 0.3575760763, 0.1804374803],
    [0.2126728463, 0.7151521672, 0.07217499957],
    [0.0193339041, 0.1191920282, 0.9503040737]
])

xyz2lms = np.array([
    [0.15514, 0.54312, -0.03286],
    [-0.15514, 0.45684, 0.03286],
    [0, 0, 0.01608]
])


node_list = [
    # RGB2XYZ transformation matrix constant
    h.make_node(
        op_type="Constant",
        inputs=[],
        outputs=["RGB2XYZ"],
        value=h.make_tensor(
            name="RGB2XYZ_value",
            data_type=onnx.TensorProto.FLOAT,
            dims=rgb2xyz.shape,
            vals=rgb2xyz.flatten()
        )
    ),
    # XYZ2LMS transformation matrix constant
    h.make_node(
        op_type="Constant",
        inputs=[],
        outputs=["XYZ2LMS"],
        value=h.make_tensor(
            name="XYZ2LMS_value",
            data_type=onnx.TensorProto.FLOAT,
            dims=xyz2lms.shape,
            vals=xyz2lms.flatten()
        )
    ),
    # Mushed together first
    h.make_node(
        op_type="MatMul",
        inputs=["XYZ2LMS", "RGB2XYZ"],
        outputs=["intermediate"],
        name="fold_this"
    ),
    # Apply
    h.make_node(
        op_type="MatMul",
        inputs=["intermediate", "Input"],
        outputs=["Output"],
        name="dont_fold"
    )
]

input_image = h.make_tensor_value_info(
    name="Input",
    elem_type=onnx.TensorProto.FLOAT,
    shape=(3, 100),
)

output_image = h.make_tensor_value_info(
    name="Output",
    elem_type=onnx.TensorProto.FLOAT,
    shape=(3, 100),
)

graph = h.make_graph(
    nodes=node_list,
    name="RGB2LMS",
    inputs=[input_image],
    outputs=[output_image]
)

model = h.make_model(
    graph=graph
)

checker.check_model(model)

onnx.save(model, "folding_test.onnx")

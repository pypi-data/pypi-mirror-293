import onnx


m = onnx.shape_inference.infer_shapes(
    onnx.load_model("chromatic_adaptation.onnx")
)

onnx.save_model(m, "chromatic_adaptation_filled.onnx")

import onnxruntime as ort


def fold_onnx(output_file: str):
    so = ort.SessionOptions()
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_EXTENDED
    so.optimized_model_filepath = output_file
    ort.InferenceSession(
        output_file,
        so,
        providers=["CPUExecutionProvider"]
    )

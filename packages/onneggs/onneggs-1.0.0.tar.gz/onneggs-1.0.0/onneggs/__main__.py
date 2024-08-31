import click
import eggwrap

from onnx import save

from .convert_to_egg import onnx2egg
from .convert_to_onnx import egg2onnx
from .folder import fold_onnx


@click.command()
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.STRING)
def optimize(input, output):
    # Convert to egg language
    print("Converting to egg")
    egg_string = onnx2egg(input)

    # Optimize with egg
    print("Performing equality saturation")
    egg_output = eggwrap.lp_optimize(egg_string, 1000)

    # Convert back to onnx
    print("Converting back to onnx")
    optimized_model = egg2onnx(egg_output)
    save(optimized_model, output)

    # Constant folding
    print("Final optimizations")
    fold_onnx(output)


if __name__ == '__main__':
    optimize()

# onneggs

onneggs is an optimizer designed to optimize CoolerSpace ONNX files.
The repository for CoolerSpace can be found [here](https://github.com/horizon-research/CoolerSpace).

## Installation

### Dependencies
onneggs requires [eggwrap](https://github.com/horizon-research/eggwrap) to be installed.
This dependency is handled automatically if using PyPI.
Additionally [Cbc](https://github.com/coin-or/Cbc) is also required.

### PyPI
onneggs is on PyPI! 
Install onneggs with the following command:

```
pip install onneggs
```

Please note that we only support Linux distributions for this package, and only for python versions 3.10+.

### Building from source on Linux
In order to build onneggs, [eggwrap](https://github.com/horizon-research/eggwrap) must first be built.
Use the following commands to build onneggs from source:

```
git clone https://github.com/horizon-research/onneggs
cd onneggs
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install build
python3 -m build
```

## Usage
onneggs can be invoked as a Python module:

```
python3 -m onneggs [INPUT_FILE] [OUTPUT_FILE]
```

Where [INPUT_FILE] is the path to the input ONNX file, and [OUTPUT_FILE] is the desired output path.

# COLMAP model_concatener
Concatenate COLMAP models without common registered images for whatever purpose.

## Installation
This script requires nothing but Python and built-in modules since it only
reads and writes files.

## Usage
Only models in .TXT format are supported. One can convert COLMAP models with the command line:
```bash
colmap model_converter --input_path path/to/model --output_path path/to/output --output_type TXT
```

To concatenate the models, simply run:
```bash
python colmap_model_concatener.py --input_path1 path/to/first/model --input_path2 path/to/second/model --output_path path/to/output/model
```

One can also replace a model's 3D points colors by specifying the model's new RGB color
with argument `--RGB1` (for first model) or `--RGB2` (for second model). This can prove
useful when debugging.

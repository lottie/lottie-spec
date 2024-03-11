#!/usr/bin/env python3
import os
import json
import pathlib
import argparse

# Ignored subschemas
# With how inheritance is acheived in json schema with allOf, we can't have 
# strict schemas be extended, as the additional fields of the child would cause
# the parent schema to fail validation.
ignored_subschemas = [
    'visual-object',
    'asset',
    'composition',
    'visual-layer',
    'layer',
    'vector-keyframe',
    'base-keyframe',
    'shape',
    'graphic-element',
    'modifier',
    'transform',
    'shape-style'
]

def strictify_fields(
    json_data: dict,
):
    for module, module_data in json_data['$defs'].items():
        for attr, attr_data in module_data.items():
            if 'type' in attr_data and attr_data['type'] == 'object' and attr not in ignored_subschemas:
                attr_data['unevaluatedProperties'] = False

    return json_data

root = pathlib.Path(__file__).absolute().parent.parent

parser = argparse.ArgumentParser(
    description="Joins JSON schema in a single file")
parser.add_argument(
    "--input", "-i",
    type=pathlib.Path,
    default=root / "docs" / "lottie.schema.json",
    help="Input file name"
)

parser.add_argument(
    "--output", "-o",
    type=pathlib.Path,
    default=root / "docs" / "lottie-strict.schema.json",
    help="Output file name"
)

args = parser.parse_args()
input_path: pathlib.Path = args.input
output_path: pathlib.Path = args.output

with open(input_path) as file:
    json_data = json.load(file)

strictify_fields(json_data)

os.makedirs(output_path.parent, exist_ok=True)

with open(output_path, "w") as file:
    json.dump(json_data, file, indent=4)

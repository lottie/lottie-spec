#!/usr/bin/env python3
import os
import json
import pathlib
import argparse

from schema_tools.schema import SchemaPath, Schema
from schema_tools import type_info

def join_parts(
    json_data: dict,
    path: pathlib.Path,
    exclude: pathlib.Path
):
    defs = {}
    for subdir in sorted(path.iterdir()):
        dir_schema = {}
        if subdir.is_dir():
            for file_item in subdir.iterdir():
                if file_item.is_file() and file_item.suffix == ".json" and file_item != exclude:
                    with open(file_item, "r") as file:
                        try:
                            file_schema = json.load(file)
                        except Exception:
                            print(file_item)
                            raise
                    file_schema.pop("$schema", None)
                    dir_schema[file_item.stem] = file_schema
            defs[subdir.name] = dir_schema

    json_data["$defs"] = defs

    return json_data

def add_vals_to_unknown_object(
    objects,
    unknown_type_dict: dict
):
    types = []

    for ele in objects.concrete:
        type = ele.properties['ty'].const
        if type is not None:
            types.append(type)
    
    unknown_type_dict["properties"]["ty"]["not"]["enum"] = types
    
root = pathlib.Path(__file__).absolute().parent.parent

parser = argparse.ArgumentParser(description="Joins JSON schema in a single file")
parser.add_argument(
    "--input", "-i",
    type=pathlib.Path,
    default=root / "schema",
    help="Path to the input schema files"
)
parser.add_argument(
    "--root", "-r",
    type=pathlib.Path,
    default="root.json",
    help="Root schema file"
)
parser.add_argument(
    "--output", "-o",
    type=pathlib.Path,
    default=root / "docs" / "lottie.schema.json",
    help="Output file name"
)

args = parser.parse_args()
input_dir: pathlib.Path = args.input.resolve()
output_path: pathlib.Path = args.output
root_path: pathlib.Path = (input_dir / args.root).resolve()

with open(root_path) as file:
    json_data = json.load(file)

join_parts(json_data, input_dir, root_path)

schema = Schema(json_data)
ts = type_info.TypeSystem(schema)

add_vals_to_unknown_object(
    ts.from_path(SchemaPath("#/$defs/layers/all-layers")),
    json_data["$defs"]["layers"]["unknown-layer"]
)
add_vals_to_unknown_object(
    ts.from_path(SchemaPath("#/$defs/shapes/all-graphic-elements")),
    json_data["$defs"]["shapes"]["unknown-shape"]
)

os.makedirs(output_path.parent, exist_ok=True)

with open(output_path, "w") as file:
    json.dump(json_data, file, indent=4)

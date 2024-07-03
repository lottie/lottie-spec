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

def add_unknown_object(
    json_data: dict,
    path_parts
):
    objects = ts.from_path(SchemaPath("#/$defs/" + "/".join(path_parts)))

    types = []

    for ele in objects.concrete:
        types.append(ele.properties['ty'].const)
    
    unknown_object = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "title": "Unknown types",
        "description": "Unknown types. Types not defined by the specification are still allowed.",
        "not": {
            "properties": {
                "ty": {
                    "$comment": "enum list is dynamically generated",
                    "enum": types
                }
            }
        }
    }
    
    json_data["$defs"][path_parts[0]][path_parts[1]]["oneOf"].append(unknown_object)
    
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

# add_unknown_object(json_data, ["layers", "all-layers"])
# add_unknown_object(json_data, ["shapes", "all-graphic-elements"])

os.makedirs(output_path.parent, exist_ok=True)

with open(output_path, "w") as file:
    json.dump(json_data, file, indent=4)

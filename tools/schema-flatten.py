#!/usr/bin/env python3
import os
import json
import pathlib
import argparse
import re

def_seperator = "__"

def replace_refs(
    json_data: dict
):
    if isinstance (json_data, list):
        for item in json_data:
            replace_refs(item)
        return json_data
        
    if not isinstance(json_data, dict):
        return json_data
    
    if "$ref" in json_data:
        json_data["$ref"] = re.sub(r"\$defs/(.*)/(.*)",  fr"$defs/\1{def_seperator}\2", json_data["$ref"])

    for key in json_data:
        replace_refs(json_data[key])

    return json_data

def flatten_defs(
    json_data: dict
):
    flat_defs = {}
    for group in json_data["$defs"]:
        for item in json_data["$defs"][group]:
            flat_defs[f"{group}{def_seperator}{item}"] = json_data["$defs"][group][item]

    json_data["$defs"] = flat_defs
    return json_data

root = pathlib.Path(__file__).absolute().parent.parent

parser = argparse.ArgumentParser(description="Flattens JSON schema refs")
parser.add_argument(
    "--input", "-i",
    type=pathlib.Path,
    default=root / "docs" / "lottie.schema.json",
    help="Path to the input schema file"
)
parser.add_argument(
    "--output", "-o",
    type=pathlib.Path,
    default=root / "docs" / "lottie-flat.schema.json",
    help="Output file name"
)

args = parser.parse_args()
input_schema: pathlib.Path = args.input.resolve()
output_path: pathlib.Path = args.output

with open(input_schema) as file:
    json_data = json.load(file)

flatten_defs(json_data)
replace_refs(json_data)

os.makedirs(output_path.parent, exist_ok=True)

with open(output_path, "w") as file:
    json.dump(json_data, file, indent=4)

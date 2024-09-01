import json
import random
from typing import Any
import exrex


def _gen_number(minimum: int, maximum: int, multiple_of: int = 1) -> int:
    if abs(multiple_of) > 1:
        minimum += multiple_of - minimum % multiple_of

    return random.randrange(minimum, maximum + 1, multiple_of)


def _gen_str(pattern: str | None = None, min_length: int = 0, max_length: int = 10) -> str:
    if pattern is None:
        pattern = f"[a-zA-Z0-9]{{{min_length},{max_length}}}"
    return exrex.getone(pattern)


def _gen_array(
    min_items: int = 1,
    max_items: int = 10,
    items: dict | bool = False,
    prefix_items: list | None = None,
) -> list:
    # TODO implement support for unique items
    max_length = random.randint(min_items, max_items)
    array = list()
    print(items)
    if prefix_items is not None:
        for item in prefix_items:
            array.append(gen_from_schema(item))

    if items:
        while len(array) < max_length:
            array.append(gen_from_schema(items))

    return list(array)


def _gen_obj(schema: dict[str, Any]) -> dict:
    json_obj = dict()
    for key, value in schema["properties"].items():
        json_obj[key] = gen_from_schema(value)

    return json_obj


def gen_from_schema(schema) -> dict[str, Any] | int | str | list[Any]:
    """
    Generates a JSON object based on the given schema.

    Values are generated for all properties having const, enum
    or any of the following types defined:
    Number
        - minimum     - default 0
        - maximum     - default 100
        - multiple_of - default 1
    String
        - pattern    - default [a-zA-Z0-9]
        - min_length - default 1 (will be ignored if pattern is set)
        - max_length - default 10 (will be ignored if pattern is set)
    """
    obj_const = schema.get("const")
    obj_enum = schema.get("enum")

    if obj_const is not None:
        return obj_const

    if obj_enum is not None:
        return random.choice(obj_enum)

    match schema["type"]:
        case "number" | "integer":
            return _gen_number(
                minimum=schema.get("minimum", 0),
                maximum=schema.get("maximum", 100),
                multiple_of=schema.get("multiple_of", 1),
            )
        case "string":
            return _gen_str(
                pattern=schema.get("pattern"),
                min_length=schema.get("minLength", 1),
                max_length=schema.get("maxLength", 10),
            )
        case "object":
            return _gen_obj(schema)
        case "array":
            return _gen_array(
                min_items=schema.get("minItems", 1),
                max_items=schema.get("maxItems", 10),
                items=schema.get("items", False),
                prefix_items=schema.get("prefixItems"),
            )
        case _:
            raise ValueError(f"Given schema is not supported:\n{schema}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="djg - create random JSON objects based on a given schema."
    )
    parser.add_argument(
        "-s",
        "--schema",
        help="JSON Schema location",
        required=True,
        metavar="SCHEMA_FILE",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="JSON output location - default is stdout",
        metavar="FILE",
    )

    args = parser.parse_args()

    def load_json(path: str):
        with open(path) as f:
            return json.load(f)

    def write_json(path: str, json_object):
        with open(path, "w") as f:
            f.write(json.dumps(json_object, indent=2))

    schema = load_json(args.schema)
    json_object = gen_from_schema(schema)

    if args.output is not None:
        write_json(args.output, json_object)
    else:
        print(json.dumps(json_object, indent=2))

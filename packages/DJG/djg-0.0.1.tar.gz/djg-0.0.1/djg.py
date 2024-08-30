import json
import random
import exrex


def _gen_number(minimum: int, maximum: int, multiple_of: int = 1) -> int:
    if abs(multiple_of) > 1:
        minimum += multiple_of - minimum % multiple_of

    return random.randrange(minimum, maximum + 1, multiple_of)


def _gen_str(pattern: str | None, min_length: int, max_length: int):
    if pattern is None:
        pattern = f"[a-zA-Z0-9]{{{min_length},{max_length}}}"
    return exrex.getone(pattern)


def generate(schema):
    """
    Generates a JSON object based on the given schema.

    The different types are generated in the following way:
    Number
        - minimum     - default 0
        - maximum     - default 100
        - multiple_of - default 1
    String
        - pattern
        - min_length - default 1 (will be ignored if pattern is set)
        - max_length - default 10 (will be ignored if pattern is set)
    """
    res = dict()
    for key, value in schema["properties"].items():
        obj_type = value["type"]
        match obj_type:
            case "number" | "integer":
                res[key] = _gen_number(
                    minimum=value.get("minimum", 0),
                    maximum=value.get("maximum", 100),
                    multiple_of=value.get("multiple_of", 1),
                )
            case "string":
                res[key] = _gen_str(
                    pattern=value.get("pattern"),
                    min_length=value.get("min_length", 1),
                    max_length=value.get("min_length", 10),
                )
            case "object":
                res[key] = generate(value)

    return res


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="djg - create random JSON objects based on a given schema."
    )
    parser.add_argument(
        "-s", "--schema", help="JSON Schema loaction", required=True, metavar="SCHEMA_FILE"
    )
    parser.add_argument(
        "-o", "--output", help="JSON output location - default is stdout", metavar="FILE"
    )

    args = parser.parse_args()

    def load_json(path: str):
        with open(path) as f:
            return json.load(f)

    def write_json(path: str, json_object):
        with open(path, "w") as f:
            f.write(json.dumps(json_object, indent=2))

    schema = load_json(args.schema)
    json_object = generate(schema)

    if args.output is not None:
        write_json(args.output, json_object)
    else:
        print(json.dumps(json_object, indent=2))

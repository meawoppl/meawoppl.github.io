#!/usr/bin/env python3
"""Validate the art-ideas data file against its schema.

Data is served from public/art-ideas/data/; the schema lives alongside this script.
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema package required. Install with: pip install jsonschema")
    sys.exit(1)

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
DATA_PATH = REPO_ROOT / "public" / "art-ideas" / "data" / "ideas.json"
SCHEMA_PATH = HERE / "schema" / "ideas.schema.json"


def validate_schema() -> list[str]:
    errors = []

    if not DATA_PATH.exists():
        return [f"{DATA_PATH.name}: file not found"]
    if not SCHEMA_PATH.exists():
        return [f"{SCHEMA_PATH.name}: schema not found"]

    try:
        data = json.loads(DATA_PATH.read_text())
    except json.JSONDecodeError as e:
        return [f"{DATA_PATH.name}: invalid JSON: {e}"]

    try:
        schema = json.loads(SCHEMA_PATH.read_text())
    except json.JSONDecodeError as e:
        return [f"{SCHEMA_PATH.name}: invalid schema JSON: {e}"]

    validator = jsonschema.Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.absolute_path)
        location = f" at {path}" if path else ""
        errors.append(f"{DATA_PATH.name}{location}: {error.message}")

    return errors


def check_duplicate_titles() -> list[str]:
    errors = []
    try:
        data = json.loads(DATA_PATH.read_text())
    except (json.JSONDecodeError, FileNotFoundError):
        return errors

    seen: dict[str, int] = {}
    for i, item in enumerate(data):
        title = item.get("title", "").strip().lower()
        if title in seen:
            errors.append(
                f"ideas.json[{i}]: duplicate title \"{item['title']}\" "
                f"(first seen at index {seen[title]})"
            )
        else:
            seen[title] = i

    return errors


def main() -> int:
    all_errors = []

    print("Validating ideas.json... ", end="")
    errors = validate_schema()
    if errors:
        print("FAIL")
        all_errors.extend(errors)
    else:
        print("OK")

    print("Checking for duplicate titles... ", end="")
    dup_errors = check_duplicate_titles()
    if dup_errors:
        print("FAIL")
        all_errors.extend(dup_errors)
    else:
        print("OK")

    if all_errors:
        print(f"\n{len(all_errors)} error(s):")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print("\nAll valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate the media-list data files against their schemas.

Data is served from public/media-list/data/; schemas live alongside this script.
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
DATA_DIR = REPO_ROOT / "public" / "media-list" / "data"
SCHEMA_DIR = HERE / "schema"

FILES = {
    "media.json": "media.schema.json",
    "recommenders.json": "recommenders.schema.json",
}


def validate_file(data_name: str, schema_name: str) -> list[str]:
    data_path = DATA_DIR / data_name
    schema_path = SCHEMA_DIR / schema_name
    errors = []

    if not data_path.exists():
        errors.append(f"{data_name}: file not found")
        return errors

    if not schema_path.exists():
        errors.append(f"{schema_name}: schema not found")
        return errors

    try:
        data = json.loads(data_path.read_text())
    except json.JSONDecodeError as e:
        errors.append(f"{data_name}: invalid JSON: {e}")
        return errors

    try:
        schema = json.loads(schema_path.read_text())
    except json.JSONDecodeError as e:
        errors.append(f"{schema_name}: invalid schema JSON: {e}")
        return errors

    validator = jsonschema.Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.absolute_path)
        location = f" at {path}" if path else ""
        errors.append(f"{data_name}{location}: {error.message}")

    return errors


def cross_validate_recommenders(media_path: Path, recommenders_path: Path) -> list[str]:
    """Check that every recommended_by value in media.json matches a recommender initial."""
    errors = []
    try:
        media = json.loads(media_path.read_text())
        recommenders = json.loads(recommenders_path.read_text())
    except (json.JSONDecodeError, FileNotFoundError):
        return errors

    valid_initials = {r["initial"] for r in recommenders if "initial" in r}

    for i, item in enumerate(media):
        recs = item.get("recommended_by", [])
        for rec in recs:
            if rec.startswith("Rando(") and rec.endswith(")"):
                continue
            if rec not in valid_initials:
                errors.append(
                    f"media.json[{i}]: recommended_by \"{rec}\" "
                    f"not found in recommenders.json"
                )

    return errors


def check_duplicate_titles(media_path: Path) -> list[str]:
    """Check for duplicate titles in media.json."""
    errors = []
    try:
        media = json.loads(media_path.read_text())
    except (json.JSONDecodeError, FileNotFoundError):
        return errors

    seen: dict[str, int] = {}
    for i, item in enumerate(media):
        title = item.get("title", "").lower()
        if title in seen:
            errors.append(
                f"media.json[{i}]: duplicate title \"{item['title']}\" "
                f"(first seen at index {seen[title]})"
            )
        else:
            seen[title] = i

    return errors


def main() -> int:
    all_errors = []

    for data_name, schema_name in FILES.items():
        print(f"Validating {data_name}... ", end="")
        errors = validate_file(data_name, schema_name)
        if errors:
            print("FAIL")
            all_errors.extend(errors)
        else:
            print("OK")

    print("Cross-validating recommenders... ", end="")
    xv_errors = cross_validate_recommenders(
        DATA_DIR / "media.json", DATA_DIR / "recommenders.json"
    )
    if xv_errors:
        print("FAIL")
        all_errors.extend(xv_errors)
    else:
        print("OK")

    print("Checking for duplicate titles... ", end="")
    dup_errors = check_duplicate_titles(DATA_DIR / "media.json")
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

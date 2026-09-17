from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import FormatChecker
from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "packages" / "contracts" / "json-schema"
EXAMPLE_DIR = ROOT / "packages" / "contracts" / "examples"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def build_validators() -> dict[str, object]:
    validators: dict[str, object] = {}
    for schema_path in sorted(SCHEMA_DIR.glob("*.json")):
        schema = load_json(schema_path)
        validator_class = validator_for(schema)
        validator_class.check_schema(schema)
        validators[schema_path.name] = validator_class(
            schema, format_checker=FormatChecker()
        )
    return validators


def validate_examples(validators: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for example_path in sorted(EXAMPLE_DIR.glob("*.valid.json")):
        schema_name = example_path.name.removesuffix(".valid.json") + ".json"
        validator = validators.get(schema_name)
        if validator is None:
            errors.append(
                f"Ejemplo sin esquema correspondiente: {example_path.relative_to(ROOT)}"
            )
            continue
        example = load_json(example_path)
        validation_errors = sorted(validator.iter_errors(example), key=lambda error: list(error.path))
        for error in validation_errors:
            location = ".".join(str(part) for part in error.path) or "$"
            errors.append(
                f"Ejemplo inválido: {example_path.relative_to(ROOT)} ({location}): {error.message}"
            )
    return errors


def main() -> int:
    try:
        validators = build_validators()
        errors = validate_examples(validators)
    except (OSError, json.JSONDecodeError, ImportError, SchemaError) as exc:
        print("CONTRACT_VALIDATION_FAILED")
        print(f"- {exc}")
        return 1

    if errors:
        print("CONTRACT_VALIDATION_FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"CONTRACT_VALIDATION_OK schemas={len(validators)} "
        f"examples={len(list(EXAMPLE_DIR.glob('*.valid.json')))}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

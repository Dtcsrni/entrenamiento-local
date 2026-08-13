from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ID_PATTERN = re.compile(
    r"\b(?:NEED|SYS|FUN-[A-Z]+|NFR-[A-Z]+|TST-[A-Z]+|ADR|RISK|SPIKE)-\d{3}\b"
)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
DEFINITION_PATTERN = re.compile(
    r"^\s*(?:[-*]\s+)?(?:\*\*)?"
    r"((?:NEED|SYS|FUN-[A-Z]+|NFR-[A-Z]+|TST-[A-Z]+|ADR|RISK|SPIKE)-\d{3})"
)
HEADING_DEFINITION_PATTERN = re.compile(
    r"^\s*#+\s+((?:ADR)-\d{3})\b"
)
TABLE_DEFINITION_PATTERN = re.compile(
    r"^\s*\|\s*((?:RISK|SPIKE)-\d{3})\s*\|"
)


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts
    )


def validate_json(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.json")):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"JSON inválido: {path.relative_to(ROOT)}: {exc}")


def validate_markdown_links(errors: list[str]) -> None:
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean_target = target.split("#", 1)[0]
            if not clean_target:
                continue
            resolved = (path.parent / clean_target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(
                    f"Enlace fuera del repositorio: {path.relative_to(ROOT)} -> {target}"
                )
                continue
            if not resolved.exists():
                errors.append(
                    f"Enlace local roto: {path.relative_to(ROOT)} -> {target}"
                )


def validate_identifiers(errors: list[str]) -> None:
    definitions: dict[str, list[str]] = defaultdict(list)
    references: dict[str, list[str]] = defaultdict(list)

    for path in markdown_files():
        relative = path.relative_to(ROOT)
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for identifier in ID_PATTERN.findall(line):
                references[identifier].append(f"{relative}:{line_number}")
            definition = DEFINITION_PATTERN.match(line)
            if definition:
                definitions[definition.group(1)].append(f"{relative}:{line_number}")
            heading_definition = HEADING_DEFINITION_PATTERN.match(line)
            if heading_definition and path.name.startswith(heading_definition.group(1)):
                definitions[heading_definition.group(1)].append(
                    f"{relative}:{line_number}"
                )
            table_definition = TABLE_DEFINITION_PATTERN.match(line)
            if table_definition and path.name in {"RISK_REGISTER.md", "DEVELOPMENT_PLAN.md"}:
                definitions[table_definition.group(1)].append(
                    f"{relative}:{line_number}"
                )

    for identifier, locations in sorted(definitions.items()):
        if len(locations) > 1:
            errors.append(f"ID definido varias veces: {identifier}: {', '.join(locations)}")

    allowed_reference_only = {"NEED", "SYS"}
    for identifier, locations in sorted(references.items()):
        prefix = identifier.split("-", 1)[0]
        if identifier not in definitions and prefix not in allowed_reference_only:
            errors.append(
                f"ID referenciado sin definición: {identifier}: {', '.join(locations)}"
            )


def validate_sensitive_names(errors: list[str]) -> None:
    forbidden_parts = {"personal-data", "captures", "photos", "private", "backups", "models"}
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        relative_parts = set(path.relative_to(ROOT).parts)
        if relative_parts & forbidden_parts:
            errors.append(f"Archivo sensible o pesado versionable: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    validate_json(errors)
    validate_markdown_links(errors)
    validate_identifiers(errors)
    validate_sensitive_names(errors)

    if errors:
        print("VALIDATION_FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALIDATION_OK markdown={len(markdown_files())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

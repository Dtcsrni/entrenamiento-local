from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = ROOT / "data" / "rutinas_autocontenidas" / "canonicas"
LOCAL_REFERENCE = re.compile(r"(?:\.\./|\.\\|/|[A-Za-z]:[\\/])")
MEDIA_SUFFIXES = {".gif", ".jpg", ".jpeg", ".png", ".webp"}
SCRIPT_MEDIA = re.compile(
    r"(?:src|staticSrc|static-src|fallback|gif|thumbnail|path|portrait)\s*:\s*[\"']([^\"']+\.(?:gif|jpg|jpeg|png|webp)(?:\?[^\"']*)?)[\"']",
    flags=re.I,
)
DAY1_MEDIA_KEYS = (
    "JALÓN AL PECHO",
    "REMO ALTO UNILATERAL",
    "REMO HORIZONTAL EN MÁQUINA",
    "APERTURA INVERSA EN MÁQUINA",
    "CURL DE BÍCEPS EN MÁQUINA",
    "CURL DE BÍCEPS SENTADO EN MÁQUINA",
)
DAY1_MEDIA_ENTRY = re.compile(
    r"gif\s*:\s*[\"']([^\"']+)[\"']\s*,\s*"
    r"thumbnail\s*:\s*[\"']([^\"']+)[\"']\s*,\s*"
    r"key\s*:\s*[\"']([^\"']+)[\"']",
    flags=re.I | re.S,
)


@dataclass
class ImageReference:
    path: str
    alt: str
    aria_hidden: str
    line: int


class MediaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: list[ImageReference] = []
        self.attribute_references: list[str] = []
        self.depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.depth += 1
        if tag.lower() != "img":
            return
        attr_map = dict(attrs)
        for name, value in attrs:
            if name.casefold() in {"src", "data-static-src", "data-fallback", "poster"} and value:
                self.attribute_references.append(value)
        src = attr_map.get("src") or ""
        if not src:
            return
        self.images.append(
            ImageReference(
                path=src,
                alt=attr_map.get("alt") or "",
                aria_hidden=attr_map.get("aria-hidden") or "",
                line=self.getpos()[0],
            )
        )

    def handle_endtag(self, tag: str) -> None:
        self.depth = max(0, self.depth - 1)


def local_references(text: str, parser: MediaParser) -> list[str]:
    references = [image.path for image in parser.images]
    references.extend(parser.attribute_references)
    references.extend(
        match.group(1)
        for match in SCRIPT_MEDIA.finditer(text)
        if LOCAL_REFERENCE.search(match.group(1))
    )
    return sorted(set(references))


def resolve_local(path: Path, reference: str) -> tuple[Path | None, str | None]:
    if reference.startswith(("data:", "http://", "https://", "//")):
        return None, None
    try:
        resolved = (path.parent / reference).resolve()
        relative = resolved.relative_to(ROOT)
    except (OSError, ValueError) as exc:
        return None, f"ruta fuera del repositorio o inválida {reference!r}: {exc}"
    if relative.parts and relative.parts[0] == "artifacts":
        return None, f"ruta no publicable bajo artifacts {reference!r}"
    return resolved, None


def validate_path(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"{path}: no se pudo leer: {exc}"]

    parser = MediaParser()
    parser.feed(text)
    errors: list[str] = []

    for reference in local_references(text, parser):
        resolved, error = resolve_local(path, reference)
        if error:
            errors.append(f"{path}: {error}")
            continue
        if resolved is None:
            continue
        if not resolved.exists():
            errors.append(f"{path}: medio faltante {reference!r}")
            continue
        if resolved.suffix.casefold() not in MEDIA_SUFFIXES:
            errors.append(f"{path}: extensión de medio no reconocida {reference!r}")

    for image in parser.images:
        if image.alt.strip() == "" and image.aria_hidden.casefold() != "true":
            errors.append(
                f"{path}:{image.line}: imagen de contenido sin alt ni aria-hidden: {image.path!r}"
            )

    if path.name == "Rutina_Dia_1_Espalda_Biceps_V1.html":
        media_block = re.search(r"const\s+media\s*=\s*\[(.*?)\];", text, flags=re.I | re.S)
        entries = DAY1_MEDIA_ENTRY.findall(media_block.group(1)) if media_block else []
        keys = tuple(entry[2] for entry in entries)
        if keys != DAY1_MEDIA_KEYS:
            errors.append(
                f"{path}: orden de media del Día 1 esperado={DAY1_MEDIA_KEYS} observado={keys}"
            )
    return errors


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    argument_parser = argparse.ArgumentParser(
        description="Valida referencias técnicas de medios en rutinas canónicas."
    )
    argument_parser.add_argument(
        "paths", nargs="*", type=Path, help="HTML canónicas; por defecto se validan todas"
    )
    args = argument_parser.parse_args(argv)
    paths = args.paths or sorted(CANONICAL_DIR.glob("*.html"))
    errors = [error for path in paths for error in validate_path(path)]
    if errors:
        print("ROUTINE_MEDIA_FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"ROUTINE_MEDIA_OK routines={len(paths)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

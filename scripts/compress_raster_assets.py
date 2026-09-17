#!/usr/bin/env python3
"""Comprime imágenes rasterizadas del material de rutinas y del HTML canónico.

La operación es conservadora: solo reemplaza un recurso cuando la versión
comprimida es más pequeña. No cambia nombres, extensiones ni referencias.
"""

from __future__ import annotations

import argparse
import base64
import io
import re
import tempfile
from pathlib import Path

from PIL import Image, ImageSequence


RASTER_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
DATA_URI_RE = re.compile(
    r"data:(image/(?:png|jpe?g|gif|webp));base64,([A-Za-z0-9+/=]+)",
    re.IGNORECASE,
)


def _save_gif(image: Image.Image, output: io.BytesIO) -> None:
    frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
    durations = [
        frame.info.get("duration", image.info.get("duration", 100)) for frame in ImageSequence.Iterator(image)
    ]
    if not frames:
        frames = [image.copy()]
        durations = [image.info.get("duration", 100)]
    first, *rest = frames
    kwargs = {
        "format": "GIF",
        "save_all": True,
        "append_images": rest,
        "duration": durations,
        "loop": image.info.get("loop", 0),
        "optimize": True,
    }
    if "transparency" in image.info:
        kwargs["transparency"] = image.info["transparency"]
    first.save(output, **kwargs)


def _encode(image: Image.Image, mime: str, extension: str) -> bytes:
    output = io.BytesIO()
    mime = mime.lower()
    if mime == "image/gif" or extension.lower() == ".gif":
        _save_gif(image, output)
    elif mime in {"image/jpeg", "image/jpg"} or extension.lower() in {".jpg", ".jpeg"}:
        rgb = image.convert("RGB") if image.mode not in {"RGB", "L"} else image
        rgb.save(output, format="JPEG", quality=82, optimize=True, progressive=True)
    elif mime == "image/webp" or extension.lower() == ".webp":
        image.save(output, format="WEBP", quality=82, method=6)
    else:
        save_image = image
        save_image.save(output, format="PNG", optimize=True, compress_level=9)
    return output.getvalue()


def _compressed_bytes(raw: bytes, mime: str, extension: str) -> bytes:
    with Image.open(io.BytesIO(raw)) as image:
        return _encode(image, mime, extension)


def _format_bytes(value: int) -> str:
    units = ("B", "KB", "MB", "GB")
    number = float(value)
    for unit in units:
        if number < 1024 or unit == units[-1]:
            return f"{number:.2f} {unit}"
        number /= 1024
    return f"{value} B"


def _replace_external(path: Path, apply: bool) -> tuple[int, int, bool]:
    original = path.read_bytes()
    try:
        with Image.open(io.BytesIO(original)) as image:
            mime = Image.MIME.get(image.format, "")
        compressed = _compressed_bytes(original, mime, path.suffix)
    except Exception as exc:  # pragma: no cover - reports malformed optional assets
        print(f"SKIP {path}: {exc}")
        return len(original), len(original), False
    if len(compressed) >= len(original):
        return len(original), len(original), False
    if apply:
        with tempfile.NamedTemporaryFile(prefix=f"{path.stem}.", suffix=path.suffix, dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(compressed)
        temporary.replace(path)
    return len(original), len(compressed), True


def _replace_embedded(html_path: Path, apply: bool) -> tuple[int, int, int, str]:
    text = html_path.read_text(encoding="utf-8")
    changed = 0
    before = 0
    after = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal changed, before, after
        mime = match.group(1).lower()
        raw = base64.b64decode(match.group(2))
        before += len(raw)
        try:
            compressed = _compressed_bytes(raw, mime, "." + mime.split("/")[-1])
        except Exception as exc:  # pragma: no cover - reports malformed optional assets
            print(f"SKIP embedded image in {html_path}: {exc}")
            after += len(raw)
            return match.group(0)
        if len(compressed) >= len(raw):
            after += len(raw)
            return match.group(0)
        changed += 1
        after += len(compressed)
        return f"data:{mime};base64,{base64.b64encode(compressed).decode('ascii')}"

    new_text = DATA_URI_RE.sub(replace, text)
    if apply and new_text != text:
        with tempfile.NamedTemporaryFile(prefix=f"{html_path.stem}.", suffix=html_path.suffix, dir=html_path.parent, delete=False, mode="w", encoding="utf-8", newline="") as handle:
            temporary = Path(handle.name)
            handle.write(new_text)
        temporary.replace(html_path)
    return before, after, changed, new_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("data/rutinas_autocontenidas"))
    parser.add_argument("--html", type=Path, default=Path("data/rutinas_autocontenidas/canonicas/Rutina_Dia_1_Espalda_Biceps_V1.html"))
    parser.add_argument("--apply", action="store_true", help="reemplaza solo recursos con una versión menor")
    args = parser.parse_args()

    external_before = external_after = external_changed = 0
    external_files = [p for p in args.root.rglob("*") if p.is_file() and p.suffix.lower() in RASTER_EXTENSIONS]
    for path in external_files:
        before, after, changed = _replace_external(path, args.apply)
        external_before += before
        external_after += after
        external_changed += int(changed)

    embedded_before, embedded_after, embedded_changed, _ = _replace_embedded(args.html, args.apply)
    before = external_before + embedded_before
    after = external_after + embedded_after
    print(
        f"MODE={'APPLY' if args.apply else 'DRY-RUN'} "
        f"external_files={len(external_files)} external_changed={external_changed} "
        f"embedded_changed={embedded_changed} "
        f"before={_format_bytes(before)} after={_format_bytes(after)} "
        f"saved={_format_bytes(max(0, before - after))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

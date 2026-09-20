"""Publica y deriva el medio local nuevo del ejercicio 6 del Día 1."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts" / "ejercicios-compartido"
PUBLISHED = ROOT / "data" / "rutinas_autocontenidas" / "medios_publicados"
VIDEO_OUT = PUBLISHED / "ejercicios-compartido" / "videos"
IMAGE_OUT = PUBLISHED / "ejercicios-compartido" / "images"
DERIVED_OUT = PUBLISHED / "rutinas_autocontenidas" / "dia1_media_generated"
MANIFEST_OUT = ROOT / "data" / "rutinas_autocontenidas" / "evidencia" / "dia1_media_manifest.json"
SOURCE_COMMIT = "7455efae41b330c265e7cd4b78dfa848e7ce5ebd"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save_frame(source: Path, destination: Path, frame_index: int) -> dict[str, int]:
    with Image.open(source) as image:
        image.seek(frame_index)
        frame = image.convert("RGB")
        frame.save(destination, format="JPEG", quality=92, optimize=True)
        return {"width": frame.width, "height": frame.height, "frame": frame_index}


def main() -> None:
    repo_id = "0575-q6y3OhV"
    source_gif = SOURCE / "videos" / f"{repo_id}.gif"
    source_image = SOURCE / "images" / f"{repo_id}.jpg"
    if not source_gif.is_file() or not source_image.is_file():
        raise FileNotFoundError(f"Falta la pareja GIF/imagen de {repo_id}")

    VIDEO_OUT.mkdir(parents=True, exist_ok=True)
    IMAGE_OUT.mkdir(parents=True, exist_ok=True)
    DERIVED_OUT.mkdir(parents=True, exist_ok=True)
    published_gif = VIDEO_OUT / source_gif.name
    published_reference = IMAGE_OUT / source_image.name
    shutil.copy2(source_gif, published_gif)
    shutil.copy2(source_image, published_reference)

    with Image.open(source_gif) as gif:
        frames = int(getattr(gif, "n_frames", 1))
        duration = int(gif.info.get("duration", 0) or 0)
    start = DERIVED_OUT / f"{repo_id}-start.jpg"
    final = DERIVED_OUT / f"{repo_id}-final.jpg"
    reference = DERIVED_OUT / f"{repo_id}-machine-reference.png"
    dimensions = save_frame(source_gif, start, 0)
    save_frame(source_gif, final, max(frames - 1, 0))
    with Image.open(source_image) as image:
        image.convert("RGBA").save(reference, format="PNG", optimize=True)

    manifest = json.loads(MANIFEST_OUT.read_text(encoding="utf-8"))
    item = next(item for item in manifest["items"] if item["exercise_number"] == 6)
    item.update(
        {
            "exercise": "Curl de bíceps sentado en máquina",
            "dataset_id": "0575",
            "dataset_name": "lever bicep curl",
            "equipment": "leverage machine",
            "gif": "artifacts/ejercicios-compartido/videos/0575-q6y3OhV.gif",
            "thumbnail": "artifacts/ejercicios-compartido/images/0575-q6y3OhV.jpg",
            "sha256_gif": sha256(source_gif),
            "dimensions": f"{dimensions['width']}x{dimensions['height']}",
            "frames": frames,
            "source_commit": SOURCE_COMMIT,
            "attribution": "© Gym visual — https://gymvisual.com/",
            "derived_media": {
                "start": str(start.relative_to(ROOT)).replace("\\", "/"),
                "final": str(final.relative_to(ROOT)).replace("\\", "/"),
                "machine_reference": str(reference.relative_to(ROOT)).replace("\\", "/"),
                "sha256_start": sha256(start),
                "sha256_final": sha256(final),
                "sha256_machine_reference": sha256(reference),
            },
            "rights_status": "CANDIDATES_PENDING_LICENSE_REVIEW",
            "equipment_identity_status": "VISUAL_PATTERN_REFERENCE_ONLY",
        }
    )
    MANIFEST_OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"PREPARED_DAY1_MEDIA dataset_id=0575 manifest={MANIFEST_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

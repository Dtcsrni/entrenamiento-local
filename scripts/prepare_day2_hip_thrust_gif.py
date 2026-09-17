"""Recorta un tramo validado de un video local de hip thrust en máquina."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
from PIL import Image


START_SECONDS = 3.5
END_SECONDS = 12.0
OUTPUT_FPS = 15
OUTPUT_SIZE = 360
OUTPUT_HEIGHT = 180
SOURCE_CROP_LEFT = 0
SOURCE_CROP_TOP = 0
SOURCE_CROP_WIDTH = 720
SOURCE_CROP_HEIGHT = 360
PEAK_SECONDS = 5.0


def build_gif(
    source: Path,
    output: Path,
    thumbnail: Path,
    phase_inicio: Path | None = None,
    phase_final: Path | None = None,
) -> tuple[int, float, tuple[int, int]]:
    capture = cv2.VideoCapture(str(source))
    if not capture.isOpened():
        raise RuntimeError(f"No se pudo abrir el video: {source}")

    source_fps = capture.get(cv2.CAP_PROP_FPS)
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if source_fps <= 0 or total_frames <= 0:
        capture.release()
        raise RuntimeError("El video no expone FPS o cantidad de cuadros válidos")

    start_frame = max(0, int(round(START_SECONDS * source_fps)))
    end_frame = min(total_frames - 1, int(round(END_SECONDS * source_fps)))
    step = max(1, int(round(source_fps / OUTPUT_FPS)))
    frames: list[Image.Image] = []

    capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    for frame_number in range(start_frame, end_frame + 1):
        ok, frame = capture.read()
        if not ok:
            break
        if (frame_number - start_frame) % step:
            continue

        height, width = frame.shape[:2]
        left = min(max(0, SOURCE_CROP_LEFT), width - 1)
        top = min(max(0, SOURCE_CROP_TOP), height - 1)
        crop_width = min(SOURCE_CROP_WIDTH, width - left)
        crop_height = min(SOURCE_CROP_HEIGHT, height - top)
        crop = frame[top : top + crop_height, left : left + crop_width]
        rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        frames.append(Image.fromarray(rgb).resize((OUTPUT_SIZE, OUTPUT_HEIGHT), Image.Resampling.LANCZOS))

    capture.release()
    if len(frames) < 20:
        raise RuntimeError(f"El tramo seleccionado produjo muy pocos cuadros: {len(frames)}")

    output.parent.mkdir(parents=True, exist_ok=True)
    thumbnail.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=round(1000 / OUTPUT_FPS),
        loop=0,
        optimize=False,
    )
    frames[0].save(thumbnail, format="JPEG", quality=94, optimize=True)
    phase_inicio = phase_inicio or output.with_name(f"{output.stem}_inicio.jpg")
    phase_final = phase_final or output.with_name(f"{output.stem}_final.jpg")
    frames[0].convert("RGB").save(phase_inicio, format="JPEG", quality=95, optimize=True, subsampling=0)
    peak_index = min(len(frames) - 1, round(OUTPUT_FPS * PEAK_SECONDS))
    frames[peak_index].convert("RGB").save(phase_final, format="JPEG", quality=95, optimize=True, subsampling=0)
    return len(frames), len(frames) * round(1000 / OUTPUT_FPS) / 1000, (OUTPUT_SIZE, OUTPUT_HEIGHT)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("thumbnail", type=Path)
    args = parser.parse_args()
    frames, seconds, size = build_gif(args.source, args.output, args.thumbnail)
    print(f"GENERATED {args.output} frames={frames} seconds={seconds:.2f} size={size[0]}x{size[1]}")


if __name__ == "__main__":
    main()

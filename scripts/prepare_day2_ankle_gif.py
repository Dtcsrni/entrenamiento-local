"""Genera un GIF enfocado de círculos de tobillo desde un video ya descargado.

El recorte evita la fase de explicación y conserva sólo la demostración filmada
del movimiento. El archivo de entrada es temporal y no forma parte del repo.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
from PIL import Image


def build_gif(source: Path, output: Path, thumbnail: Path) -> None:
    capture = cv2.VideoCapture(str(source))
    if not capture.isOpened():
        raise RuntimeError(f"No se pudo abrir el video: {source}")

    fps = capture.get(cv2.CAP_PROP_FPS) or 30.0
    start_frame = int(round(19.4 * fps))
    end_frame = int(round(25.7 * fps))
    frame_step = max(1, int(round(fps / 15.0)))
    frames: list[Image.Image] = []
    frame_index = 0

    while True:
        ok, frame = capture.read()
        if not ok:
            break
        if start_frame <= frame_index <= end_frame and (frame_index - start_frame) % frame_step == 0:
            height, width = frame.shape[:2]
            side = min(height, 360)
            left = max(0, min(width - side, 90))
            top = max(0, (height - side) // 2)
            crop = frame[top : top + side, left : left + side]
            rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(rgb).resize((360, 360), Image.Resampling.LANCZOS))
        frame_index += 1

    capture.release()
    if len(frames) < 20:
        raise RuntimeError(f"El segmento produjo muy pocos cuadros: {len(frames)}")

    output.parent.mkdir(parents=True, exist_ok=True)
    thumbnail.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=67,
        loop=0,
        optimize=True,
        disposal=2,
    )
    frames[0].save(thumbnail, quality=90, optimize=True)
    print(f"GENERATED {output} frames={len(frames)} size={frames[0].size}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--thumbnail", type=Path, required=True)
    args = parser.parse_args()
    build_gif(args.input, args.output, args.thumbnail)


if __name__ == "__main__":
    main()

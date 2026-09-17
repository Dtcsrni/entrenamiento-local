from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_routine_media import validate_path  # noqa: E402


CANONICAL = ROOT / "data" / "rutinas_autocontenidas" / "canonicas"


class RoutineMediaValidationTests(unittest.TestCase):
    def test_current_canonical_media_references_exist(self) -> None:
        for path in sorted(CANONICAL.glob("*.html")):
            with self.subTest(path=path.name):
                self.assertEqual(validate_path(path), [])

    def test_missing_media_is_reported(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            root = Path(directory)
            html = root / "routine.html"
            html.write_text(
                '<img src="missing.gif" alt="GIF del ejercicio">', encoding="utf-8"
            )
            errors = validate_path(html)
        self.assertTrue(any("medio faltante" in error for error in errors))

    def test_content_image_without_alt_is_reported(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            root = Path(directory)
            image = root / "image.jpg"
            image.write_bytes(b"fixture")
            html = root / "routine.html"
            html.write_text('<img src="image.jpg">', encoding="utf-8")
            errors = validate_path(html)
        self.assertTrue(any("sin alt" in error for error in errors))

    def test_day1_media_mapping_order_is_detected(self) -> None:
        source = (CANONICAL / "Rutina_Dia_1_Espalda_Biceps_V1.html").read_text(
            encoding="utf-8"
        )
        mutated = source.replace(
            'key:"APERTURA INVERSA EN MÁQUINA"',
            'key:"REMO HORIZONTAL EN MÁQUINA"',
            1,
        )
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            path = Path(directory) / "Rutina_Dia_1_Espalda_Biceps_V1.html"
            path.write_text(mutated, encoding="utf-8")
            errors = validate_path(path)
        self.assertTrue(any("orden de media del Día 1" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

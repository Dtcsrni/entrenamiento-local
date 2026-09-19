from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_canonical_routines import validate_path  # noqa: E402


CANONICAL = ROOT / "data" / "rutinas_autocontenidas" / "canonicas"


class CanonicalRoutineValidationTests(unittest.TestCase):
    def test_day2_matches_its_declared_contract(self) -> None:
        self.assertEqual(
            validate_path(CANONICAL / "Rutina_Dia_2_Pierna_Gluteo_V1.html"), []
        )

    def test_day1_matches_its_declared_contract(self) -> None:
        self.assertEqual(
            validate_path(CANONICAL / "Rutina_Dia_1_Espalda_Biceps_V1.html"), []
        )

    def test_day1_corruption_is_detected(self) -> None:
        source = (CANONICAL / "Rutina_Dia_1_Espalda_Biceps_V1.html").read_text(
            encoding="utf-8"
        )
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            path = Path(directory) / "Rutina_Dia_1_Espalda_Biceps_V1.html"
            path.write_text(source.replace('data-exercise="3"', 'data-exercise="5"', 1), encoding="utf-8")
            errors = validate_path(path)
        self.assertTrue(any("secuencia contigua" in error for error in errors))

    def test_day3_matches_its_declared_contract(self) -> None:
        self.assertEqual(
            validate_path(CANONICAL / "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html"), []
        )

    def test_day3_current_exercise_cue_is_detected(self) -> None:
        source = (CANONICAL / "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html").read_text(
            encoding="utf-8"
        )
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            path = Path(directory) / "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html"
            path.write_text(source.replace('data-next="2"', 'data-next="1"', 1), encoding="utf-8")
            errors = validate_path(path)
        self.assertTrue(any("apunta a 1; se esperaba 2" in error for error in errors))

    def test_day3_does_not_keep_day1_media_repairs(self) -> None:
        source = (CANONICAL / "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("machineOnlyCurl", source)
        self.assertNotIn("finalAssets", source)
        self.assertNotIn(
            "confirma directamente la identidad de la máquina del gimnasio", source
        )


if __name__ == "__main__":
    unittest.main()

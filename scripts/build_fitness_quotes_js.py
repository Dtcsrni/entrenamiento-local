"""Genera el módulo local que consume la rutina autocontenida."""

from pathlib import Path
import json


root = Path(__file__).resolve().parents[1]
source = root / "data" / "rutinas_autocontenidas" / "frases_fitness" / "fitness_quotes.json"
target = root / "data" / "rutinas_autocontenidas" / "frases_fitness" / "fitness_quotes.js"
payload = json.loads(source.read_text(encoding="utf-8"))
target.write_text(
    "window.fitnessQuotesData = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n",
    encoding="utf-8",
)
print(f"QUOTES_JS_OK quotes={payload['count']} portraits={payload['portraitCount']} output={target}")

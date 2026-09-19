"""Construye el banco local de frases fitness con metadatos de procedencia.

La fuente de citas es Quotables (CC0). La selección es deliberadamente
conservadora: exige vocabulario explícito de ejercicio/deporte y descarta
usos evidentes que no hablan de entrenamiento. Las traducciones se solicitan
solo durante la construcción; la rutina no consulta ningún servicio externo.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote as urlquote, unquote as urlunquote
from urllib.request import Request, urlopen

try:
    import argostranslate.translate as argos_translate  # type: ignore
except ImportError:
    argos_translate = None


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "rutinas_autocontenidas" / "frases_fitness"
SOURCE = DATA / "author-quote.txt"
OUT = DATA / "fitness_quotes.json"
PORTRAITS = DATA / "retratos"

TRANSLATION_URL = "https://api.mymemory.translated.net/get"

STRONG_TERMS = (
    "exercise", "exercising", "workout", "fitness", "muscle", "muscles",
    "athlete", "athletic", "sportsman", "sportswoman", "sport", "sports", "training", "trained", "train",
    "gym", "bodybuilding", "weightlifting", "powerlifting", "lifting", "lifted",
    "bench press", "squat", "squats", "deadlift", "pull-up", "pullups", "push-up",
    "pushups", "marathon", "sprint", "swim", "swimming", "swimmer", "cyclist",
    "cycling", "boxing", "boxer", "football", "basketball", "soccer", "tennis",
    "yoga", "climbing", "runner", "running", "race", "racing", "coach", "coaching",
    "baseball", "hockey", "golf", "volleyball", "skating", "skiing", "surfing", "wrestling", "karate", "judo", "rowing",
)
CONTEXT_TERMS = (
    "strength", "strong", "physical", "physically", "health", "healthy", "discipline",
    "effort", "practice", "practise", "repetition", "reps", "performance", "competition",
    "compete", "champion", "team", "game", "fight", "fighting", "speed", "endurance",
    "stamina", "conditioning", "cardio", "body", "weight", "weights", "play", "playing",
    "win", "winning", "goal", "goals",
)
EXCLUDE_TERMS = (
    "video game", "computer game", "need for speed", "constitutional right",
    "exercise in logic", "exercise of power", "acting coach", "coach to prepare",
    "train to sing", "train to dance", "train station", "freight train", "train wreck",
    "sports car", "sporting chance",
)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"\W+", " ", text.lower()).strip()


def terms_in(text: str, terms: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    found: list[str] = []
    for term in terms:
        pattern = r"(?<![a-z])" + re.escape(term) + r"(?![a-z])"
        if re.search(pattern, lowered):
            found.append(term)
    return found


def select_quotes() -> list[dict[str, object]]:
    if not SOURCE.exists():
        raise SystemExit(f"No existe la fuente descargada: {SOURCE}")
    selected: list[dict[str, object]] = []
    seen: set[str] = set()
    for line in SOURCE.read_text(encoding="utf-8", errors="replace").splitlines():
        author, sep, content = line.partition("\t")
        if not sep or not author.strip() or not content.strip():
            continue
        content = re.sub(r"\s+", " ", content.replace("\ufffd", "")).strip()
        if len(content) < 24 or len(content) > 520:
            continue
        key = normalize(content)
        if not key or key in seen:
            continue
        strong = terms_in(content, STRONG_TERMS)
        context = terms_in(content, CONTEXT_TERMS)
        lowered = content.lower()
        if any(term in lowered for term in EXCLUDE_TERMS):
            continue
        # Una mención explícita de ejercicio/deporte basta; los términos
        # contextuales solos no convierten una frase en frase fitness.
        if not strong:
            continue
        score = len(strong) * 3 + len(context)
        # Prioriza el lenguaje de entrenamiento frente a usos deportivos
        # accidentales y evita frases extremadamente largas para la tarjeta.
        if any(term in strong for term in ("exercise", "workout", "fitness", "muscle", "training", "gym", "bodybuilding", "weightlifting", "powerlifting")):
            score += 4
        seen.add(key)
        selected.append({
            "author": author.strip(),
            "quoteOriginal": content,
            "topics": strong + context,
            "selectionScore": score,
        })
    selected.sort(key=lambda item: (-int(item["selectionScore"]), len(str(item["quoteOriginal"])), str(item["author"])))
    if len(selected) < 1000:
        raise SystemExit(f"La selección explícitamente fitness solo contiene {len(selected)} frases; no se rellenará con contenido ajeno.")
    return selected[:1000]


def http_json(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "Entrenamiento-local/1.0"})
    with urlopen(request, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def translate(text: str) -> str:
    if argos_translate is not None:
        translated = str(argos_translate.translate(text, "en", "es")).strip()
        if translated:
            return translated
    url = TRANSLATION_URL + "?q=" + urlquote(text) + "&langpair=en|es"
    result = http_json(url)
    translated = str(result.get("responseData", {}).get("translatedText", "")).strip()
    if not translated or translated.lower() == text.lower():
        raise ValueError("traducción vacía o sin traducir")
    return translated


def translate_item(item: dict[str, object]) -> tuple[dict[str, object], str | None]:
    for attempt in range(4):
        try:
            item["quoteEs"] = translate(str(item["quoteOriginal"]))
            return item, None
        except Exception as error:  # noqa: BLE001 - se informa al final de la tarea
            if attempt == 3:
                return item, str(error)
            time.sleep(1.5 * (attempt + 1))
    return item, "error de traducción desconocido"


def slug(text: str) -> str:
    value = normalize(text).replace(" ", "-")
    return value[:70] or "autor"


def wikidata_portraits(authors: list[str]) -> dict[str, dict[str, str]]:
    values = " ".join('"' + author.replace('"', '\\"') + '"@en' for author in authors)
    query = """SELECT ?personLabel ?image WHERE {
      VALUES ?personLabel { %s }
      ?person rdfs:label ?personLabel.
      ?person wdt:P18 ?image.
    }""" % values
    url = "https://query.wikidata.org/sparql?format=json&query=" + urlquote(query)
    result = http_json(url)
    portraits: dict[str, dict[str, str]] = {}
    for binding in result.get("results", {}).get("bindings", []):
        author = str(binding.get("personLabel", {}).get("value", ""))
        image_url = str(binding.get("image", {}).get("value", ""))
        if author and image_url and author not in portraits:
            file_name = urlunquote(image_url.rsplit("/", 1)[-1]).replace("_", " ")
            image_url = image_url.replace("http://", "https://", 1)
            if "?" not in image_url:
                image_url += "?width=320"
            portraits[author] = {
                "fileName": file_name,
                "imageUrl": image_url,
                "commonsUrl": "https://commons.wikimedia.org/wiki/File:" + urlquote(file_name.replace(" ", "_")),
            }
    return portraits


def download_portrait(author: str, portrait: dict[str, str]) -> str:
    PORTRAITS.mkdir(parents=True, exist_ok=True)
    name = slug(author) + ".jpg"
    destination = PORTRAITS / name
    if not destination.exists() or destination.stat().st_size < 512:
        request = Request(portrait["imageUrl"], headers={"User-Agent": "Entrenamiento-local/1.0"})
        with urlopen(request, timeout=35) as response:
            payload = response.read()
        if len(payload) < 512:
            raise ValueError("retrato descargado demasiado pequeño")
        destination.write_bytes(payload)
    return "retratos/" + name


def main() -> None:
    selected = select_quotes()
    errors: list[str] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(translate_item, item) for item in selected]
        for index, future in enumerate(as_completed(futures), start=1):
            item, error = future.result()
            if error:
                errors.append(f"{item['author']}: {error}")
            if index % 50 == 0:
                print(f"traducidas={index}/1000")
    if errors:
        raise SystemExit("No se pudieron traducir todas las frases:\n" + "\n".join(errors[:10]))

    authors = list(dict.fromkeys(str(item["author"]) for item in selected))
    try:
        by_author = wikidata_portraits(authors)
    except Exception as error:  # noqa: BLE001 - se conserva la cita y queda fallback visual
        print(f"AVISO consulta de retratos: {error}", file=sys.stderr)
        by_author = {}
    author_assets: dict[str, dict[str, str]] = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {
            pool.submit(download_portrait, author, portrait): (author, portrait)
            for author, portrait in by_author.items()
        }
        for future in as_completed(futures):
            author, portrait = futures[future]
            try:
                local_path = future.result()
                author_assets[author] = {**portrait, "localPath": local_path}
            except Exception as error:  # noqa: BLE001 - queda fallback de iniciales
                print(f"AVISO descarga retrato {author}: {error}", file=sys.stderr)
    for item in selected:
        author = str(item["author"])
        portrait = author_assets.get(author)
        if portrait:
            item["portrait"] = portrait["localPath"]
        item.pop("selectionScore", None)
    payload = {
        "schemaVersion": 1,
        "language": "es",
        "count": len(selected),
        "authorCount": len({str(item["author"]) for item in selected}),
        "portraitCount": len(author_assets),
        "quotes": selected,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"BANK_OK quotes={len(selected)} authors={payload['authorCount']} portraits={payload['portraitCount']} output={OUT}")


if __name__ == "__main__":
    main()

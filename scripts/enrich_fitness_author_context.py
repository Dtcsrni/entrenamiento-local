#!/usr/bin/env python3
"""Añade descriptores de autor en español usando coincidencias exactas de Wikidata."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def fetch_author(author: str) -> tuple[str, str] | None:
    params = urllib.parse.urlencode(
        {
            "action": "wbsearchentities",
            "search": author,
            "language": "es",
            "uselang": "es",
            "format": "json",
            "limit": 3,
        }
    )
    url = f"https://www.wikidata.org/w/api.php?{params}"
    request = urllib.request.Request(url, headers={"User-Agent": "EntrenamientoLocal/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.load(response)
    target = normalize(author)
    for result in payload.get("search", []):
        if normalize(result.get("label", "")) == target and result.get("description"):
            return result["description"].strip(), f"https://www.wikidata.org/wiki/{result['id']}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/rutinas_autocontenidas/frases_fitness/fitness_quotes.json"))
    parser.add_argument("--output-js", type=Path, default=Path("data/rutinas_autocontenidas/frases_fitness/fitness_quotes.js"))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    authors = list(dict.fromkeys(item["author"] for item in data["quotes"]))
    contexts: dict[str, tuple[str, str]] = {}
    failed: list[str] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        pending = {executor.submit(fetch_author, author): author for author in authors}
        for future in as_completed(pending):
            author = pending[future]
            try:
                result = future.result()
            except Exception as exc:  # pragma: no cover - network-dependent fallback
                print(f"WARN {author}: {exc}", flush=True)
                result = None
            if result:
                contexts[author] = result
            else:
                failed.append(author)

    for item in data["quotes"]:
        result = contexts.get(item["author"])
        if result:
            item["authorContext"] = result[0]
        else:
            item.pop("authorContext", None)

    if args.apply:
        serialized = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        args.input.write_text(serialized, encoding="utf-8", newline="")
        args.output_js.write_text(
            "window.fitnessQuotesData = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
            encoding="utf-8",
            newline="",
        )
    print(f"MODE={'APPLY' if args.apply else 'DRY-RUN'} authors={len(authors)} contexts={len(contexts)} missing={len(failed)}")
    if failed:
        print("MISSING " + " | ".join(failed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

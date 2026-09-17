"""Asocia y descarga retratos de Wikimedia Commons para el banco local."""

from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote as urlquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_fitness_quote_bank as bank  # noqa: E402


def commons_metadata(portraits: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    values = list(portraits.items())
    for offset in range(0, len(values), 40):
        chunk = values[offset : offset + 40]
        titles = "|".join("File:" + item["fileName"] for _, item in chunk)
        url = (
            "https://commons.wikimedia.org/w/api.php?action=query&titles="
            + urlquote(titles)
            + "&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=320&format=json"
        )
        try:
            data = bank.http_json(url)
        except Exception as error:  # noqa: BLE001 - se conserva URL y licencia pendiente
            print(f"AVISO metadatos Commons bloque {offset}: {error}", file=sys.stderr)
            result.update(dict(chunk))
            continue
        pages = data.get("query", {}).get("pages", {})
        by_file = {}
        for page in pages.values():
            info = (page.get("imageinfo") or [{}])[0]
            meta = info.get("extmetadata", {})
            if info.get("url"):
                by_file[page.get("title", "").removeprefix("File:")] = {
                    "imageUrl": str(info.get("thumburl") or info["url"]),
                    "license": str(meta.get("LicenseShortName", {}).get("value", "")),
                    "credit": str(meta.get("Credit", {}).get("value", "") or meta.get("Artist", {}).get("value", "")),
                }
        for author, portrait in chunk:
            extra = by_file.get(portrait["fileName"])
            if extra:
                result[author] = {**portrait, **extra}
    return result


def main() -> None:
    source = bank.OUT
    payload = json.loads(source.read_text(encoding="utf-8"))
    authors = list(dict.fromkeys(str(item["author"]) for item in payload["quotes"]))
    portraits: dict[str, dict[str, str]] = {}
    for offset in range(0, len(authors), 40):
        chunk = authors[offset : offset + 40]
        try:
            portraits.update(bank.wikidata_portraits(chunk))
        except Exception as error:  # noqa: BLE001 - conserva fallback de iniciales
            print(f"AVISO Wikidata bloque {offset}: {error}", file=sys.stderr)
        print(f"autores consultados={min(offset + 40, len(authors))}/{len(authors)} retratos encontrados={len(portraits)}")
    portraits = commons_metadata(portraits)
    assets: dict[str, dict[str, str]] = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(bank.download_portrait, author, portrait): (author, portrait) for author, portrait in portraits.items()}
        for future in as_completed(futures):
            author, portrait = futures[future]
            try:
                assets[author] = {**portrait, "localPath": future.result()}
            except Exception as error:  # noqa: BLE001
                print(f"AVISO descarga {author}: {error}", file=sys.stderr)
    for item in payload["quotes"]:
        asset = assets.get(str(item["author"]))
        if asset:
            item["portrait"] = asset["localPath"]
            item["portraitLicense"] = asset.get("license", "")
            item["portraitCredit"] = asset.get("credit", "")
            item["portraitSource"] = asset["commonsUrl"]
    payload["portraitCount"] = len(assets)
    payload["portraitAuthorCount"] = len(assets)
    source.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PORTRAITS_OK authors={len(assets)} quotes={sum(1 for item in payload['quotes'] if 'portrait' in item)}")


if __name__ == "__main__":
    main()

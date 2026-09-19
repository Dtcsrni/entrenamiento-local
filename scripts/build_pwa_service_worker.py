"""Genera el service worker con el inventario offline de las rutinas canónicas."""

from __future__ import annotations

import hashlib
import re
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = ROOT / "data" / "rutinas_autocontenidas" / "canonicas"
OUTPUT = ROOT / "sw.js"
ROUTINE_FILES = (
    "Rutina_Dia_1_Espalda_Biceps_V1.html",
    "Rutina_Dia_2_Pierna_Gluteo_V1.html",
    "Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html",
    "Rutina_Dia_4_Pierna_Equilibrio_V1.html",
)
HTML_ATTR_PATTERN = re.compile(r"(?:src|data-static-src|gif|thumbnail)\s*[:=]\s*[\"']([^\"']+)")


class ResourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value and name in {"src", "data-static-src"}:
                self.references.add(value)


def resolve_reference(canonical: Path, reference: str) -> str | None:
    if reference.startswith(("http://", "https://", "data:", "#", "/")):
        return None
    canonical_url = PurePosixPath(canonical.relative_to(ROOT).as_posix())
    resolved = PurePosixPath(*canonical_url.parent.parts, reference).as_posix()
    normalized = PurePosixPath(resolved)
    parts: list[str] = []
    for part in normalized.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    path = "/".join(parts)
    target = ROOT / Path(*parts)
    if not target.is_file():
        raise SystemExit(f"Recurso offline no encontrado: {canonical.relative_to(ROOT)} -> {reference}")
    return f"./{path}"


def routine_resources(canonical: Path) -> set[str]:
    text = canonical.read_text(encoding="utf-8")
    parser = ResourceParser()
    parser.feed(text)
    parser.references.update(match.group(1) for match in HTML_ATTR_PATTERN.finditer(text))
    resources = set()
    for reference in parser.references:
        resolved = resolve_reference(canonical, reference)
        if resolved:
            resources.add(resolved)
    return resources


def build_precache() -> list[str]:
    base = ["./", "./index.html", "./manifest.webmanifest", "./icon.png", "./progress-store.js"]
    routines = [f"./data/rutinas_autocontenidas/canonicas/{name}" for name in ROUTINE_FILES]
    resources = set(base + routines)
    for name in ROUTINE_FILES:
        resources.update(routine_resources(CANONICAL_DIR / name))
    return base + routines + sorted(resources - set(base + routines))


def render(resources: list[str]) -> str:
    material = []
    for resource in resources:
        target = ROOT / Path(resource.removeprefix("./"))
        material.append(resource.encode("utf-8"))
        if target.is_file():
            material.append(target.read_bytes())
    fingerprint = hashlib.sha256(b"\n".join(material)).hexdigest()[:12]
    precache = ",\n  ".join(f"{resource!r}" for resource in resources)
    return rf"""const CACHE_NAME = 'entrenamiento-pwa-{fingerprint}';
const PRECACHE = [
  {precache}
];

const ROUTINE_URLS = [
  './data/rutinas_autocontenidas/canonicas/Rutina_Dia_1_Espalda_Biceps_V1.html',
  './data/rutinas_autocontenidas/canonicas/Rutina_Dia_2_Pierna_Gluteo_V1.html',
  './data/rutinas_autocontenidas/canonicas/Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html',
  './data/rutinas_autocontenidas/canonicas/Rutina_Dia_4_Pierna_Equilibrio_V1.html'
];
const LOCAL_REFERENCE = /(?:src|data-static-src|gif|thumbnail)\s*[:=]\s*[\"'](\.\.[^\"']+)[\"']/g;

async function refresh(request, cache) {{
  const response = await fetch(request, {{ cache: 'no-store' }});
  if (response.ok) await cache.put(request, response.clone());
  return response;
}}

async function refreshRoutine(url, cache) {{
  const response = await fetch(url, {{ cache: 'no-store' }});
  if (!response.ok) throw new Error(`${{url}}: HTTP ${{response.status}}`);
  await cache.put(url, response.clone());
  const html = await response.text();
  const base = new URL(url, self.location.href);
  const assetUrls = [...html.matchAll(LOCAL_REFERENCE)]
    .map((match) => new URL(match[1], base))
    .filter((assetUrl) => assetUrl.origin === self.location.origin)
    .map(String);
  await Promise.allSettled([...new Set(assetUrls)].map((assetUrl) => refresh(assetUrl, cache)));
}}

async function refreshApplication() {{
  const cache = await caches.open(CACHE_NAME);
  await Promise.allSettled(PRECACHE.map((url) => refresh(new Request(url), cache)));
  await Promise.allSettled(ROUTINE_URLS.map((url) => refreshRoutine(url, cache)));
}}

self.addEventListener('install', (event) => {{
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
}});

self.addEventListener('activate', (event) => {{
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))))
      .then(() => self.clients.claim())
      .then(() => refreshApplication())
  );
}});

self.addEventListener('message', (event) => {{
  if (event.data?.type === 'SYNC_APP') event.waitUntil(refreshApplication());
}});

self.addEventListener('fetch', (event) => {{
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;

  event.respondWith((async () => {{
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    const isNavigation = request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html');
    const bypassCache = ['no-cache', 'no-store', 'reload'].includes(request.cache);

    if (cached && !bypassCache) {{
      event.waitUntil(refresh(request, cache).catch(() => undefined));
      return cached;
    }}
    try {{
      return await refresh(request, cache);
    }} catch (error) {{
      if (cached) return cached;
      if (isNavigation) return cache.match(new URL('./index.html', self.registration.scope));
      throw error;
    }}
  }})());
}});
"""


def main() -> None:
    resources = build_precache()
    OUTPUT.write_text(render(resources), encoding="utf-8", newline="\n")
    print(f"PWA_SERVICE_WORKER_OK resources={len(resources)} cache={resources[0]}")


if __name__ == "__main__":
    main()

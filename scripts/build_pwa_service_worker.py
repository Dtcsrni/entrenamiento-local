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
TEXT_RESOURCE_SUFFIXES = {".css", ".html", ".js", ".json", ".svg", ".txt", ".webmanifest", ".xml"}


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
    base = [
        "./",
        "./index.html",
        "./manifest.webmanifest",
        "./icon.png",
        "./install-gate.js",
        "./data/profile/mascot-install-phone.png",
        "./progress-store.js",
        "./routine-liquid-glass-v13.css",
        "./data/profile/mouse-female-effort.png",
        "./data/profile/mouse-male-effort.png",
    ]
    routines = [f"./data/rutinas_autocontenidas/canonicas/{name}" for name in ROUTINE_FILES]
    resources = set(base + routines)
    for name in ROUTINE_FILES:
        resources.update(routine_resources(CANONICAL_DIR / name))
    return base + routines + sorted(resources - set(base + routines))


def fingerprint_content(target: Path) -> bytes:
    content = target.read_bytes()
    if target.suffix.lower() in TEXT_RESOURCE_SUFFIXES:
        return content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return content


def render(resources: list[str]) -> str:
    material = []
    for resource in resources:
        target = ROOT / Path(resource.removeprefix("./"))
        material.append(resource.encode("utf-8"))
        if target.is_file():
            material.append(fingerprint_content(target))
    fingerprint = hashlib.sha256(b"\n".join(material)).hexdigest()[:12]
    precache = ",\n  ".join(f"{resource!r}" for resource in resources)
    return rf"""const CACHE_NAME = 'entrenamiento-pwa-{fingerprint}';
const PRECACHE = [
  {precache}
];

async function refresh(request, cache) {{
  const response = await fetch(request, {{ cache: 'no-store' }});
  if (response.ok) await cache.put(request, response.clone());
  return response;
}}

async function notifyClientsAppUpdated() {{
  const updatedAt = Date.now();
  const clients = await self.clients.matchAll({{ type: 'window', includeUncontrolled: true }});
  clients.forEach((client) => client.postMessage({{ type: 'APP_UPDATED', updatedAt, cacheName: CACHE_NAME }}));
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
      .then(() => notifyClientsAppUpdated())
  );
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

"""Collect notices and corresponding sources for Qt libraries absent from wheels.

This runs at build time only. The desktop application never imports this module.
"""
from hashlib import sha256
from pathlib import Path
import json
import shutil
from urllib.request import Request, urlopen
import zipfile

SOURCES = {
    "qtbase": "https://github.com/qt/qtbase/archive/refs/tags/v6.10.1.zip",
    "qtsvg": "https://github.com/qt/qtsvg/archive/refs/tags/v6.10.1.zip",
    "qtimageformats": "https://github.com/qt/qtimageformats/archive/refs/tags/v6.10.1.zip",
    "pyside": "https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.10.1-src/pyside-setup-everywhere-src-6.10.1.zip",
}


def downloadSources(name, url, directory):
    target = directory / f"{name}-6.10.1.zip"
    if not target.exists():
        pending = target.with_suffix(".download")
        request = Request(url, headers={"User-Agent": "PDF-Studio-build-license-collector"})
        try:
            with urlopen(request, timeout=90) as response, pending.open("wb") as stream:
                shutil.copyfileobj(response, stream)
            pending.replace(target)
        finally:
            pending.unlink(missing_ok=True)
    with zipfile.ZipFile(target) as archive:
        if not any("6.10.1" in member for member in archive.namelist()):
            raise RuntimeError(f"Unexpected source version in {target}")
        if archive.testzip() is not None:
            raise RuntimeError(f"Invalid source archive: {target}")
    return target


def copySourceNotices(source, destination):
    copied = []
    with zipfile.ZipFile(source) as archive:
        for member in archive.infolist():
            parts = Path(member.filename).parts[1:]
            if not parts or member.is_dir() or ".." in parts:
                continue
            relative = Path(*parts)
            text = str(relative).lower()
            name = relative.name.lower()
            notice = any(word in name for word in ("license", "licence", "copying", "copyright", "notice", "attribution"))
            notice = notice or "licenses" in [part.lower() for part in parts]
            notice = notice or ("3rdparty" in text and name.startswith("readme"))
            if not notice:
                continue
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))
            copied.append(str(relative))
    if not copied:
        raise RuntimeError(f"No upstream notices in {source}")
    return copied


def collectVendorLicenses(destination):
    destination = Path(destination)
    directory = Path("build/vendor-sources")
    directory.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, url in SOURCES.items():
        archive = downloadSources(name, url, directory)
        copied = copySourceNotices(archive, destination / name)
        digest = sha256(archive.read_bytes()).hexdigest()
        manifest.append({"name": name, "version": "6.10.1", "url": url,
                         "sha256": digest, "noticeFiles": copied})
    for licenseName in ("LGPL-3.0-only.txt", "GPL-3.0-only.txt"):
        if not list(destination.rglob(licenseName)):
            raise RuntimeError(f"Missing Qt open-source license: {licenseName}")
    (directory / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    shutil.copy2(directory / "manifest.json", destination / "source-manifest.json")
    Path("dist").mkdir(exist_ok=True)
    with zipfile.ZipFile("dist/PDF-Studio-Library-Sources.zip", "w", zipfile.ZIP_STORED) as output:
        for source in directory.iterdir():
            if source.suffix in (".zip", ".json"):
                output.write(source, source.name)
    return manifest

"""Collect the actual wheel notices, including native vendored libraries."""
from importlib import metadata
from pathlib import Path
import json
import shutil
import sys


def collectLicenses(destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    manifest = []
    for distribution in metadata.distributions():
        name = distribution.metadata["Name"]
        copied = []
        for relative in distribution.files or []:
            text = str(relative).lower()
            if "license" not in text and "licence" not in text and "copying" not in text and "notice" not in text:
                continue
            source = Path(distribution.locate_file(relative))
            if not source.is_file():
                continue
            safeRelative = Path(*[part for part in Path(relative).parts if part not in ("..", ".")])
            target = destination / name / safeRelative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            copied.append(str(target.relative_to(destination)))
        manifest.append({"name": name, "version": distribution.version,
                         "license": distribution.metadata.get("License-Expression") or distribution.metadata.get("License"),
                         "urls": distribution.metadata.get_all("Project-URL") or [], "files": copied})
    for name in ["PySide6_Essentials", "shiboken6", "pikepdf", "pypdfium2", "pillow"]:
        matching = [entry for entry in manifest if entry["name"].lower().replace("-", "_") == name.lower()]
        if not matching or not matching[0]["files"]:
            raise RuntimeError(f"Missing license files: {name}")
    candidates = [Path(sys.base_prefix) / "LICENSE.txt", Path(sys.base_prefix) / "lib/python3.12/LICENSE.txt"]
    for source in candidates:
        if source.is_file():
            shutil.copy2(source, destination / "PYTHON-LICENSE.txt")
            break
    for fileName in ["LICENSE", "THIRD_PARTY_NOTICES.md"]:
        shutil.copy2(fileName, destination / fileName)
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    collectLicenses("licenses/generated")

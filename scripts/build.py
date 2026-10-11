from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

from collect_licenses import collectLicenses
from create_icon import createIcon


def build():
    collectLicenses("licenses/generated")
    createIcon()
    subprocess.run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "PDF-Studio.spec"], check=True)
    destination = Path("dist/PDF-Studio")
    shutil.copytree("licenses/generated", destination / "licenses", dirs_exist_ok=True)
    for name in ["README.md", "LICENSE", "THIRD_PARTY_NOTICES.md"]:
        shutil.copy2(name, destination / name)
    executable = destination / ("PDF-Studio.exe" if sys.platform == "win32" else "PDF-Studio")
    report = Path("dist/smoke-report.json").resolve()
    subprocess.run([str(executable.resolve()), "--smoke-test", "--smoke-report", str(report)], check=True, timeout=60)
    import json
    result = json.loads(report.read_text(encoding="utf-8"))
    if result.get("status") != "passed":
        raise RuntimeError(f"Packaged application smoke test failed: {result}")
    shutil.copy2(report, destination / "smoke-report.json")
    shutil.make_archive("dist/PDF-Studio-Windows" if sys.platform == "win32" else "dist/PDF-Studio-Linux", "zip", "dist", "PDF-Studio")
    tracked = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
    with zipfile.ZipFile("dist/PDF-Studio-Source.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for name in tracked:
            if name and Path(name).is_file():
                archive.write(name, "PDF-Studio-source/" + name)


if __name__ == "__main__":
    build()

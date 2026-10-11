# One-folder distribution keeps Qt/native libraries separately replaceable.
from PyInstaller.utils.hooks import collect_all

allData, allBinaries, allHidden = [], [], []
for package in ('pikepdf', 'pypdfium2', 'pypdfium2_raw'):
    packageData, packageBinaries, packageHidden = collect_all(package)
    allData += packageData
    allBinaries += packageBinaries
    allHidden += packageHidden

a = Analysis(['run_studio.py'], pathex=['.'], binaries=allBinaries,
             datas=allData, hiddenimports=allHidden, hookspath=[],
             excludes=['tkinter', 'PySide6.QtTest'], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='PDF-Studio',
          debug=False, strip=False, upx=False, console=False)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name='PDF-Studio')

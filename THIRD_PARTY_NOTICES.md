# Bibliotheken und Lizenzhinweise

PDF Studio wird unter GPL-3.0-or-later veröffentlicht. Der vollständige Text steht
in LICENSE. Die Anwendung enthält keine Telemetrie und führt keine Netzwerkanfragen
aus. Nur Entwicklungswerkzeuge und GitHub Actions laden Abhängigkeiten herunter.

| Komponente | Version | Lizenz | Quelle |
| --- | --- | --- | --- |
| Python | 3.12 | PSF und weitere | https://www.python.org/downloads/source/ |
| PySide6-Essentials / Shiboken6 / Qt | 6.10.1 | LGPLv3 / GPLv3, Qt-Drittkomponenten separat | https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.10.1-src/ |
| pikepdf | 10.0.2 | MPL-2.0 | https://github.com/pikepdf/pikepdf/tree/v10.0.2 |
| QPDF (in pikepdf) | siehe Wheel-Lizenztexte | Apache-2.0 | https://github.com/qpdf/qpdf |
| pypdfium2 | 5.3.0 | Apache-2.0 oder BSD-3-Clause | https://github.com/pypdfium2-team/pypdfium2/tree/5.3.0 |
| PDFium und dessen Drittkomponenten | siehe BUILD_LICENSES im Paket | BSD-artig und weitere | https://pdfium.googlesource.com/pdfium/ |
| Pillow | 12.0.0 | MIT-CMU | https://github.com/python-pillow/Pillow/tree/12.0.0 |
| lxml | siehe Paketmanifest | BSD-3-Clause und Drittkomponenten | https://lxml.de/ |
| Deprecated / wrapt / packaging | siehe Paketmanifest | MIT / BSD / Apache | siehe Metadaten der Wheels |
| PyInstaller (Buildwerkzeug) | 6.17.0 | GPL-2.0-or-later mit Bootloader-Ausnahme | https://pyinstaller.org/en/stable/license.html |

Es werden nur QtCore, QtGui und QtWidgets aus dem Essentials-Paket verwendet.
Qt-Zusatzmodule werden nicht benötigt. Qt-DLLs bleiben in der One-Folder-Ausgabe
separat und austauschbar. Reverse Engineering zur Fehlersuche an Änderungen
LGPL-lizenzierter Bibliotheken ist gestattet; die Anwendung enthält keine
technischen Beschränkungen dafür. Keine Bibliothek wurde modifiziert.

Der Build kopiert die Lizenzdateien **der tatsächlich installierten Wheels**
einschließlich PDFium-BUILD_LICENSES und Qt-Lizenzdateien in den Ordner licenses.
Qt-6.10.1-Quellen sind außerdem unter
https://download.qt.io/archive/qt/6.10/6.10.1/single/ verfügbar.
Das Manifest enthält Namen, Versionen und Projekt-/Quelllinks aller installierten
Pakete. Python-Lizenztexte werden ebenfalls übernommen. Die zugehörigen Quellen
von PDF Studio werden als PDF-Studio-Source.zip zusammen mit dem Windows-Paket
veröffentlicht. Zum Austausch der Qt-Bibliotheken kann die Anwendung aus diesen
Quellen mit einer kompatiblen, selbst gebauten PySide6-Version erstellt werden.

Prüfgrundlagen: https://pypi.org/project/PySide6/6.10.1/,
https://pypi.org/project/pikepdf/10.0.2/,
https://pypi.org/project/pypdfium2/5.3.0/,
https://doc.qt.io/qtforpython-6/licenses.html.

# Verifikation für Version 1.0.0

Prüfdatum: 11. Oktober 2026.

## Windows

Der vollständige Windows-Build des implementierten Anwendungsstands
`815bc28064fafa4238454ee479d64c2f2fd7c519` wurde erfolgreich ausgeführt:

https://github.com/JanKarras/PDF-Studio-Lokaler-PDF-Editor/actions/runs/38168602693

- Python 3.12 auf `windows-latest`.
- **49 Tests bestanden**, keine Fehler, keine übersprungenen Tests.
- PyInstaller-One-Folder-Build erfolgreich.
- Gebaute EXE mit dem nativen Windows-Qt-Plattformplugin gestartet.
- Unicode-PDF importiert, mit PDFium gerendert, exportiert und erneut gelesen.
- Qt-Fenster geöffnet; asynchrone Vorschau empfangen; regulär geschlossen.
- Smoke-Report: `status=passed`, `renderSize=[240,360]`, `pages=1`, `gui=true`.
- ZIP enthält EXE, Windows-Plattformplugin, pikepdf/PDFium und vollständige
  Lizenzhinweise einschließlich ergänzter Qt-Open-Source-Lizenzen/Attributionen.
- Das unbenutzte Qt-PDF-Plugin wird nicht verteilt.
- Windows-ZIP, Anwendungsquellen und Qt-/PySide6-Quellarchive als Artifact bereitgestellt.

Der Versions-Tag verwendet denselben wiederverwendbaren Windows-Workflow.
Der Release wird erst veröffentlicht, wenn dessen erneuter Build, Tests,
Smoke-Test und Artefaktprüfungen erfolgreich waren. Die verbindlichen Ergebnisse
für den veröffentlichten Tag stehen in GitHub Actions und im Smoke-Report des ZIPs.

## Lokale Entwicklung unter Linux

- Python 3.12.3; festgelegte Abhängigkeiten installiert.
- Vollständige Suite: **48 bestanden, 1 erwartungsgemäß übersprungen**.
  Der übersprungene Test prüft die Windows-spezifische Veröffentlichung ohne Hardlinks.
- GUI-Suite bei 150 % Anzeigeskalierung: **10 Tests bestanden**.
- `pip check`: keine widersprüchlichen Abhängigkeiten.
- Quellcode-Smoke-Test: bestanden, einschließlich Rendering, Export und GUI-Vorschau.
- Startfenster und geladener Arbeitsbereich tatsächlich aufgenommen und visuell
  geprüft; Screenshots sind in `docs/screenshots` enthalten.
- Python-Syntax und Begrenzung auf vier Funktionen/Methoden je Quelldatei geprüft.

Ein lokaler Linux-Paketversuch zeigte unvollständige Lizenzdateien der Qt-Wheels.
Dies wurde vor Veröffentlichung durch eine zusätzliche Sammlung aus den offiziellen
Qt-/PySide6-Quellen behoben und im Windows-Paket verifiziert. Ein Linux-Binärpaket
ist nicht Bestandteil dieses Windows-Releases.

## Umfang der Prüfungen

PDFs mit unterschiedlichen Seitengrößen, direkten und geerbten Rotationen sowie
Unicode-Dateinamen werden programmatisch erzeugt. Ausgaben werden erneut geöffnet
und anhand von Seiteneigenschaften und Markierungen geprüft. Tests behandeln
Originalschutz, bestehende Ausgaben, Schreibfehler, konkurrierende Dateierstellung,
Aufteilungs-Rollback, ungültige Bereiche und geschützte/beschädigte Dateien.
GUI-Tests decken Tastenkürzel, Strg-/Shift-Auswahl, tatsächlichen Mausstart des
Seitendrags, den internen Drop-Handler, Dateidrop, Kartenhöhe, Zoom und Dialogaktionen ab.

Die Windows-EXE ist nicht mit einem Code-Signing-Zertifikat signiert. Passwort-
verwaltung, dokumentweite Lesezeichenübernahme und komplexe Formulare gehören
nicht zum zugesicherten Funktionsumfang dieser Version.

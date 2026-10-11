# Implementierungsplan

1. Isolierte Python-3.12-Umgebung, festgelegte Abhängigkeiten, Lizenzprüfung.
2. Unveränderliche Seitenreferenzen, private Quellkopien, Operationen und Undo/Redo.
3. Atomarer PDF-Export, Bereichsparser, Extraktion und Aufteilung mit Tests.
4. Deutsche Qt-Oberfläche, Raster, Mehrfachauswahl, Drag & Drop, Hintergrundjobs.
5. GUI-Tests, Paket-Smoke-Test und Lizenzsammlung.
6. Windows-CI, Release-Workflow, Push und verifizierter v1.0.0-Release.

Architektur: Die Oberfläche hält nur Seitenmetadaten. Quelldokumente werden beim
Import einmal in einen privaten temporären Arbeitsbereich kopiert. Undo/Redo
speichert Tupel unveränderlicher Referenzen; PDF-Daten werden nicht dupliziert.
Export liest jede benötigte Quelle einmal. PDFium läuft ausschließlich in einem
einzelnen Hintergrundthread. Vorschaubilder werden nur für sichtbare Seiten
angefordert und begrenzt zwischengespeichert. Schreibjobs blockieren Änderungen
am Arbeitsbereich, aber nicht das Qt-Ereignissystem.

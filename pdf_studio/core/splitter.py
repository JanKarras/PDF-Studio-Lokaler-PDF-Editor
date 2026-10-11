from pathlib import Path

from .errors import StudioError
from .exporter import exportPdf, validateTarget


def splitPlan(pages, groups, folder, stem="PDF-Studio"):
    folder = Path(folder)
    plan = []
    for number, group in enumerate(groups, 1):
        if not group or any(index < 0 or index >= len(pages) for index in group):
            raise StudioError("Ungültiger Seitenbereich für die Aufteilung.")
        subset = tuple(pages[index] for index in group)
        suffix = f"Seite-{group[0] + 1:03d}" if len(group) == 1 else f"Teil-{number:02d}"
        target = folder / f"{stem}_{suffix}.pdf"
        validateTarget(subset, target)
        plan.append((subset, target))
    if len({target for _, target in plan}) != len(plan):
        raise StudioError("Die Teilbereiche erzeugen doppelte Ausgabedateien.")
    return plan


def exportSplit(plan, progress=None):
    created = []
    try:
        for index, (pages, target) in enumerate(plan):
            created.append(exportPdf(pages, target))
            if progress:
                progress(index + 1, len(plan))
        return created
    except Exception:
        for target in created:
            target.unlink(missing_ok=True)
        raise

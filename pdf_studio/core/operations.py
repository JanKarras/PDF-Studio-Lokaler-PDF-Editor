from .model import rotatedPage
from .errors import StudioError


def movePages(pages, selectedIds, destination):
    if not 0 <= destination <= len(pages):
        raise StudioError("Ungültige Einfügeposition.")
    selectedIds = set(selectedIds)
    moving = [page for page in pages if page.id in selectedIds]
    remaining = [page for page in pages if page.id not in selectedIds]
    destination -= sum(page.id in selectedIds for page in pages[:destination])
    return tuple(remaining[:destination] + moving + remaining[destination:])


def rotatePages(pages, selectedIds, degrees):
    if degrees not in (-90, 90, 180):
        raise StudioError("Nur Drehungen um 90 oder 180 Grad sind unterstützt.")
    selectedIds = set(selectedIds)
    return tuple(rotatedPage(page, degrees) if page.id in selectedIds else page for page in pages)


def deletePages(pages, selectedIds):
    selectedIds = set(selectedIds)
    return tuple(page for page in pages if page.id not in selectedIds)


def selectedPages(pages, selectedIds):
    selectedIds = set(selectedIds)
    return tuple(page for page in pages if page.id in selectedIds)

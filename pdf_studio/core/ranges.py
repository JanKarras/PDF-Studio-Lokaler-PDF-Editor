import re

from .errors import StudioError


def parseRange(expression, pageCount):
    indices = []
    for token in expression.split(","):
        match = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+)\s*)?", token)
        if not match:
            raise StudioError("Seitenbereich ungültig. Beispiel: 1, 3, 5-9")
        start = int(match[1])
        end = int(match[2] or start)
        if not 1 <= start <= end <= pageCount:
            raise StudioError(f"Seiten müssen zwischen 1 und {pageCount} liegen; Bereiche aufsteigend angeben.")
        for index in range(start - 1, end):
            if index in indices:
                raise StudioError("Ein Seitenbereich darf keine doppelten Seiten enthalten.")
            indices.append(index)
    return tuple(indices)


def parseGroups(expression, pageCount):
    groups = tuple(parseRange(part, pageCount) for part in expression.split(";"))
    flattened = [index for group in groups for index in group]
    if len(flattened) != len(set(flattened)):
        raise StudioError("Die Teilbereiche dürfen sich nicht überschneiden.")
    return groups

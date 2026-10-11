from dataclasses import dataclass, replace
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True)
class PageRef:
    id: str
    source: Path
    original: Path
    index: int
    rotation: int = 0


def createPage(source, original, index):
    return PageRef(uuid4().hex, Path(source), Path(original), index)


def rotatedPage(page, degrees):
    return replace(page, rotation=(page.rotation + degrees) % 360)

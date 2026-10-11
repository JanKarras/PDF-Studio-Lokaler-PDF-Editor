import pytest

from pdf_studio.core.errors import StudioError
from pdf_studio.core.ranges import parseRange, parseGroups


@pytest.mark.parametrize("text, expected", [("4", (3,)), ("2-8", tuple(range(1, 8))),
                         ("1, 3, 5, 9", (0, 2, 4, 8)), (" 1 - 3 , 5 ", (0, 1, 2, 4))])
def testValidRanges(text, expected):
    assert parseRange(text, 9) == expected


@pytest.mark.parametrize("text", ["", "0", "10", "3-1", "a", "1,", "1,1", "1-3,2", "-1", "1;2", "1.5", "1--2"])
def testInvalidRanges(text):
    with pytest.raises(StudioError):
        parseRange(text, 9)


def testGroups():
    assert parseGroups("1-3;4,6;5", 6) == ((0, 1, 2), (3, 5), (4,))
    with pytest.raises(StudioError):
        parseGroups("1-3;3-5", 5)

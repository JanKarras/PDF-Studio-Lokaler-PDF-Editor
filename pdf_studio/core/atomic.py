import os
from pathlib import Path


def publishNew(source, target):
    # Windows rename rejects existing destinations and also works on FAT/exFAT.
    # POSIX rename would overwrite; hard-link creation provides no-clobber there.
    if os.name == "nt":
        os.rename(source, target)
    else:
        os.link(source, target)
        Path(source).unlink()

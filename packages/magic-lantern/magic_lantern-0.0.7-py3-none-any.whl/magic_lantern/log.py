from logging import *
from logging.handlers import RotatingFileHandler

# import platform
# import os
from pathlib import Path

# set up logging to file - see previous section for more details
LONGFORMAT = (
    "%(asctime)s\t"
    "%(levelname)s\t"
    "%(filename)14s:%(lineno)s\t"
    "%(funcName)-14s\t"
    "%(message)s\t"
    # "%(name)s\t"
)
SHORTFORMAT = "%(filename)s:%(lineno)s - %(message)s"

# Root logger gets everything.  Handlers defined below will filter it out...
getLogger("").setLevel(DEBUG)

# The exifread package is very chatty for this application.  Not everything has EXIF data.
getLogger("exifread").setLevel(ERROR)


def init(filename=Path("magic-lantern.log")):
    # Not sure if this is what we want.  TBD
    # if platform.system() == "Windows":
    #     filename = Path(os.getcwd()) / filename
    # else:
    #     filename = Path("/var/log") / filename

    filehandler = RotatingFileHandler(
        filename, mode="w", maxBytes=100000, backupCount=1, encoding="utf-8"
    )
    filehandler.setLevel(DEBUG)
    filehandler.setFormatter(Formatter(LONGFORMAT))
    getLogger("").addHandler(filehandler)
    info(f"Logging to {filename.absolute()}")


# define a Handler which writes to sys.stderr
console = StreamHandler()
console.setLevel(INFO)
console.setFormatter(Formatter(SHORTFORMAT))
# add the handler to the root logger
getLogger("").addHandler(console)

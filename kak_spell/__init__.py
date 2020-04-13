from typing import Any
from .checker import Checker  # noqa: F401
import datetime


# Useful when debugging kak scripts
def log(stuff: Any) -> None:
    with open("/tmp/kak-spell.log", "a") as f:
        f.write(str(datetime.datetime.now()) + " " + str(stuff) + "\n")

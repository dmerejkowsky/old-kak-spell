import os
from typing import Any
from .checker import Checker  # noqa: F401
import datetime

# Useful when debugging kak scripts
def log(stuff: Any) -> None:
    if not os.environ.get("KAK_SPELL_DEBUG"):
        return
    with open("/tmp/kak-spell.log", "a") as f:
        f.write(str(datetime.datetime.now()) + " " + str(stuff) + "\n")

from typing import Iterator, List
import attr
import enchant
import enchant.checker
from path import Path
import xdg.BaseDirectory


@attr.s
class Error:
    path: Path = attr.ib()
    line: int = attr.ib()
    offset: int = attr.ib()
    word: str = attr.ib()


def get_pwl_path(lang: str) -> Path:
    data_path = Path(xdg.BaseDirectory.save_data_path("kak-spell"))
    data_path.makedirs_p()
    pwl_path = data_path / f"{lang}.pwl"
    if not pwl_path.exists():
        pwl_path.write_text("")
    return pwl_path


class Checker:
    def __init__(self, *, lang: str):
        self.pwl_path = get_pwl_path(lang)
        dict_with_pwl = enchant.DictWithPWL(lang, str(self.pwl_path))
        self._checker = enchant.checker.SpellChecker(lang)
        self._checker.dict = dict_with_pwl

    def check(self, path: Path) -> Iterator[Error]:
        with open(path, "r") as f:
            for lineno, line in enumerate(f, start=1):
                self._checker.set_text(line)
                for error in self._checker:
                    yield Error(path, lineno, error.wordpos + 1, error.word)

    def add(self, word: str) -> None:
        words = set(self.pwl_path.lines(retain=False))
        words.add(word)
        self.pwl_path.write_lines(sorted(words))

    def remove(self, word: str) -> None:
        words = set(self.pwl_path.lines(retain=False))
        words.discard(word)
        self.pwl_path.write_lines(sorted(words))

    def replace(self, word: str) -> List[str]:
        return self._checker.suggest(word)  # type: ignore

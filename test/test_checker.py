from typing import Any
from path import Path

from kak_spell import Checker


def test_can_find_errors(mocked_xdg: Any, tmp_path: Path) -> None:
    readme_path = tmp_path / "readme.txt"
    readme_path.write_text("this is a missstake")
    checker = Checker(lang="en_US")
    errors = list(checker.check(readme_path))
    assert len(errors) == 1
    actual = errors[0]
    assert actual.line == 1
    assert actual.offset == 11
    assert actual.word == "missstake"


def test_can_add_word_to_pwl(mocked_xdg: Any, tmp_path: Path) -> None:
    checker = Checker(lang="en_US")
    checker.add("CMake")
    expected_path = tmp_path / "share" / "kak-spell" / "en_US.pwl"
    assert expected_path.exists()
    lines = expected_path.lines(retain=False)
    assert len(lines) == 1


def test_can_remove_word_from_pwl(mocked_xdg: Any, tmp_path: Path) -> None:
    checker = Checker(lang="en_US")
    checker.add("CMake")
    expected_path = tmp_path / "share" / "kak-spell" / "en_US.pwl"
    lines = expected_path.lines(retain=False)
    assert len(lines) == 1

    checker.remove("CMake")
    expected_path = tmp_path / "share" / "kak-spell" / "en_US.pwl"
    lines = expected_path.lines(retain=False)
    assert len(lines) == 0


def test_can_replace(mocked_xdg: Any) -> None:
    checker = Checker(lang="en_US")
    replacements = checker.replace("missstake")
    print(replacements)
    assert "mistake" in replacements

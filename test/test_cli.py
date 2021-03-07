from typing import Any
import pytest
from pathlib import Path
import subprocess

import kak_spell.cli


def test_check_no_errors(tmp_path: Path) -> None:
    readme_path = tmp_path / "readme.txt"
    readme_path.write_text("No spelling errors here")
    kak_spell.cli.main(argv=["check", str(readme_path)])


def test_check_with_errors(tmp_path: Path, capsys: Any) -> None:
    readme_path = tmp_path / "readme.txt"
    readme_path.write_text(
        "No spelling errors on first line\nBut a spelling missstake here\n"
    )
    with pytest.raises(SystemExit):
        kak_spell.cli.main(argv=["check", str(readme_path)])

    ## check messages format to make sure it's kakoune compatible
    capture = capsys.readouterr()

    # kak linter plugin needs all messages on stdout
    assert not capture.err

    # kak linter plugin needs all messages on stdout
    stdout = capture.out
    messages = stdout.splitlines()
    assert len(messages) == 1
    message = messages[0]
    assert message == f"{readme_path}:2:16: error: missstake"


def test_add(tmp_path: Path, mocked_xdg: Any) -> None:
    readme_path = tmp_path / "readme.txt"
    readme_path.write_text("Talking about Kakoune here")

    kak_spell.cli.main(argv=["add", "Kakoune"])
    kak_spell.cli.main(argv=["check", str(readme_path)])


def test_remove(tmp_path: Path, mocked_xdg: Any) -> None:
    readme_path = tmp_path / "readme.txt"
    readme_path.write_text("Talking about Kakoune here")
    kak_spell.cli.main(argv=["add", "Kakoune"])
    kak_spell.cli.main(argv=["check", str(readme_path)])

    kak_spell.cli.main(argv=["remove", "Kakoune"])

    with pytest.raises(SystemExit):
        kak_spell.cli.main(argv=["check", str(readme_path)])


def test_replace_default_output(capsys: Any) -> None:
    kak_spell.cli.main(argv=["replace", "missstake"])
    capture = capsys.readouterr()
    assert not capture.err
    assert "mistake" in capture.out


def test_replace_kakoune_output(capsys: Any) -> None:
    kak_spell.cli.main(argv=["replace", "missstake", "--kakoune"])
    capture = capsys.readouterr()
    assert not capture.err
    assert "mistake" in capture.out

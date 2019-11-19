import pytest
from path import Path
import subprocess
import xdg.BaseDirectory

import kak_spell.cli


def test_check_no_errors(tmp_path):
    readme_path = tmp_path / "readme.txt"
    readme_path.write_text("No spelling errors here")
    kak_spell.cli.main(argv=["check", readme_path])


def test_check_with_errors(tmp_path, capsys):
    readme_path = tmp_path / "readme.txt"
    readme_path.write_text(
        "No spelling errors on first line\nBut a spelling missstake here\n"
    )
    with pytest.raises(SystemExit):
        kak_spell.cli.main(argv=["check", readme_path])

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


@pytest.fixture
def mocked_xdg(mocker, tmp_path):
    data_path_mock = mocker.patch("xdg.BaseDirectory.save_data_path")
    data_path_mock.side_effect = lambda name: tmp_path / "share" / name


def test_add(tmp_path, mocked_xdg):
    readme_path = tmp_path / "readme.txt"
    readme_path.write_text("Talking about Kakoune here")

    kak_spell.cli.main(argv=["add", "Kakoune"])
    kak_spell.cli.main(argv=["check", readme_path])


def test_remove(tmp_path, mocked_xdg):
    readme_path = tmp_path / "readme.txt"
    readme_path.write_text("Talking about Kakoune here")
    kak_spell.cli.main(argv=["add", "Kakoune"])
    kak_spell.cli.main(argv=["check", readme_path])

    kak_spell.cli.main(argv=["remove", "Kakoune"])

    with pytest.raises(SystemExit):
        kak_spell.cli.main(argv=["check", readme_path])


def test_replace_default_output(capsys):
    suggestions = kak_spell.cli.main(argv=["replace", "missstake"])
    capture = capsys.readouterr()
    assert not capture.err
    assert "mistake" in capture.out

from typing import Any, List
from path import Path
from kak_spell.checker import Error
from kak_spell.kak import (
    convert_to_pos,
    convert_ranges,
    error_to_range,
    get_next_selection,
    get_previous_selection,
    goto_and_select,
    goto_next,
    menu_from_replacements,
    Range,
)


def test_error_to_range_en() -> None:
    error = Error(Path("foo.txt"), 2, 1, "missstake", "this is a missstake, yo")
    assert error_to_range(error) == (2, 2, 9)


def test_error_to_range_fr_adjust_length() -> None:
    error = Error(Path("foo.txt"), 2, 4, "cafée", "le cafée est chaud")
    assert error_to_range(error) == (2, 5, 6)


def test_error_to_range_fr_adjust_offset() -> None:
    error = Error(Path("foo.txt"), 2, 13, "froidd", "le café est froidd")
    assert error_to_range(error) == (2, 15, 6)


def test_convert_to_pos_option() -> None:
    assert convert_to_pos("1.1") == (1, 1)


def test_convert_ranges_option() -> None:
    option = "1 1.21,1.30|Error 2.19,2.27|Error"
    assert convert_ranges(option) == [(1, 21, 30), (2, 19, 27)]


def test_goto_next_no_errors(capsys: Any) -> None:
    pos = "1.1"
    ranges = "5 "
    goto_next(pos, ranges)
    capture = capsys.readouterr()
    assert "no spelling errors" in capture.out


def test_get_next_selection_same_line_after_cursor() -> None:
    pos = (1, 1)
    ranges = [(1, 21, 30), (2, 19, 27)]
    assert get_next_selection(pos, ranges) == (1, 21, 30)


def test_get_next_selection_same_line_before_cursor() -> None:
    pos = (1, 15)
    ranges = [(1, 10, 14), (2, 19, 27)]
    assert get_next_selection(pos, ranges) == (2, 19, 27)


def test_get_next_selection_same_line_same_cursor() -> None:
    # Scenario: the cursor is at the end of the spell error -
    # we want to go to the next error, not stay where we are!
    pos = (1, 14)
    ranges = [(1, 10, 14), (2, 19, 27)]
    assert get_next_selection(pos, ranges) == (2, 19, 27)


def test_get_next_selection_end_of_buffer() -> None:
    pos = (3, 4)
    ranges = [(1, 10, 14), (2, 19, 27)]
    assert get_next_selection(pos, ranges) == (1, 10, 14)


def test_goto_and_select(capsys: Any) -> None:
    goto_and_select((2, 4, 9))
    capture = capsys.readouterr()

    assert not capture.err
    assert capture.out == "select 2.4,2.9\n"


def test_replace_no_suggestion(capsys: Any) -> None:
    menu_from_replacements([])
    capture = capsys.readouterr()

    assert not capture.err
    assert capture.out == "fail no suggestions\n"


def test_get_previous_selection_same_line_after_cursor() -> None:
    pos = (1, 21)
    ranges = [(1, 12, 19), (2, 19, 27)]
    assert get_previous_selection(pos, ranges) == (1, 12, 19)


def test_get_previous_selection_same_line_before_cursor() -> None:
    pos = (1, 15)
    ranges = [(1, 3, 12), (2, 19, 27)]
    assert get_previous_selection(pos, ranges) == (1, 3, 12)


def test_get_previous_selection_same_line_same_cursor() -> None:
    # Scenario: the cursor is at the end of the spell error -
    # we want to go to the previous error, not stay where we are!
    pos = (2, 19)
    ranges = [(1, 10, 14), (2, 19, 27)]
    assert get_previous_selection(pos, ranges) == (1, 10, 14)

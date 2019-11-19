#!/usr/bin/env python3
from typing import List, Optional
import argparse
import sys

import enchant
import enchant.checker
from path import Path
import xdg.BaseDirectory


def get_pwl_path(lang: str) -> Path:
    data_path = Path(xdg.BaseDirectory.save_data_path("kak-spell"))
    data_path.makedirs_p()
    pwl_path = data_path / f"{lang}.pwl"
    if not pwl_path.exists():
        pwl_path.write_text("")
    return pwl_path


def add_word(word: str, *, lang: str) -> None:
    pwl_path = get_pwl_path(lang)
    words = set(pwl_path.lines(retain=False))
    words.add(word)
    pwl_path.write_lines(sorted(words))
    print("Word added to", pwl_path)


def remove_word(word: str, *, lang: str) -> None:
    pwl_path = get_pwl_path(lang)
    words = set(pwl_path.lines(retain=False))
    words.discard(word)
    pwl_path.write_lines(sorted(words))


def check(path: Path, *, lang: str) -> bool:
    pwl_path = get_pwl_path(lang)
    dict_with_pwl = enchant.DictWithPWL(lang, str(pwl_path))
    checker = enchant.checker.SpellChecker(lang)
    checker.dict = dict_with_pwl
    ok  = True
    with open(path, "r") as f:
        for lineno, line in enumerate(f, start=1):
            checker.set_text(line)
            for error in checker:
                ok = False
                print(f"{path}:{lineno}:{error.wordpos+1}: error: {error.word}")
    return ok


def kak_menu_from_suggestions(suggestions: List[str]) -> str:
    menu = ""
    for entry in suggestions:
        # Note: %{...} is kakoune way of grouping stuff that may - or not
        # contains quotes, which prevents us from using `%`, `.format()` or
        # f-strings :P
        menu_entry = "%{ENTRY} %{execute-keys -itersel %{cENTRY<esc>be}}"
        menu_entry = menu_entry.replace("ENTRY", entry)
        menu += " " + menu_entry
    return "menu " + menu


def replace(word: str, *, lang: str, kak_output: bool) -> None:
    pwl_path = get_pwl_path(lang)
    dict_with_pwl = enchant.DictWithPWL(lang, str(pwl_path))
    suggestions = dict_with_pwl.suggest(word)
    if kak_output:
        menu = kak_menu_from_suggestions(suggestions)
        print(menu)
    else:
        print(" ".join(suggestions))


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", default="en_US")

    subparsers = parser.add_subparsers(title="commands", dest="command")

    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("path")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("word")

    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("word")

    replace_parser = subparsers.add_parser("replace")
    replace_parser.add_argument(
        "--kakoune", action="store_true", help="Output kak-script compatible output"
    )
    replace_parser.add_argument("word")

    args = parser.parse_args(args=argv)
    lang = args.lang

    if args.command == "add":
        word = args.word
        add_word(word, lang=lang)
    elif args.command == "remove":
        word = args.word
        remove_word(word, lang=lang)
    elif args.command == "check":
        path = args.path
        ok = check(path, lang=lang)
        if not ok:
            sys.exit(1)
    elif args.command == "replace":
        word = args.word
        kakoune = args.kakoune
        replace(word, lang=lang, kak_output=kakoune)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

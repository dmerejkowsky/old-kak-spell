#!/usr/bin/env python3
import argparse
import sys

import enchant
import enchant.checker
from path import Path
import xdg.BaseDirectory


def get_pwl_path(lang):
    data_path = Path(xdg.BaseDirectory.save_data_path("kak-spell"))
    data_path.makedirs_p()
    pwl_path = data_path / f"{lang}.pwl"
    if not pwl_path.exists():
        pwl_path.write_text("")
    return pwl_path


def add_word(word, *, lang):
    pwl_path = get_pwl_path(lang)
    words = set(pwl_path.lines(retain=False))
    words.add(word)
    pwl_path.write_lines(sorted(words))


def remove_word(word, *, lang):
    pwl_path = get_pwl_path(lang)
    words = set(pwl_path.lines(retain=False))
    words.discard(word)
    pwl_path.write_lines(sorted(words))


def check(path, *, lang):
    pwl_path = get_pwl_path(lang)
    dict_with_pwl = enchant.DictWithPWL(lang, str(pwl_path))
    checker = enchant.checker.SpellChecker(lang)
    checker.dict = dict_with_pwl
    with open(path, "r") as f:
        for lineno, line in enumerate(f, start=1):
            checker.set_text(line)
            for error in checker:
                print(f"{path}:{lineno}:{error.wordpos+1}: error: {error.word}")


def kak_menu_from_suggestions(suggestions):
    menu = ""
    for entry in suggestions:
        # Note: %{...} is kakoune way of grouping stuff that may - or not
        # contains quotes, which prevents us from using `%`, `.format()` or
        # f-strings :P
        menu_entry = "%{ENTRY} %{execute-keys -itersel %{cENTRY<esc>be}}"
        menu_entry = menu_entry.replace("ENTRY", entry)
        menu += " " + menu_entry
    return "menu " + menu


def replace(word, *, lang, kak_output):
    pwl_path = get_pwl_path(lang)
    dict_with_pwl = enchant.DictWithPWL(lang, str(pwl_path))
    suggestions = dict_with_pwl.suggest(word)
    if kak_output:
        menu = kak_menu_from_suggestions(suggestions)
        print(menu)
    else:
        print(" ".join(suggestions))


def main():
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

    args = parser.parse_args()
    lang = args.lang

    if args.command == "add":
        word = args.word
        add_word(word, lang=lang)
    elif args.command == "remove":
        word = args.word
        remove_word(word, lang=lang)
    elif args.command == "check":
        path = args.path
        check(path, lang=lang)
    elif args.command == "replace":
        word = args.word
        kakoune = args.kakoune
        replace(word, lang=lang, kak_output=kakoune)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

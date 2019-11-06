#!/usr/bin/env python3
import argparse
import sys

import enchant
from path import Path
import xdg.BaseDirectory


def get_personal_dict_path(lang):
    # Remove this
    data_path = Path(xdg.BaseDirectory.save_data_path("kak-spell"))
    data_path.makedirs_p()
    personnal_word_list_path = data_path / f"{lang}.pwl"
    if not personnal_word_list_path.exists():
        personnal_word_list_path.write_text("")
    return personnal_word_list_path


def add_word(word, *, lang):
    # use the add() method of the checker directly :)
    personnal_path = get_personal_dict_path(lang)
    lines = personnal_path.lines(retain=False)
    if word not in lines:
        lines.append(word)
    personnal_path.write_lines(lines)


def remove_word():
    # how to implement remove?
    pass


def check(path, *, lang):
    personnal_path = get_personal_dict_path(lang)
    # use spell checker
    checker = enchant.DictWithPWL(lang, str(personnal_path))
    with open(path, "r") as f:
        for lineno, line in enumerate(f, start=1):
            checker.set_text(line)
            for error in checker:
                print(f"{path}:{lineno}:{error.wordpos+1}: error: {error.word}")


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
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

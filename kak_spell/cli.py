#!/usr/bin/env python3
from typing import List, Optional
import argparse
import sys

from path import Path

from .checker import Checker
from . import kak
from . import log


def add_word(word: str, *, lang: str) -> None:
    checker = Checker(lang=lang)
    checker.add(word)
    print("Word added to", checker.pwl_path)


def remove_word(word: str, *, lang: str) -> None:
    checker = Checker(lang=lang)
    checker.remove(word)
    print("Word removed from", checker.pwl_path)


def check(
    path: Path,
    *,
    lang: str,
    filetype: Optional[str] = None,
    kakoune: bool = False,
    kak_timestamp: int = 0,
) -> bool:
    checker = Checker(lang=lang)
    errors = checker.check(path, filetype=filetype)
    if kakoune:
        kak.set_spell_errors(errors, timestamp=kak_timestamp)
        return True
    else:
        ok = True
        for error in errors:
            ok = False
            print(f"{path}:{error.lineno}:{error.offset + 1}: error: {error.word}")
    return ok


def replace(word: str, *, lang: str, kak_output: bool) -> None:
    checker = Checker(lang=lang)
    replacements = checker.replace(word)
    if kak_output:
        kak.menu_from_replacements(replacements)
    else:
        print(" ".join(replacements))


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", default="en_US")

    subparsers = parser.add_subparsers(title="commands", dest="command")

    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("path", type=Path)
    check_parser.add_argument(
        "--filetype", help="file type, as set by kakoune in $kak_opt_filetype"
    )
    check_parser.add_argument(
        "--kakoune", help="output kakoune commands", action="store_true"
    )
    check_parser.add_argument("--kak-timestamp", help="kakoune timestamp", type=int)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("path", type=Path)
    list_parser.add_argument(
        "--filetype", help="file type, as set by kakoune in $kak_opt_filetype"
    )

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("word")

    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("word")

    replace_parser = subparsers.add_parser("replace")
    replace_parser.add_argument(
        "--kakoune", action="store_true", help="Output kak-script compatible output"
    )
    replace_parser.add_argument("word")

    next_parser = subparsers.add_parser("next")
    next_parser.add_argument("--ranges", help="kakoune ranges", required=True)
    next_parser.add_argument("--pos", help="kakoune cursor pos", required=True)

    previous_parser = subparsers.add_parser("previous")
    previous_parser.add_argument("--ranges", help="kakoune ranges", required=True)
    previous_parser.add_argument("--pos", help="kakoune cursor pos", required=True)

    args = parser.parse_args(args=argv)
    log(args)
    lang = args.lang

    if args.command == "add":
        word = args.word
        add_word(word, lang=lang)
    elif args.command == "remove":
        word = args.word
        remove_word(word, lang=lang)
    elif args.command == "check":
        ok = check(
            args.path,
            lang=lang,
            filetype=args.filetype,
            kakoune=args.kakoune,
            kak_timestamp=args.kak_timestamp,
        )
        if not ok:
            sys.exit(1)
    elif args.command == "list":
        kak.list(args.path, lang=lang, filetype=args.filetype)
    elif args.command == "replace":
        word = args.word
        kakoune = args.kakoune
        replace(word, lang=lang, kak_output=kakoune)
    elif args.command == "next":
        kak.goto_next(args.pos, args.ranges)
    elif args.command == "previous":
        kak.goto_previous(args.pos, args.ranges)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

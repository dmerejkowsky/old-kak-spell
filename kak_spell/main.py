#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess

from enchant.checker import SpellChecker


def add_word():
    pass


def remove_word():
    pass


def check(path):
    checker = SpellChecker("en_US")
    with open(path, "r") as f:
        for lineno, line in enumerate(f, start=1):
            checker.set_text(line)
            for error in checker:
                print(f"{path}:{lineno}:{error.wordpos+1}: error: {error.word}")


def main():
    parser = argparse.ArgumentParser()
    # TODO
    parser.add_argument("--lang", default="en_US")

    subparsers = parser.add_subparsers(title="commands", dest="command")

    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("path")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("word")

    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("word")

    args = parser.parse_args()

    if args.command == "add":
        word = args.word
        add_word(word)
    elif args.command == "remove":
        word = args.word
        remove_word(word)
    elif args.command == "check":
        path = args.path
        check(path)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

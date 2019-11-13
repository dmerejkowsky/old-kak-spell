#!/usr/bin/env python3
import argparse
import sys
import os
import socketserver
import socket

import daemon
import enchant
import enchant.checker
from path import Path
import xdg.BaseDirectory

SOCKET_PATH = Path("/tmp/kak-spell")

# TODO: need a 'real' protocol json-rpc like
# so we know if commands are successful or not


def get_pwl_path(lang):
    data_path = Path(xdg.BaseDirectory.save_data_path("kak-spell"))
    data_path.makedirs_p()
    pwl_path = data_path / f"{lang}.pwl"
    if not pwl_path.exists():
        pwl_path.write_text("")
    return pwl_path


def get_server_log_path():
    data_path = Path(xdg.BaseDirectory.save_data_path("kak-spell"))
    data_path.makedirs_p()
    log_path = data_path / "server.log"
    log_path.write_text("")
    return log_path


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


def get_checker():
    pwl_path = get_pwl_path(lang)
    dict_with_pwl = enchant.DictWithPWL(lang, str(pwl_path))
    checker = enchant.checker.SpellChecker(lang)
    checker.dict = dict_with_pwl
    return checker


def check(checker, path):
    message = ""
    errors = []
    with open(path, "r") as f:
        for lineno, line in enumerate(f, start=1):
            checker.set_text(line)
            for error in checker:
                errors.append(error)
                message += f"{path}:{lineno}:{error.wordpos+1}: error: {error.word}\n"
    return (not errors), message


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
        return True, menu
    else:
        message = " ".join(suggestions)
        return True, message


class KakServerRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.parser = configure_parser(with_server_commands=False)
        # TODO: need a check per lang ...
        self.checker = ...

    def handle(self):
        data = self.request.recv(1024)
        as_string = data.decode()
        cmd = as_string.split(" ")
        try:
            args = self.parser.parse_args(cmd)
            _, response = run(args)
        except SystemError:
            response = b"Could not parse arguments"
        except Exception as e:
            response = str(e)
        self.request.sendall(response.encode())


class ThreadedStreamServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    pass


def start_server():
    # Todo : import daemon
    try:
        with ThreadedStreamServer(SOCKET_PATH, KakServerRequestHandler) as s:
            s.serve_forever()
    except KeyboardInterrupt:
        pass
    SOCKET_PATH.remove_p()


def stop_server():
    pass
    # TODO!


def configure_parser(*, with_server_commands):
    # If not called by a script start-server and stop-server
    # are not available
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", default="en_US")
    parser.add_argument("--client", action="store_true")

    subparsers = parser.add_subparsers(title="commands", dest="command")

    if with_server_commands:
        subparsers.add_parser("start-server")
        subparsers.add_parser("stop-server")

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
    return parser


def send_request(argv):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(SOCKET_PATH)
        s.send(" ".join(argv).encode())
        response = s.recv(1024)
        return response


def run(args):
    lang = args.lang
    if args.command == "start-server":
        start_server()
        return True, ""
    if args.command == "stop-server":
        stop_server()
        return True, ""
    elif args.command == "add":
        word = args.word
        add_word(word, lang=lang)
        return True, f"added word: {word}"
    elif args.command == "remove":
        word = args.word
        remove_word(word, lang=lang)
        return True, f"remove word: f{word}"
    elif args.command == "check":
        path = args.path
        return check(path, lang=lang)
    elif args.command == "replace":
        word = args.word
        kakoune = args.kakoune
        message = replace(word, lang=lang, kak_output=kakoune)
        return True, message
    else:
        return False, f"no such command {args.command}"


def main(argv=None):
    # Called directly by a script
    if not argv:
        argv = sys.argv[1:]
    parser = configure_parser(with_server_commands=True)
    args = parser.parse_args(args=argv)
    if args.client:
        response = send_request(argv).decode()
        ok = True
    else:
        ok, response = run(args)
    print(response, end="")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()

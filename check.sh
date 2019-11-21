#/bin/bash
set -x
set -e

flake8 kak_spell
mypy kak_spell test/
pytest

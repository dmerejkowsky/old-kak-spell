#/bin/bash
set -x
set -e

poetry run flake8 kak_spell
poetry run mypy kak_spell test/
poetry run pytest

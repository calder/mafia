#!/bin/sh -e

# Colors
RED="$(tput setaf 1)"
GREEN="$(tput setaf 2)"
RESET="$(tput sgr0)"

cd "$(dirname "$0")/.."

pytest

scripts/make_role_page.py | colordiff doc/roles.md - \
  || { echo "\n${RED}ERROR${RESET}: doc/roles.md is out of date. Run\n  scripts/make_role_page.py > doc/roles.md\nto update it."; exit 1; }

echo
! grep -r "print(" mafia/*.py mafia/*/*.py \
  --exclude=mafia/util.py \
  --exclude=mafia/test/util.py \
  --exclude=mafia/test/readme_test.py \
  || { echo "\n${RED}ERROR${RESET}: Remove leftover print statements before committing."; exit 1; }

echo
! grep -r "debug=True" mafia/*.py \
  --exclude=mafia/util.py \
  || { echo "\n${RED}ERROR${RESET}: Remove leftover 'debug=True's before committing."; exit 1; }

echo "Presubmits ${GREEN}PASSED${RESET}.\n"

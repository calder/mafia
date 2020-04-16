#!/bin/sh -e

cd "$(dirname "$0")/../.git"

mv hooks "hooks_$(date '+%Y-%m-%d_%H:%M:%S')"
ln -s ../scripts/git_hooks hooks

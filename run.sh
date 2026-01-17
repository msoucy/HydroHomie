#!/bin/sh

cd "$(dirname "${BASH_SOURCE[0]}")"
uv run ./main.py "$@"

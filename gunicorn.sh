#!/usr/bin/env bash

set -o errexit
set -o nounset

/usr/local/bin/gunicorn wsgi:app -w 4 -b 0.0.0.0:8000 --chdir=/code/server --reload

#!/bin/sh

set -e

/app/.venv/bin/alembic upgrade head
exec /app/.venv/bin/python /app/src/main.py

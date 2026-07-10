#!/usr/bin/env bash


set -e
echo "Fill database"
python /var/app/fill_db.py
echo "Fill database done"

exec "$@"
#!/bin/sh

echo "Execute generators"
python3 generators/dirmaker.py
python3 generators/imagemaker.py
python3 generators/partymaker.py

echo "Build frontend"
./build_frontend.sh

echo "Apply database migration"
python3 src/manage.py migrate --noinput

echo "Starting server"
python3 src/manage.py runserver 0.0.0.0:8000

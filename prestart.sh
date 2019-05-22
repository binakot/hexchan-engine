#!/bin/sh

set -e

echo "Waiting for database..."
until PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -c '\q'; do
    sleep 5
done

echo "Create directories"
python3 generators/dirmaker.py

echo "Apply database migration"
python3 src/manage.py migrate --noinput

echo "Make captcha"
python3 src/manage.py makecaptchas 1024

echo "Build frontend"
./build_frontend.sh

if [ $FAKE_CONTENT = "True" ]; then
    echo "Generate fake content (optional)"
    python3 generators/imagemaker.py .
    python3 generators/partymaker.py
    python3 src/manage.py loaddata boards threads posts images
fi

if [ $DEBUG != "True" ]; then
    echo "Collect static (optional)"
    python3 src/manage.py collectstatic --noinput
fi

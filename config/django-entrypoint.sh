#!/usr/bin/env bash

python /app/wait_for_postgres.py
cd /app/src

python manage.py migrate
python manage.py initadmin
python manage.py loaddata ./fixtures/categories.json
python manage.py loaddata ./fixtures/products.json

gunicorn online_shop.wsgi -b 0.0.0.0:8000 --reload

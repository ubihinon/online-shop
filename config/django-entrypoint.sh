#!/usr/bin/env bash

python /app/wait_for_postgres.py
cd /app/src

python manage.py migrate
python manage.py initadmin

gunicorn online_shop.wsgi -b 0.0.0.0:8000 --reload

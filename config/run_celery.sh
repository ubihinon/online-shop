#!/usr/bin/env bash

cd /app/src
su -m online_shop -c "celery worker -A online_shop.celery --loglevel=info -Q default -n default@%h -B"

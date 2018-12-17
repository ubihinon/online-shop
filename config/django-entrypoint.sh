#!/usr/bin/env bash

gunicorn chat.wsgi -b 0.0.0.0:8000 --reload

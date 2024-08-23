#!/bin/sh
# python manage.py collectstatic --noinput --clear
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
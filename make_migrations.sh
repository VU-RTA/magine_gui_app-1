#!/usr/bin/env bash
python manage.py makemigrations
python manage.py makemigrations gui
python manage.py migrate


#!/usr/bin/env bash
source activate magine_36
export PYTHONPATH=/run/media/pinojc/SharedData/PycharmProjects/PycharmProjects/Magine/:$PYTHONPATH
python manage.py makemigrations
python manage.py makemigrations gui
python manage.py migrate


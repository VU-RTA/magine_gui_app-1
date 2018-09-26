#!/usr/bin/env bash
source activate magine_36
export PYTHONPATH=`pwd`/Magine/:$PYTHONPATH
export PYTHONPATH=../RTA/magine_scripts:$PYTHONPATH
python manage.py makemigrations
python manage.py makemigrations gui
python manage.py migrate


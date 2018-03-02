#!/usr/bin/env bash
export PYTHONPATH=`pwd`/Magine/:$PYTHONPATH
./make_migrations.sh
python test_data/add_test_data.py


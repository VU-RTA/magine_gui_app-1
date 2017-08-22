export PYTHONPATH=`pwd`/Magine/:$PYTHONPATH
./make_migrations.sh
python gui/test_data/add_test_data.py


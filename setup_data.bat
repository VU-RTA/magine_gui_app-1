@ECHO OFF
setlocal
make_migrations.bat
set PYTHONPATH=C:\Users\James Pino\PycharmProjects\Magine;%PYTHONPATH%
python gui/test_data/add_test_data.py
endlocal


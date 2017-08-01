@ECHO OFF
setlocal
set PYTHONPATH=C:\Users\James Pino\PycharmProjects\Magine;%PYTHONPATH%
python manage.py makemigrations
python manage.py migrate
endlocal
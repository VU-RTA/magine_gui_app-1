@ECHO OFF
setlocal
set PYTHONPATH=C:\Users\james\PycharmProjects\Magine;%PYTHONPATH%
python manage.py makemigrations
python manage.py makemigrations gui
python manage.py migrate
endlocal
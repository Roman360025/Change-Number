#python create_table.py

python manage.py makemigrations main
python manage.py migrate main



gunicorn achievement2.wsgi:application --bind 0.0.0.0:8000 --log-level info --timeout 180  --workers 3
#python manage.py runserver
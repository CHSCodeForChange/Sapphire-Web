release: python manage.py migrate --no-input --settings=sapphire.production
web: gunicorn sapphire.wsgi --log-file -

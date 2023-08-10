#!/bin/bash
python manage.py migrate &
python manage.py add_user &
python manage.py runserver 0.0.0.0:8000 


#!/bin/bash

# Запуск локального сервера Django для music25

export DJANGO_SETTINGS_MODULE=soundcloud.settings
export PYTHONUNBUFFERED=1

python3 manage.py migrate
python3 manage.py runserver 8001

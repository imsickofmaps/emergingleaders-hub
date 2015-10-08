#!/bin/sh
export DATABASE_URL='postgres://postgres:@/test_emergingleaders_hub'
export DJANGO_SETTINGS_MODULE="emergingleaders_hub.testsettings"
./manage.py test "$@"

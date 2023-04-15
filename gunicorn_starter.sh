#!/bin/sh

gunicorn -b 0.0.0.0:5000 --log-level error --error-logfile - --access-logfile -  app.wsgi:app

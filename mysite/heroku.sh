#!/bin/bash

echo "starting django app"
gunicorn mysite.wsgi --log-file -
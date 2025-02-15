#!/bin/bash

sleep 10
flask db migrate
flask db upgrade
waitress-serve --port 5000 --call 'repmate:create_app'

tail -f /dev/null

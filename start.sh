#!/bin/bash

if [ "$1" == "systemd" ]; then
    systemctl --user ${2:-start} verenluovutus
fi

source venv/bin/activate
source ./.env
flask run --host=$HOST --port=$PORT

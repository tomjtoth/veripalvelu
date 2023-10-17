#!/bin/bash

APP_NAME="verenluovutus-sovellus"

if [ "$1" == "systemd" ]; then
    systemctl --user $2 "$APP_NAME"
elif [ "$1" == "update" ]; then
    git fetch origin
    if $(git pull | grep -q '^Updating'); then
        systemctl --user daemon-reload
        systemctl --user restart "$APP_NAME"
    fi
elif [ "$1" == "resetdb" ]; then
    sudo -u postgres dropdb $APP_NAME
    sudo -u postgres createdb -O $USER $APP_NAME
else
    if [ ! -d "./venv" ]; then
        python3 -m venv venv
        . venv/bin/activate
        pip install -r requirements.txt
    else
        . venv/bin/activate
    fi
    [ -f ".env" ] && . .env
    flask run \
        ${HOST:+--host=$HOST} \
        ${PORT:+--port=$PORT} \
        ${TLS_CERT:+--cert=$TLS_CERT} \
        ${TLS_KEY:+--key=$TLS_CERT}
    
    #gunicorn -b $HOST:$PORT --keyfile $TLS_KEY --certfile $TLS_CERT 'app:app'
fi

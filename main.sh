#!/bin/bash

SERVICE="verenluovutus-sovellus"

if [ "$1" == "systemd" ]; then
    systemctl --user $2 "$SERVICE"
elif [ "$1" == "update" ]; then
    git fetch origin
    if $(git pull | grep -q '^Updating'); then
        systemctl --user daemon-reload
        systemctl --user restart "$SERVICE"
    fi
else
    [ -f ".env" ] && . .env
    flask run \
        ${HOST:+--host=$HOST} \
        ${PORT:+--port=$PORT} \
        ${TLS_CERT:+--cert=$TLS_CERT} \
        ${TLS_KEY:+--key=$TLS_CERT}
    
    #gunicorn -b $HOST:$PORT --keyfile $TLS_KEY --certfile $TLS_CERT 'app:app'
fi

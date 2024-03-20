#!/bin/sh

PG_PASS=$(uuidgen)
PG_USER=vp
PG_DB=vp

echo "\
# This file is now used by both the app and docker-compose.yml
FLASK_SECRET_KEY=$(uuidgen)
APP_PORT=8080

# connection to v12.5 via local socket, name should be adjusted
DATABASE_URL=postgresql+psycopg2:///${USER}

# connection via 'dialect+driver://username:password@host[:port]/database'
DATABASE_URL=postgresql+psycopg2://${PG_USER}:${PG_PASS}@db/${PG_DB}

# postgres needs these (docker-compose.yml)
POSTGRES_PASSWORD=${PG_PASS}
POSTGRES_USER=${PG_USER}
POSTGRES_DB=${PG_DB}
" > .env

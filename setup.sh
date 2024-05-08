#!/bin/sh

# if uuidgen does not exist, implement something similar
if [ -z "$(which uuidgen)" ]; then
  uuidgen () {
    tr -dc A-Za-z0-9 < /dev/urandom | head -c 40; echo
  }  
fi

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

# same as above, only connecting to the PG instance launched by docker compose up
# provided you uncommented publishing the port in /docker-compose.yml
# DATABASE_URL=postgresql+psycopg2://${PG_USER}:${PG_PASS}@localhost/${PG_DB}

# postgres needs these (docker-compose.yml)
POSTGRES_PASSWORD=${PG_PASS}
POSTGRES_USER=${PG_USER}
POSTGRES_DB=${PG_DB}
POSTGRES_DATA=./pg_data
" > .env

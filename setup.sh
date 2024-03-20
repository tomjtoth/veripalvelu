#!/bin/sh

POSTGRES_PASSWORD=$(uuidgen)

echo \
"FLASK_SECRET_KEY=$(uuidgen)

# connection via local socket, name should be adjusted
DATABASE_URL=postgresql+psycopg2:///local-database-name

# connection via 'dialect+driver://username:password@host[:port]/database'
DATABASE_URL=postgresql+psycopg2://vp:${POSTGRES_PASSWORD}@db/vp

# postgres needs these (docker-compose.yml)
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_USER=vp
POSTGRES_DB=vp
" > .env

echo ".env created with new UUIDs"

docker-compose up $@

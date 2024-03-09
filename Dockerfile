# syntax=docker/dockerfile:1

FROM postgres:16.2-alpine

RUN mkdir -p /var/{lib,run}/postgresql/ && chown postgres:postgres /var/{lib,run}/postgresql/
USER postgres
ENV POSTGRES_HOST_AUTH_METHOD=trust
ENV PGUSER=postgres
RUN docker-entrypoint.sh

USER root

WORKDIR /usr/src/app/
VOLUME $WORKDIR/.env

COPY . .

RUN apk add --no-cache python3 py3-pip
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt

ENTRYPOINT docker-entrypoint.sh postgres & sleep 3 && \
    flask run \
    ${HOST:+--host=$HOST} \
    ${PORT:+--port=$PORT} \
    ${TLS_CERT:+--cert=$TLS_CERT} \
    ${TLS_KEY:+--key=$TLS_KEY}

FROM python:3.12-alpine3.19

WORKDIR /usr/src/app

# utilizing build caches since ./requirements.txt doesn't change "often"
COPY ./requirements.txt .

ENV \
    VIRTUAL_ENV=/opt/venv \
    PATH="$VIRTUAL_ENV/bin:$PATH"

RUN \
    # building packages via `pip install` takes 10s of seconds
    python3 -m venv $VIRTUAL_ENV && \
    pip install -r requirements.txt && \
    # add the non-root user
    adduser --no-create-home --disabled-password --gecos "" vp

# copy over the more frequently changing /src/
COPY ./src/ .

USER vp

ENTRYPOINT \
    # generate random data if not done so previously
    GEN_RAND_DATA=1 flask run && \
    # start serving with 4 worker threads
    unset GEN_RAND_DATA && gunicorn -w 4 -b 0.0.0.0:80 app:app

EXPOSE 80

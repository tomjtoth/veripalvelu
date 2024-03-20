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

# copy over the rapidly changing /src/
COPY . .

USER vp

# 4 worker threads trigger the population of fake data 3x
# ENTRYPOINT gunicorn -w 4 -b 0.0.0.0:80 app:app
ENTRYPOINT gunicorn -b 0.0.0.0:80 app:app

EXPOSE 80

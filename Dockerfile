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
    # create the .env file and make it readable for others
    touch .env && chmod o+r .env && \
    # add the non-root user
    adduser --no-create-home --disabled-password --gecos "" veripalvelu

# copy over the rapidly changing /src/
COPY . .

USER veripalvelu

# ENTRYPOINT flask run --host=0.0.0.0 --port=80
ENTRYPOINT gunicorn --bind 0.0.0.0:80 app:app

EXPOSE 80

FROM python:3.12-alpine3.19

WORKDIR /usr/src/app/

COPY ./requirements.txt .
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt

# the above block takes long, requirements don't change as often as the /src/
VOLUME .env
COPY . .

RUN adduser --no-create-home --disabled-password --gecos "" veripalvelu
RUN chown veripalvelu:veripalvelu .
USER veripalvelu

RUN CREATE_DOTENV=true python3 app.py

ENTRYPOINT gunicorn --bind 0.0.0.0 app:app

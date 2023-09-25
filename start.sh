#!/bin/bash

source venv/bin/activate
source ./.env
flask run --host=$HOST --port=$PORT

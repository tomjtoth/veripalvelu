#!/bin/bash

source ./.env

flask run --host=$HOST --port=$PORT

#!/usr/bin/env bash

echo "################"
echo 'insuring setup...'
./lsetup.sh
echo 'activating virtual env...'
. venv/bin/activate
echo "ready to start..."
echo "starting your flask app..."
python app.py
echo "################"

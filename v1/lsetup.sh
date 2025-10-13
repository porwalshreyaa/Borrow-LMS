#!/usr/bin/env bash

echo "################"
if [ -d "venv" ];
then
    echo "venv exists, installing req..."
else
    echo "creting venv..."
    python3 -m venv venv
    echo "installing req"
fi

. venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
echo "installation complete"
deactivate
echo "done!"
echo "################"

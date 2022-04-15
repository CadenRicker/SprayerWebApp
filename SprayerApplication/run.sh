#!/bin/bash
sudo service mysql start
python3 Test_SupportFunctionsSQL.py -v
export FLASK_ENV=development
export FLASK_APP=app
flask run
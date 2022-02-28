#!/bin/bash
sudo service mysql start
export FLASK_ENV=development
export FLASK_APP=app
flask run
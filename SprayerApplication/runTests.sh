#!/bin/bash
sudo service mysql start
python3 Test_SupportFunctions.py
python3 Test_SupportFunctionsSQL.py
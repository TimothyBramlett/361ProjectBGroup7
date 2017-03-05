#!/bin/bash

python ./db_api/sqlite_init.py
python ./db_api/app_test.py > app_test.report
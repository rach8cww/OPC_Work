#! /bin/bash

./copy $@
ssh pi -A "python3 main.py"
#! /bin/bash

./copy.sh $@
ssh pi -A "cd project; python3 $@"
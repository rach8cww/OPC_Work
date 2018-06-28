#! /bin/bash

# scp -r $@ pi:~/project
rsync -r $@ pi:~/project

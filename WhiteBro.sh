#!/bin/bash

source env/bin/activate
if [ $# -ne 1 ]; then
    echo file://`pwd`/startpage.html
    python WhiteBro.py file://`pwd`/startpage.html
else
    echo $1
    python WhiteBro.py $1
fi

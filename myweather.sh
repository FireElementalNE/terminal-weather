#!/bin/bash
#be sure to change the directories OR add this dir to your path!
if [ $# == 2  ]; then
    CITY=$1
    COUNTRY=$2
    python weather.py ${CITY} ${COUNTRY}
else
    CITY=$1
    python weather.py ${CITY}
fi

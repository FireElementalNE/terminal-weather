#!/bin/bash
#be sure to change the directories OR add this dir to your path!
if [ $# -eq 3 ]; then
    UNIT=$1
    CITY=$2
    COUNTRY=$3
    python weather.py ${UNIT} ${CITY} ${COUNTRY}
else
    if [ $# -eq 2 ]; then
	UNIT=$1
	CITY=$2
	python weather.py ${UNIT} ${CITY}
    else
	python weather.py
    fi
fi


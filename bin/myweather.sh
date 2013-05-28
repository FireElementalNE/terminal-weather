#!/bin/bash
#be sure to change the directories OR add this dir to your path!
if [ $# -eq 3 ]; then
    UNIT=$3
    CITY=$1
    COUNTRY=$2
    python ~/weather/weather.py ${CITY} ${COUNTRY} ${UNIT}
else
    if [ $# -eq 2 ]; then
	if [[ $2 =~ \d\d\d\d+ ]]; then
	    CITY=$1
	    UNIT=$2
	    python ~/weather/weather.py ${CITY} ${UNIT}
	else
	    CITY=$1
	    COUNTRY=$2
	    python ~/weather/weather.py ${CITY} ${UNIT}
	fi
    else
	if [ $# -eq 1 ]; then
	    CITY=$1
	    python ~/weather/weather.py ${CITY}
	else
	    python ~/weather/weather.py
	fi
    fi
fi


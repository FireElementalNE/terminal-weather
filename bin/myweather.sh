#!/bin/bash
#be sure to change the directories OR add this dir to your path!
MYDIR=~/terminal-weather/weather.py
if [ $# -eq 3 ]; then
    UNIT=$3
    CITY=$1
    COUNTRY=$2
    python ${MYDIR} ${CITY} ${COUNTRY} ${UNIT}
else
    if [ $# -eq 2 ]; then
	if [[ $2 =~ \d\d\d\d+ ]]; then
	    CITY=$1
	    UNIT=$2
	    python ${MYDIR} ${CITY} ${UNIT}
	else
	    CITY=$1
	    COUNTRY=$2
	    python ${MYDIR} ${CITY} ${COUNTRY}
	fi
    else
	if [ $# -eq 1 ]; then
	    CITY=$1
	    python ${MYDIR} ${CITY}
	else
	    python ${MYDIR}
	fi
    fi
fi


#!/usr/bin/bash

N=1000
LOG=bpu.log

if [ -e $LOG ]; then
    echo "${LOG} is exist, so remove it."
    rm -f ${LOG}
fi

for ((i=0; i<$N; i++))
do
    hrut_bpuprofile -b 2 -r 1 >> $LOG
done
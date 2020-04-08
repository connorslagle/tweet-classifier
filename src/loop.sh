#!/bin/bash
for ((i = 0; i <= 2; i++))
do
	for ((j = 0; j <= 4; j++))
	do
		python loop_script.py -s $i -l $j -n $1
	done
done

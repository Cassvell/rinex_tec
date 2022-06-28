#!/bin/bash

#dir = https://data.unavco.org/archive/gnss/rinex/obs/2022/

zeroes="000"
DOY=()
zero="0"

idate = -d '2022-02-22' +%j
fdate = -d '2022-02-24' +%j   
for i in {$idate..$fdate}

	tmp_n="$zeroes$i"
	#echo "${tmp_n:(-${#zeroes})}"
	DOY=("${tmp_n:(-${#zeroes})}")
	
	for j in "${DOY[@]}"
	do 
		wget https://data.unavco.org/archive/gnss/rinex/obs/2022/$j/ucoe$j$zero.22o.Z
	done

done 
uncompress *.Z 

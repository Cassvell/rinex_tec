#!/bin/bash

#dir = https://data.unavco.org/archive/gnss/rinex/obs/2022/

#zeroes="000"
#DOY=()
zero="0"


read -p "Enter the initial date with the format (yyyy-mm-dd): " iuser_date
idate=$(date -d "$iuser_date" +%j)

#echo $idate

read -p "Enter the final date with the format (yyyy-mm-dd): " fuser_date

#read iday

for i in {seq ${idate} ${fdate}}
do
        wget https://data.unavco.org/archive/gnss/rinex/obs/2022/$i/ucoe$i$zero.22o.Z
done
uncompress *.Z

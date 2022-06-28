#!/bin/bash

#dir = https://data.unavco.org/archive/gnss/rinex/obs/2022/

zero="0"
zeroes="000"
DOY=()

#mover los archivos del directorio ucoe.obs_med al directorio general ucoe.obs

echo 'descargar datos de rinex'
read -p "Enter the initial date with the format (yyyy-mm-dd): " iuser_date
idate=$(date -d "$iuser_date" +%j)

#echo $idate

read -p "Enter the final date with the format (yyyy-mm-dd): " fuser_date
fdate=$(date -d "$fuser_date" +%j)

#read iday

read -p "Enter the name code of the GNSS station: " code

for i in $(seq ${idate} ${fdate})	
do
        tmp_n="$zeroes$i"
        #echo "${tmp_n:(-${#zeroes})}"
        DOY=("${tmp_n:(-${#zeroes})}")	
        wget https://data.unavco.org/archive/gnss/rinex/obs/2022/$DOY/$code$DOY$zero.22o.Z
	#echo $DOY
done
uncompress *.Z

wine /home/c-isaac/Documentos/rinex_ucoe/GPS_Gopi_v3.03/GPS_TEC.exe

mv *.22o /home/c-isaac/Documentos/rinex_ucoe/rinex.obs


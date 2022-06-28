#!/bin/bash


echo "moving files from output_gopi to next dir..."

read -p "Introduce the name of the folder to move (code): " folder
ext='_cmn'

if [ -d "/home/c-isaac/Documentos/rinex_ucoe/$folder$ext" ]
then 
	mv /home/c-isaac/Documentos/rinex_ucoe/output_gopi/*.Cmn /home/c-isaac/Documentos/rinex_ucoe/$folder$ext
else 
	mkdir $folder$ext
	mkdir $folder$ext/med
	mkdir $folder$ext/obs
	mv /home/c-isaac/Documentos/rinex_ucoe/output_gopi/*.Cmn /home/c-isaac/Documentos/rinex_ucoe/$folder$ext
fi


file1=/home/c-isaac/Documentos/rinex_ucoe/$folder$ext/med
file2=/home/c-isaac/Documentos/rinex_ucoe/$folder$ext/obs

if [ -d "$file1" ]; then
	if [ "$(-A $file1)"]; then
		echo 'no hay documentos previos'
	else	
		mv /home/c-isaac/Documentos/rinex_ucoe/$folder$ext/med/*.Cmn /home/c-isaac/Documentos/rinex_ucoe/$folder$ext
	fi
fi

if [ -d "$file2" ]; then

        if [ "$(-A $file2)" ]; then     
                echo 'no hay documentos previos'
        else
                mv /home/c-isaac/Documentos/rinex_ucoe/$folder$ext/obs/*.Cmn /home/c-isaac/Documentos/rinex_ucoe/$folder$ext
        fi
fi




read -p "Introduce date for med reference(yyyy-mm-dd ): " date_ref
date=$(date -d "$date_ref" +%j)
echo $date

read -p "introduce doy: " num
read -p "introduce year: " year

a=$num
b=28

doy=$(expr $a - $b)

begining=$(date -d ""$year"-1-1 +$doy days" +%F)

echo 'fecha de inicio debe ser: '$begining'' 


echo 'select Cmn files to create TEC med and move to med dir'
read -p "Enter the initial date with the format (yyyy-mm-dd): " iuser_date
idate=$(date -d "$iuser_date" +%j)
#echo $idate

read -p "Enter the final date with the format (yyyy-mm-dd): " fuser_date
fdate=$(date -d "$fuser_date" +%j)
#echo $fdate

zeroes="000"
DOY=()

for i in $(seq ${idate} ${fdate})
do
        tmp_n="$zeroes$i"
        #echo "${tmp_n:(-${#zeroes})}"
        DOY=("${tmp_n:(-${#zeroes})}")
	
	mv /home/c-isaac/Documentos/rinex_ucoe/$folder$ext/$folder$DOY* /home/c-isaac/Documentos/rinex_ucoe/$folder$ext/med

done
 
###########################################################################
###########################################################################

echo 'select cmn files to create obs TEC and move to obs dir'

read -p "Enter the initial date with the format (yyyy-mm-dd): " iuser_date2
idate2=$(date -d "$iuser_date2" +%j)

#echo $idate

read -p "Enter the final date with the format (yyyy-mm-dd): " fuser_date2
fdate2=$(date -d "$fuser_date2" +%j)

for i in $(seq ${idate2} ${fdate2})
do
        tmp_n="$zeroes$i"
        #echo "${tmp_n:(-${#zeroes})}"
        DOY=("${tmp_n:(-${#zeroes})}")

        mv /home/c-isaac/Documentos/rinex_ucoe/$folder$ext/$folder$DOY* /home/c-isaac/Documentos/rinex_ucoe/$folder$ext/obs

done

python3 vtec.py


#!/bin/sh -x

templist=$1
BLID=$2
ID=$3
src=$4
dest=$5
suffix=$6
MT=$7
refFile=$8

# Copy ListOfTemplates
cp -v \
 ${templist} \
 ${dest}/${ID}_${suffix}-ListOfTemplates.txt;		
		

for t in $( cat ${dest}/${ID}_${suffix}-ListOfTemplates.txt )
do
	echo -e "\n\nTemplate${t}"
	
	for m in dramms ants
	do
		if [ -f ${src}/${BLID}_${suffix}-Template${t}_label_InSpace_${m}.nii.gz ] \
		&& [ ! -f ${dest}/${ID}_${suffix}-Template${t}_label_InSpace_${m}.nii.gz ]
		then
			echo -e "\n"
			
			WarpImageMultiTransform \
			 3 \
			 ${src}/${BLID}_${suffix}-Template${t}_label_InSpace_${m}.nii.gz \
			 ${dest}/${ID}_${suffix}-Template${t}_label_InSpace_${m}.nii.gz \
			 --use-NN \
			 -R ${refFile} \
			 ${dest}/tmp_ants/blwarpedWarp.nii.gz \
			 ${dest}/tmp_ants/blwarpedAffine.txt; 
		fi
		
		
		if [ -f ${src}/${BLID}_${suffix}-Template${t}_InSpace_${m}.nii.gz ] \
		&& [ ! -f ${dest}/${ID}_${suffix}-Template${t}_InSpace_${m}.nii.gz ]
		then
			echo -e "\n"
			
			WarpImageMultiTransform \
			 3 \
			 ${src}/${BLID}_${suffix}-Template${t}_InSpace_${m}.nii.gz \
			 ${dest}/${ID}_${suffix}-Template${t}_InSpace_${m}.nii.gz \
			 -R ${refFile} \
			 ${dest}/tmp_ants/blwarpedWarp.nii.gz \
			 ${dest}/tmp_ants/blwarpedAffine.txt; 
		fi

		while [ `jobs -p | wc -l` -ge $MT ]; do sleep 1s; done
		
		
		if [ -f ${src}/${BLID}_${suffix}-Template${t}_Sim_${m}.nii.gz ] \
		&& [ ! -f ${dest}/${ID}_${suffix}-Template${t}_Sim_${m}.nii.gz ]
		then
			echo -e "\n"
			
			$(dirname $(dirname `which muse`))/lib/muse-calculateSimilarityMap \
			 -a ${refFile} \
			 -b ${dest}/${ID}_${suffix}-Template${t}_InSpace_${m}.nii.gz \
			 -sim ${dest}/${ID}_${suffix}-Template${t}_Sim_${m}.nii.gz \
			 -v 0 &
		fi
		
# 		read -p ee
	done
done

wait `jobs -p`

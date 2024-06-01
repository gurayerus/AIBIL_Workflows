#!/bin/sh +x

## Read args
fin=${1}
fout=${2}

## MUSE params
MuseSSTempNum='50'
MuseSSTempLoc=${MUSE_DIR}/data/Templates/BrainExtraction
MuseSSrois=${MUSE_DIR}/data/List/MUSE-SS_ROIs.csv
MuseSSMethod='3'
MuseSSTemps='15'
MuseSSDRAMMSReg='0.1'
MuseSSANTSReg='0.5'
MT='4'
d='1'


dout=`dirname ${fout}`
fnameout=`basename ${fout} | sed 's/.nii.gz//g'`

mkdir -pv ${dout}/logs

## Apply MUSE skull-stripping with the muse container
cmd="muse -i ${fin} -r ${MuseSSTempLoc} -n ${MuseSSTempNum} -R ${MuseSSrois} -D ${dout} -o ${fnameout} -M ${MuseSSMethod} -g ${MuseSSDRAMMSReg} -s ${MuseSSANTSReg} -p -I -F -T ${MuseSSTemps} -k 0 -P $MT -Q -l ${dout}/logs/ -d ${d}"

echo "About to run: $cmd"
$cmd


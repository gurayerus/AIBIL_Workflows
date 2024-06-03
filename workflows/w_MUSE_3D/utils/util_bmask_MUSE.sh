#!/bin/sh +x

## Read args
fin=`realpath ${1}`
fout=`realpath ${2}`

## Set vars
dout=`dirname ${fout}`
fnameout=`basename ${fout} | sed 's/.nii.gz//g'`

## Set params
MuseSSTempLoc='/cbica/software/muse-3.1.0/data/Templates/BrainExtraction'
MuseSSTempNum='50'
MuseSSrois='/cbica/software/muse-3.1.0/data/List/MUSE-SS_ROIs.csv'
MuseSSMethod='3'
MuseSSDRAMMSReg='0.1'
MuseSSANTSReg='0.5'
MuseSSTemps='15'
MT='4'
d='1'

mkdir -pv ${dout}/logs

## Apply MUSE skull-stripping with the muse container
cmd="muse -i ${fin} -r ${MuseSSTempLoc} -n ${MuseSSTempNum} -R ${MuseSSrois} -D ${dout} -o ${fnameout} -M ${MuseSSMethod} -g ${MuseSSDRAMMSReg} -s ${MuseSSANTSReg} -p -I -F -T ${MuseSSTemps} -k 0 -P $MT -Q -l ${dout}/logs/ -d ${d}"

echo About to run: $cmd

$cmd



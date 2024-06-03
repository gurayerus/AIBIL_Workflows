#!/bin/sh +x

## Read args
fin=`realpath ${1}`
fout=`realpath ${2}`

## Set vars
muse_cont='/cbica/projects/OASIS/OASIS3/Pipelines/OASIS3_3.5D_2020/Container/CBICApipeline_centos7.sif'
dout=`dirname ${fout}`
fnameout=`basename ${fout} | sed 's/.nii.gz//g'`
MuseTempLoc='/opt/cbica/software/muse-3.1.0/data/Templates/WithCere'
MuseTempNum='35'
MuseRois='/opt/cbica/software/muse-3.1.0/data/List/MUSE-SS_ROIs.csv'
MuseMethod='3'
MuseDRAMMSReg='0.1'
MuseANTSReg='0.5'
MuseTemps='11'
MT='4'
d='1'

mkdir -pv ${dout}/logs

## Run MUSE
cmd="muse -i ${fin} -r ${MuseTempLoc} -n ${MuseTempNum} -D ${dout} -o ${fnameout} -M ${MuseMethod} -g ${MuseDRAMMSReg} -s ${MuseANTSReg} -c ${MuseCSF} -T ${MuseTemps} -l ${dout}/logs/ -k 0 -Q -P $MT"

echo About to run: $cmd

$cmd

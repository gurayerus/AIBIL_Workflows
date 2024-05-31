#!/bin/sh +x

# ## Singularity wrapper
# ### Timestamps
# echo -e "\nRunning commands on          : `hostname`"
# echo -e "Start time                   : `date +%F-%H:%M:%S` \n"
# echo -e "\n"
# set -x
# /usr/bin/singularity \
#  run \
#  -B ${TMPDIR} \
#  $*
# set +x
# echo -e "\n"


# ## Run
# bash \
#  ${PROJ}/Container/singularity_wrapper.sh \
#  ${PROJ}/Container/CBICApipeline_centos7.sif \
#  ${PROJ}/Scripts/sMRI_ProcessingPipeline/Scripts/ProcessingPipeline_subject_3.5D.sh \
#  -ID $SUB \
#  -BLID $BLID \
#  -T1 ${DATA}/${SUB}/${SUB}_T1.nii.gz \
#  -FL ${DATA}/${SUB}/${SUB}_FL.nii.gz \
#  -T2 ${DATA}/${SUB}/${SUB}_T2.nii.gz \
#  -dest ${PROJ} \
#  -MT 4 > ${PROJ}/Protocols/logs/${SUB}/ProcessingPipeline_subject_3.5D.sh-${JOB_ID}-${SGE_TASK_ID}.log 2>&1

## Read args
fin=`realpath ${1}`
fout=`realpath ${2}`

## Set vars
muse_cont='/cbica/projects/OASIS/OASIS3/Pipelines/OASIS3_3.5D_2020/Container/CBICApipeline_centos7.sif'
dout=`dirname ${fout}`
fnameout=`basename ${fout} | sed 's/.nii.gz//g'`
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
cmd="/usr/bin/singularity run -B ${TMPDIR} ${muse_cont} muse -i ${fin} -r ${MuseSSTempLoc} -n ${MuseSSTempNum} -R ${MuseSSrois} -D ${dout} -o ${fnameout} -M ${MuseSSMethod} -g ${MuseSSDRAMMSReg} -s ${MuseSSANTSReg} -p -I -F -T ${MuseSSTemps} -k 0 -P $MT -Q -l ${dout}/logs/ -d ${d}"

echo $cmd


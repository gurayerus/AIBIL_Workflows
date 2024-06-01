#!/bin/sh +x

## Input args
in_img=$(realpath $1)
bl_img=$(realpath $2)
bl_seg=$(realpath $3)
out_img=$(realpath $4)
MRID=$5
BLID=$6

## Create tmp outdir
dout=$(dirname $out_img)
dtmp=${dout}/tmp_ants
mkdir -pv $dtmp

## Get var names for other intermediate images
tlist=${bl_seg%_muse.nii.gz}-ListOfTemplates.txt
BLDIR=$(dirname $bl_seg)
FUDIR=$(dirname $out_img)
insuff='T1_LPS_N4_brain_muse-ss_Mean_fastbc'
musesuff='_T1_LPS_N4_brain_muse-ss_Mean_fastbc_muse'
MT='4'

#################################
## Run ANTs
# cmd="ANTS 3 -m PR[$bl_img,$in_img,1,2] -i 10x50x50x10 -o ${dtmp}/blwarped.nii.gz
# -t SyN[0.5] -r Gauss[2,0]"

# ### FIXME the params are changed here to run it fast for now
# cmd="ANTS 3 -m PR[$bl_img,$in_img,1,2] -i 2x3x3x4 -o ${dtmp}/blwarped.nii.gz
# -t SyN[0.5] -r Gauss[2,0]"
# echo "Running: $cmd"
# $cmd

#################################
# Apply warp to MUSE intermediate files
cmd="utils/applyWarpToMuseInterFiles.sh $tlist $BLID $MRID $BLDIR $FUDIR $insuff $MT $in_img"
echo $cmd
$cmd

#################################
# Run MUSE on FU

MuseMethod='3'
MuseDRAMMSReg='0.1'
MuseANTSReg='0.5'
MuseCSF='1.2'
MuseTemps='11'

muse 
    -i $in_img \
    -r $MuseTempPath \
    -n ${MuseTempNum} \
    -D ${MUSE_4D}/${MRID} \
    -o ${MRID}_${musesuff} \
    -M ${MuseMethod} \
    -g ${MuseDRAMMSReg} \
    -s ${MuseANTSReg} \
    -c $MuseCSF \
    -T $MuseTemps \
    -l ${MUSE_4D}/${MRID}/logs \
    -k 0 \
    -Q \
    -P $MT

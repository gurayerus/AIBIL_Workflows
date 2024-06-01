#!/bin/sh +x

## Apply MUSE 

fin=$(realpath $1)
fout=$(realpath $2)

# MuseTempPath=${MUSE_DIR}/data/Templates/WithCere
# MuseTempNum=35
# MuseMethod=3
# MuseDRAMMSReg=0.1
# MuseANTSReg=0.5
# MuseCSF=1.2
# MuseTemps=11
# MT=1
# 
# muse -i ${fin} -r $MuseTempPath -n ${MuseTempNum} -D ${dout} \
#  -o ${pout} -M ${MuseMethod} -g ${MuseDRAMMSReg} -s ${MuseANTSReg} \
#  -c $MuseCSF -T $MuseTemps -l ${dout}/logs -k 1 -Q -P $MT

##########################################
## FIXME tmp copy prev out

# mrid=`basename $fin | cut -d'_' -f1-3`
# odir=`dirname $fout`
# bdir='/cbica/projects/OASIS/OASIS3/Pipelines/OASIS3_3.5D_2020/Protocols/MUSE_BL'

mrid=`basename $fin | cut -d'_' -f1-2`
odir=`dirname $fout`
bdir='/cbica/projects/Prevent_AD/Pipelines/preventad_3.5D_2022/Protocols/MUSE_BL'

muse=${bdir}/${mrid}/${mrid}_T1_LPS_N4_brain_muse-ss_Mean_fastbc_muse.nii.gz

# mkdir -pv $odir
# cp ${bmask} ${odir}
# cp ${rank} ${odir}

for ll in `ls -1 ${bdir}/${mrid} | grep -v logs`; do
    ln -s ${bdir}/${mrid}/${ll} ${odir}/
done

## FIXME tmp copy prev out
##########################################

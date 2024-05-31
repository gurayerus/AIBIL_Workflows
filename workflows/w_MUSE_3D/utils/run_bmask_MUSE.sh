#!/bin/sh +x

## Apply MUSE skull-stripping

fin=$(realpath $1)
fout=$(realpath -m $2)

# muse -i ${fin} -r ${MuseSSTempLoc} -n ${MuseSSTempNum} -R ${MuseSSrois} \
# 	 -D ${SS}/${ID} -o ${fout} -M ${MuseSSMethod} -g ${MuseSSDRAMMSReg} \
# 	 -s ${MuseSSANTSReg} -p -I -F -T ${MuseSSTemps} -k 0 -P $MT \
# 	 -Q -l ${SS}/${ID}/logs/ -d 1



##########################################3
## FIXME tmp copy prev out

# mrid=`basename $fin | cut -d'_' -f1-3`
# odir=`dirname $fout`
# bdir='/cbica/projects/OASIS/OASIS3/Pipelines/OASIS3_3.5D_2020/Protocols/Skull-Stripped'

mrid=`basename $fin | cut -d'_' -f1-2`
odir=`dirname $fout`
bdir='/cbica/projects/Prevent_AD/Pipelines/preventad_3.5D_2022/Protocols/Skull-Stripped'

bmask=${bdir}/${mrid}/${mrid}_T1_LPS_N4_brainmask_muse-ss.nii.gz
rank=${bdir}/${mrid}/${mrid}_T1_LPS_N4_ROI_1_SimRank.nii.gz

mkdir -pv $odir
cp ${bmask} ${odir}
cp ${rank} ${odir}

## FIXME tmp copy prev out
##########################################3

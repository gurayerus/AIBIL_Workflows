#! /bin/bash

## Read input
t1=$1
t1ce=$2
t2=$3
fl=$4
fout=$5

mdldir="/cbica/software/lab/captk/centos7/1.7.6/data/deepMedic/saved_models/skullStripping"

## keep 1.7.6 
captk_module="captk/1.7.6"
module unload captk
module load ${captk_module}
dm_exe=`which DeepMedic`

outdir=`dirname $(realpath $fout)`
tmpdir=${outdir}/tmp_deep_medic
mkdir -pv $tmpdir

## Apply deep medic
# echo ${dm_exe} -t1c $t1ce -t1 $t1 -fl $fl -t2 $t2 -md $mdldir -o $fout
${dm_exe} -t1c $t1ce -t1 $t1 -fl $fl -t2 $t2 -md $mdldir -o $tmpdir

## Move final results to out folder
for mod in t1 t2 t1ce; do
    mv ${tmpdir}/${mod}_normalized.nii.gz ${outdir}/
done
mv ${tmpdir}/fl_normalized.nii.gz ${outdir}/flair_normalized.nii.gz
mv ${tmpdir}/predictions/testApiSession/predictions/ProbMapClass0.nii.gz ${outdir}/
mv ${tmpdir}/predictions/testApiSession/predictions/ProbMapClass1.nii.gz ${outdir}/
mv ${tmpdir}/predictions/testApiSession/predictions/Segm.nii.gz ${fout}

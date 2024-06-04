#!/bin/sh +x

## Apply FAST bias correction

export FSLOUTPUTTYPE=NIFTI_GZ

fin=$(realpath $1)
fout=$(realpath $2)

## Create tmp outdir
dout=$(dirname $fout)
dtmp=${dout}/tmp_fast
mkdir -pv $dtmp

FASTiter=8
FASTfwhm=20

# fast -n 3 -I $FASTiter -l $FASTfwhm -B -o ${dtmp}/fastseg -v ${fin}

## FIXME simple args here to run fast
FASTiter=1
fast -n 3 -I $FASTiter -l $FASTfwhm -B -o ${dtmp}/fastseg.nii.gz -v ${fin}

cp ${dtmp}/fastseg_restore.nii.gz $fout

rm -rf ${dtmp}

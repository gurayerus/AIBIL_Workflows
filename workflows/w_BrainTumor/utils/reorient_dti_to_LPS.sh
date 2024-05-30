#! /bin/bash

## Read input
fin=$1
fout=$2
orient=$3

captk_exe='/cbica/software/lab/captk/centos7/1.8.1/bin/captk'

## Check that input DTI.nii.gz is in LAS orientation
orient=`fslhd $fin | grep qform_.orient | cut -d- -f3 | cut -c1 | tr '\n' ',' | sed 's/,//g'`

if [ "$orient" != "LAS" ]; then
    echo -e "Input DTI is not in LAS orientation. DTI preprocessing aborted"
    exit 1;
fi

## Reorient image
$captk_exe Utilities -i $fin -o ${fout%.nii.gz}.mha -or $orient
$captk_exe Utilities -i ${fout%.nii.gz}.mha -o $fout -cov
rm -rf ${fout%.nii.gz}.mha

## Copy bval
cp ${fin%.nii.gz}.bval ${fout%.nii.gz}.bval

## Multiply values in bvec with -1 (for specific reorientation from LAS to LPS)
awk 'NR==2 { for (i=1; i<=NF; ++i) $i = -$i } 1' ${fin%.nii.gz}.bvec > ${fout%.nii.gz}.bvec

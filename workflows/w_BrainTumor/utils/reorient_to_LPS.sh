#! /bin/bash

## Read input
fin=$1
fout=$2
orient=$3

captk_exe='/cbica/software/lab/captk/centos7/1.8.1/bin/captk'

## Reorient image
$captk_exe Utilities -i $fin -o ${fout%.nii.gz}.mha -or $orient
$captk_exe Utilities -i ${fout%.nii.gz}.mha -o $fout -cov
rm -rf ${fout%.nii.gz}.mha

#! /bin/bash -x

## Read input
fin=$1
fmask=$2
fout=$3

captk_exe='/cbica/software/lab/captk/centos7/1.8.1/bin/captk'

## Mask image
$captk_exe Utilities -i $fin -o $fout -m $fmask

#!/bin/sh +x

## Input args
in_img=$(realpath $1)
ref_img=$(realpath $2)
out_img=$(realpath -m $3)

## Run ANTs
cmd="ANTS 3 -m PR[$ref_img,$in_img,1,2] -i 10x50x50x10 -o $out_img -t SyN[0.5] -r Gauss[2,0]"
echo "Running: $cmd"
$cmd


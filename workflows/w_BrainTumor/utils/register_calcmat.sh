#! /bin/bash

## Read input
fin=$1
fref=$2
fout=$3

## Default args
##  Add to args for changing them if necessary
dim="3"; #assume 3D image
metric="NMI"; #use normalized mutual information
iter="100x50x10"; #100 iterations at lowest resolution, 50 at intermediate, 10 at full resolution
dof="6"; #6 for rigid, 12 for affine

reg_exe="/cbica/software/external/greedy/centos7/c6dca2e/bin/greedy"

## Calculate reg mat 

## If in and ref images are the same, create an empty out mat file
if [ "${fin}" == "${fref}" ]; then
    touch ${fout}
else
    ${reg_exe} -d ${dim} -a -m ${metric} -ia-image-centers -n ${iter} -dof ${dof} -i ${fref} ${fin} -o ${fout}
fi

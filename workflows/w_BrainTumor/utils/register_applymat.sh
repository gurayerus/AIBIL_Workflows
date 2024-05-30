#! /bin/bash

## Read input
fin=$1
fref=$2
fmat=$3
fout=$4

## Default args
##  Add to args for changing them if necessary
dim="3"; #assume 3D image
interp="LINEAR";

reg_exe="/cbica/software/external/greedy/centos7/c6dca2e/bin/greedy"

## Apply reg mat 

## If in and ref images are the same, copy in image to out
if [ "${fin}" == "${fref}" ]; then
    cp ${fin} ${fout}
else
    ${reg_exe} -d ${dim} -rf ${fref} -ri ${interp} -rm ${fin} ${fout} -r ${fmat}
fi

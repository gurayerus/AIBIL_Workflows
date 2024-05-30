#! /bin/bash

## Read input
fin=$1
fout=$2

## Shrink factor is set to s=4 (default value in ANTs). Optionally 
##  it can be added as a parameter to use different values 
##  (e.g. by adding a list of values in Snakemake rule)
shrink=4

## Image is not rescaled
rescaling=0

n4_exe="/cbica/software/external/ANTs/centos7/2.3.1/bin/N4BiasFieldCorrection"

## Apply n4 
$n4_exe -i ${fin} -s $shrink -r $rescaling -o ${fout}


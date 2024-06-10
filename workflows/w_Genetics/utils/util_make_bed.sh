#!/bin/bash
# make bed and apply filters

## Read args
bgen=`realpath ${1}`
sample=`realpath ${2}`
chrno=${3}
flagref=${4}
maf=${5}
geno=${6}
hwe=${7}
mind=${8}
rmdup=${9}
flagmbed=${10}
fout=`realpath ${11}`

## Edit args
ref=''
if [ "${flagref}" == '1' ]; then
    ref='ref-first'
fi

mbed=''
if [ "${flagmbed}" == '1' ]; then
    mbed='--make-bed'
fi

## Load modules
module load plink/2.20210701

## Run command
cmd="plink2 --bgen ${bgen} ${ref} --sample ${sample} --maf ${maf} --geno ${geno} --hwe ${hwe} --mind ${mind} --rm-dup ${rmdup} $mbed --out ${fout}"
echo; echo "About to run: $cmd"; echo
# $cmd

                                                                                                                                        

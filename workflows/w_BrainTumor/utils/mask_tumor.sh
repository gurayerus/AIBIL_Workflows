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

## Mask image
${dm_exe} -t1c $t1ce -t1 $t1 -fl $fl -t2 $t2 -md $modeldir -o $fout

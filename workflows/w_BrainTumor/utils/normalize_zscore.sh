#! /bin/bash

## Read input
fin=$1
fout=$2

mdldir="/cbica/software/lab/captk/centos7/1.7.6/data/deepMedic/saved_models/skullStripping"

## keep 1.7.6 
captk_module="captk/1.7.6"
module unload captk
module load ${captk_module}
pp_exe=`which Preprocessing`

## Mask image
${pp_exe} -zn -i ${fin} -o ${fout}

#!/bin/sh +x

## Apply MUSE skull-stripping

t1=$(realpath $1)
t2=$(realpath $2)
rank=$(realpath $3)
T2ICViter=$4
T2ICVminsd=$5
T2ICVmaxsd=$6
T2ICVtol=$7
fout=$(realpath $8)

echo python ./utils/GenerateICVmask.py -i ${t1} -r ${t2} -j ${rank} -o ${fout} -n $T2ICViter -l $T2ICVminsd -h $T2ICVmaxsd -t $T2ICVtol 

python ./utils/GenerateICVmask.py -i ${t1} -r ${t2} -j ${rank} -o ${fout} -n $T2ICViter -l $T2ICVminsd -h $T2ICVmaxsd -t $T2ICVtol -v

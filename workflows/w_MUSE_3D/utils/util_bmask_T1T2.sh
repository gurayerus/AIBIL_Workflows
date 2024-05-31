#!/bin/sh +x

## Apply MUSE skull-stripping

t1=$(realpath $1)
t2=$(realpath $2)
bmask=$(realpath $3)
fout=$(realpath $4)

rank=${bmask%_brain_muse-ss_Mean.nii.gz}_ROI_1_SimRank_Mean.nii.gz

T2ICViter=100
T2ICVminsd=-1
T2ICVmaxsd=100
T2ICVtol=0.00001

GenerateICVmask.py -i ${t1} -r ${t2} -j ${rank} -o ${fout} -n $T2ICViter -l $T2ICVminsd -h $T2ICVmaxsd -t $T2ICVtol 

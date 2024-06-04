#!/bin/bash

outpath=/cbica/home/yangzhi/project_in_progress/gene_guided_smilegan/hypertension_train
mkdir ${outpath}/logs/ -pv

qsub -o ${outpath}/logs/\$JOB_NAME-\$JOB_ID.log  ./parellel.sh

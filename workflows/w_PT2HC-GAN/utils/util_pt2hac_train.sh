#! /usr/bin/bash

in_demog=`realpath ${1}`
in_roi=`realpath ${2}`
n_pattern=${3}
final_saving_epoch=${4}
fold=${5}
numfold=${6}
outmdl=`realpath ${7}`

outdir=`dirname $outmdl`

cmd="python ./utils/surrealgan_train_model.py --train_data $in_roi --covariate_data $in_demog --output_dir $outdir --npattern $n_pattern --start_fold $fold --fold_number $numfold --final_saving_epoch $final_saving_epoch"

echo "About to run $cmd"
$cmd


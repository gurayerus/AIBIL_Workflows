#! /usr/bin/bash

in_demog=${1}
in_roi=${2}
n_cluster=${3}
fold=${4}
numfold=${5}
outmdl=`realpath ${6}`

outdir=`basedir $outmdl`

cmd="python ./utils/smilegan_train_model.py --train_data $in_toi --covariate_data $in_demog -output_dir $outdir --ncluster $n_cluster --start_fold $fold --fold_number $numfold"

echo "About to run $cmd"
$cmd


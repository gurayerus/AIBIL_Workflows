#! /usr/bin/bash

in_data=`realpath ${1}`
in_covar=`realpath ${2}`
mdl=`realpath ${3}`
epoch=${4}
out_csv=`realpath ${5}`

cmd="python ./utils/surrealgan_test.py --in_data $in_data --in_covar $in_covar --model $mdl --epoch $epoch --out_csv $out_csv"

echo "About to run $cmd"
$cmd


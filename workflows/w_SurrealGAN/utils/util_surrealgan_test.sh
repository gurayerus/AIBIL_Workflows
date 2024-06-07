#! /usr/bin/bash

in_data=`realpath ${1}`
in_covar=`realpath ${2}`
epoch=${3}
out_csv=`realpath ${4}`

cmd="python ./utils/surrealgan_test.py --in_data $in_data --in_covar $in_covar --epoch $epoch --out_csv $out_csv"

echo "About to run $cmd"
$cmd


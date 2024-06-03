#!/bin/sh +x

## This script calls MUSE for skull stripping using the MUSE container

fin=${1}
muse_cont=${2}
fout=${3}

## Run MUSE 
cmd="/usr/bin/singularity run -B $TMPDIR $muse_cont ./utils/util_MUSE.sh $fin $fout"
echo "About to run: $cmd"
$cmd


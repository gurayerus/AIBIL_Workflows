#!/bin/sh +x

## N4 bias correction

fin=$(realpath $1)
fout=$(realpath $2)

N4BiasFieldCorrection -d 3 -i ${fin} -o ${fout}

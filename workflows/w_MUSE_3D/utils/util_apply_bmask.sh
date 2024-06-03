#!/bin/sh +x

## Apply mask to image

inimg=$(realpath $1)
inmask=$(realpath $2)
fout=$(realpath $3)

3dcalc -prefix ${fout} -a ${inimg} -b ${inmask} -expr "a*step(b)" -verbose -nscale

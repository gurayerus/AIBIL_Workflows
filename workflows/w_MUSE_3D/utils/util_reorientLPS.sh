#!/bin/sh +x

## Reorient nifti image to LPS

fin=$(realpath $1)
fout=$(realpath $2)

dout=$(dirname $fout)

dtmp=${dout}/tmp_reorient
mkdir -pv $dtmp
cd $dtmp

### Get file pair
nifti1_test -n2 ${fin} tmp;

### Resample/Reorient
3dresample -orient rai -prefix tmp_LPS.hdr -inset tmp.hdr

### Clear sform
nifti_tool -mod_hdr -mod_field sform_code 0 -prefix tmp_nosform.hdr -infiles tmp_LPS.hdr

### Convert to nii.gz
nifti1_test -zn1 tmp_nosform.img $fout
 
### Remove intermediate files
rm -rf ../tmp_reorient

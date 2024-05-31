#!/bin/sh +x

## Input args
in_img=$(realpath $1)
in_mask=$(realpath $2)
bl_img=$(realpath $3)
bl_mask=$(realpath $4)
out_img=$(realpath $5)

## Create tmp outdir
dout=$(dirname $out_img)
dtmp=${dout}/tmp_ants
mkdir -pv $dtmp

## Get var names for other intermediate images
in_img_base=$(basename $in_img)
in_rank=${in_mask%_brainmask_muse-ss.nii.gz}_ROI_1_SimRank.nii.gz
bl_rank=${bl_mask%_brainmask_muse-ss.nii.gz}_ROI_1_SimRank.nii.gz
in_rank_base=$(basename $in_rank)
bl_rank_base=$(basename $bl_rank)
warp=${out_img%.nii.gz}Warp.nii.gz
affine=${out_img%.nii.gz}Affine.nii.gz
out_mask=${out_img%_brain_muse-ss_Mean.nii.gz}_brainmask_muse-ss_Mean.nii.gz

## Run ANTs
# cmd="ANTS 3 -m PR[$bl_img,$in_img,1,2] -i 10x50x50x10 -o ${dtmp}/blwarped.nii.gz
# -t SyN[0.5] -r Gauss[2,0]"

### FIXME the params are changed here to run it fast for now
cmd="ANTS 3 -m PR[$bl_img,$in_img,1,2] -i 2x3x3x4 -o ${dtmp}/blwarped.nii.gz
-t SyN[0.5] -r Gauss[2,0]"
echo "Running: $cmd"
$cmd

# Apply warp to BL SimRank
bl_warp=${dtmp}/blwarpedWarp.nii.gz
bl_aff=${dtmp}/blwarpedAffine.txt
blrank_warped=${dtmp}/blrank_warped.nii.gz
cmd="WarpImageMultiTransform 3 ${bl_rank} ${blrank_warped} -R ${in_img} ${bl_warp} ${bl_aff}"
echo "----------------"
echo "Running: $cmd"
echo "----------------"
$cmd

# Average SimRanks
rank_mean=${dtmp}/rank_Mean.nii.gz
amax=`3dBrickStat -slow -max ${in_rank} | awk '{ print $1 }'`
bmax=`3dBrickStat -slow -max ${blrank_warped} | awk '{ print $1 }'`
echo "----------------"
echo "Running: 3dcalc -prefix ${rank_mean} -a ${in_rank} -b ${blrank_warped} -expr "
echo "----------------"
3dcalc -prefix ${rank_mean} -a ${in_rank} -b ${blrank_warped} -expr "(a/${amax}+b/${bmax})/2" -verbose -nscale -float
# read -p ee
    
# Get mean brain mask
echo "----------------"
echo "Running: 3dcalc -prefix ${out_mask} -a ${rank_mean} -expr"
echo "----------------"
3dcalc -prefix ${out_mask} -a ${rank_mean} -expr "step(a-0.5)" -verbose -nscale -byte

# Get final brain image
echo "----------------"
echo "3dcalc -prefix ${out_img} -a ${in_img} -b ${out_mask} -expr "
echo "----------------"
3dcalc -prefix ${out_img} -a ${in_img} -b ${out_mask} -expr "a*step(b)" -verbose -nscale


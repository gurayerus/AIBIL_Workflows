#! /bin/bash

################################## START OF EMBEDDED SGE COMMANDS ##########################
#$ -S /bin/bash
#$ -cwd
#$ -N run_DM
#$ -j y #### merge stdout and stderr
#$ -l gpu -l h_vmem=36G
#$ -l h_rt=0:10:00
############################## END OF DEFAULT EMBEDDED SGE COMMANDS #######################

## Read input
t1=$1
t1ce=$2
t2=$3
fl=$4
fout=$5

## Model params (hardcoded)
mdlconf='/cbica/software/lab/BTpipeline/2.0.4/data/DM/modelConfig.cfg'
mdlload='/cbica/software/lab/BTpipeline/2.0.4/data/DM/dm1Sc3Thin3Seg40_gt4C_HGG587.HGG_Flag.final.2020-01-28.12.59.42.621007.model.ckpt'

## Set modules and exe
dm_module='DeepMedic/v0.7.1.1'
dm_module='DeepMedic/2019-02-13'
module load ${dm_module}
dm_exe=/cbica/external/python/anaconda/3/envs/DeepMedic_v0.7.1.1/bin/deepMedicRun

## Write config files for each modality

outdir=`dirname $(realpath -m $fout)`
mkdir -pv $outdir

echo $(realpath $t1) > ${outdir}/conf_t1.cfg
echo $(realpath $t1ce) > ${outdir}/conf_t1ce.cfg
echo $(realpath $t2) > ${outdir}/conf_t2.cfg
echo $(realpath $fl) > ${outdir}/conf_flair.cfg
echo SCID > ${outdir}/conf_NamesOfPredictions.cfg

## Write main config file
out_conf=${outdir}/conf_dmConfig.cfg
echo "sessionName = \"testSession\" 
folderForOutput = \"${outdir}\" 
channels = [\"${outdir}/conf_flair.cfg\", \"${outdir}/conf_t1ce.cfg\", \"${outdir}/conf_t1.cfg\", \"${outdir}/conf_t2.cfg\" ] 
namesForPredictionsPerCase = \"${outdir}/conf_NamesOfPredictions.cfg\"
saveSegmentation = True 
saveProbMapsForEachClass = [True, True, True, True, True] 
padInputImagesBool = True 
" > ${out_conf}

## Set deep medic
# if cubic interactive node, check to make sure GPU is available
# nvidia-smi
if [[ "$host" == "cubic-login"* ]]; then
    if [ -z "$(nvidia-smi | grep 'No running processes found')" ]; then
        echo "Exiting as no GPU available on $host at this time"
        exit;
    fi
else
    echo -e "CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"
fi

## Segment image
echo ${dm_exe} -model ${mdlconf} -test ${out_conf} -load $mdlload -dev gpu
${dm_exe} -model ${mdlconf} -test ${out_conf} -load $mdlload -dev gpu

## Copy segmentation
cp  ${outdir}/predictions/testSession/predictions/SCID_Segm.nii.gz $fout

#! /bin/bash

ma_exe="/cbica/external/python/anaconda/3/envs/brainmage/1.0.0/bin/brain_mage_run"

## Read input
fin=$1
fout=$2


## Create out dir
odir=`dirname $(realpath $fout)`
tmpdir=${odir}/tmpbrainma
mkdir -pv $tmpdir

## Create input list
csvfile="$odir/input.csv"
echo "Patient_ID_Modality,image_path" > $csvfile
echo "ID,$fin" >> $csvfile

## Create config file
configfile=${odir}/test_params_ma.cfg
cat <<EOF > $configfile
# Output directory
results_dir = ${odir}/tmpbrainma
# Directory containing subjects for testing (give path here if using the input_data structure, instead of using the csv input. If using csv input, simply keep the period.)
test_dir = .
# Mode: ma (modality-agnostic), single (only 1 modality is being used), multi (multiple modalities used)
mode = ma
#Whether using a csv file as input (recommended) or not. If False, please provide the test_dir. [True or False]
csv_provided = True
#Path to input csv file when csv_provided=True. If csv_provided=False, please give a period. 
test_csv = ${odir}/input.csv
# The number of modalities for testing 
num_modalities = 1
# Type of channels you are gonna enter : **NOTE** that they should match the training configuration
modalities = ['t1', 't2', 't1ce', 'flair']
# Set the type of encoder you need to try out. Options: resunet, fcn, unet
model = resunet
#Number of classes? Maybe right now for skull stripping
num_classes = 2
#Set the base filter of the unet
base_filters = 16
EOF

## Mask image
${ma_exe} -params $configfile -test True -mode MA

## Copy output
cp -L ${tmpdir}/ID/ID_mask.nii.gz $fout

## Remove temp results
# rm -rf $tmpdir

${dm_exe} -t1c $t1ce -t1 $t1 -fl $fl -t2 $t2 -md $modeldir -o $fout

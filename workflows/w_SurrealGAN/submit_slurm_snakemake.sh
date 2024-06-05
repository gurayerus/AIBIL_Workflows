#!/bin/bash

#SBATCH --mem=32000
#SBATCH --output=slurm_logs/snakemake-%j.out

source activate /cbica/home/erusg/.conda/envs/snakemake-tutorial

cd /cbica/home/erusg/GitHub/NiChart/NiChart_Workflows/NiChart_Engine/NiChart_MLAnalytics/workflows/w_spare

# snakemake --cores=1 --executor slurm --default-resources slurm_account=davatzic --jobs 1 
snakemake --cores=1 --executor slurm --default-resources slurm_account=davatzic --jobs 10 

conda deactivate

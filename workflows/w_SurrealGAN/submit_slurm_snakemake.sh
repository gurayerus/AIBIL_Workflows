#!/bin/bash

#SBATCH --mem=32000
#SBATCH --output=slurm_logs/snakemake-%j.out

source activate /cbica/home/erusg/.conda/envs/surrealgan312

# snakemake --cores=1 --executor slurm --default-resources slurm_account=davatzic --jobs 1 

snakemake --cores=1 --executor slurm --default-resources slurm_account=davatzic --jobs 20
# snakemake --cores=1 --executor slurm --default-resources --jobs 1 

conda deactivate

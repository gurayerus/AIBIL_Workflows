#!/bin/bash

#SBATCH --mem=32000
#SBATCH --output=slurm_logs/snakemake-%j.out

snakemake --executor slurm --jobs 1

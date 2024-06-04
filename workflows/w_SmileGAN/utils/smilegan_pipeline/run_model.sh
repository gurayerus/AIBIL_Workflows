#!/usr/bin/env bash

random_seed=${1}

source activate smilegan

echo "Running Permutation"
python run_model.py "$random_seed"
echo "Done!"

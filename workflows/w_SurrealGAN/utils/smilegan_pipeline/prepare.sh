#!/usr/bin/env bash
module load python/anaconda/3.8.8

conda create --name smilegan python=3.8

source activate smilegan

pip install SmileGAN==0.1.3

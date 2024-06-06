#!/usr/bin/env python
import numpy as np
import pandas as pd
import argparse
from SurrealGAN import Surreal_GAN_representation_learning as sgr
import os

def trainSurrealGAN(train_data,  covariate_data, output_dir, npattern,
                    final_saving_epoch, start_fold, stop_fold, fold_number):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    sgr.repetitive_representation_learning(train_data, 
                                           npattern, 
                                           fold_number, 
                                           1, 
                                           final_saving_epoch, 
                                           output_dir, 
                                           lr = 0.0008, 
                                           batchsize = 300, 
                                           verbose = False, 
                                           lipschitz_k = 0.5, 
                                           covariate = covariate_data, 
                                           lam = 0.8,
                                           gamma = 0.1, 
                                           saving_freq = 2500, 
                                           start_repetition = start_fold, 
                                           stop_repetition = stop_fold,
                                           early_stop_thresh = 0.005)

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Input arguments
    parser.add_argument('--train_data', type=str, required=True,
                        help='Path to the training data CSV file.')
    
    parser.add_argument('--covariate_data', type=str, required=True,
                        help='Path to the covariate data CSV file.')

    # Output argument
    parser.add_argument('--output_dir', type=str, required=True,
                        help='Path to the directory for storing results.')

    # Hyperparameter arguments (optional)
    parser.add_argument('--npattern', type=int, default=5,
                        help='Number of clusters for clustering (default: 5).')

    # Training fold/iter arguments
    parser.add_argument('--final_saving_epoch', type=int, default=63000,
                        help='Final saving epoch (default: 63000).')

    parser.add_argument('--start_fold', type=int, required=True,
                        help='Index of the starting fold for cross-validation.')
    
    parser.add_argument('--fold_number', type=int, required=True,
                        help='Total number of folds for cross-validation.')

    args = parser.parse_args()

    # Read data and set hyperparameters
    train_data = pd.read_csv(args.train_data)
    covariate_data = pd.read_csv(args.covariate_data)
    output_dir = args.output_dir
    npattern = args.npattern
    final_saving_epoch = args.final_saving_epoch
    fold_number = args.fold_number
    start_fold = args.start_fold -1
    stop_fold = start_fold + 1 if start_fold != fold_number else fold_number

    # Call your training function
    trainSurrealGAN(train_data,  covariate_data, output_dir, npattern, 
                    final_saving_epoch, start_fold, stop_fold, fold_number)
    
    




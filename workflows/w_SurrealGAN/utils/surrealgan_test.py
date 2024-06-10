#!/usr/bin/env python
import numpy as np
import pandas as pd
import argparse
from SurrealGAN import Surreal_GAN_representation_learning as sgr
import os

def testSurrealGAN(in_data, in_covar, model, epoch, out_csv):

    ## Read data
    df_data = pd.read_csv(in_data)
    df_covar = pd.read_csv(in_covar)

    ## Apply testing
    rindex = sgr.apply_saved_model(model, df_data, epoch, df_covar) 

    # Write results
    dfr = pd.DataFrame(data = rindex, columns=['r1','r2','r3','r4','r5'])
    dfr['participant_id'] = df_data['participant_id']
    dfr = dfr[['participant_id','r1','r2','r3','r4','r5']]
    dfr.to_csv(out_csv, index = False)

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Input arguments
    parser.add_argument('--in_data', type=str, required=True,
                        help='Path to the testing data CSV file.')
    
    parser.add_argument('--in_covar', type=str, required=True,
                        help='Path to the covariate data CSV file.')

    parser.add_argument('--model', type=str, required=True,
                        help='Path to pre-trained model.')

    # Output argument
    parser.add_argument('--out_csv', type=str, required=True,
                        help='Path to out file.')

    # Hyperparameter arguments
    # NOTE: set epoch to be the "best epoch" in the "representation_result.csv" file    
    parser.add_argument('--epoch', type=int, default=50000,
                        help='Number of epochs (default: 50000).')

    args = parser.parse_args()

    # Call testing function
    testSurrealGAN(args.in_data,  args.in_covar, args.model, args.epoch, args.out_csv)
    
    




#!/usr/bin/env python
import numpy as np
import pandas as pd
import argparse
from SmileGAN import Smile_GAN_clustering
import os



def trainSmileGAN(train_data, nCluster, output_dir, covariate, start_fold, stop_fold, fold_number):


  start_saving_epoch = 9000
  max_epoch = 15000
  WD = 0.09 # to be changed
  AQ = 50 # to be changed
  cluster_loss = 0.002 # to be changed
  batchsize = 80 # to be changed
  mu = 5 # to be changed, try mu = 1-7

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  Smile_GAN_clustering.cross_validated_clustering(train_data,  nCluster, fold_number, 0.8, start_saving_epoch, max_epoch,output_dir, WD, AQ, cluster_loss, \
        'highest_matching_clustering', lam=9, mu=mu, batchSize=batchsize, verbose= False, \
        beta1 = 0.5, lr = 0.0002, max_gnorm = 100, eval_freq = 10, save_epoch_freq = 10, start_fold = start_fold, stop_fold = stop_fold,  covariate = covariate, check_outlier=True, std_in_WD=False)

  return


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('start_fold') 
  args = parser.parse_args()

  fold_number = 20
  start_fold = int(args.start_fold) - 1
  stop_fold = start_fold + 1 if start_fold != fold_number else fold_number

  train_data = pd.read_csv('./train_data.csv') #to be changed
  covariate_data = pd.read_csv('./train_covariate.csv') #to be changed
  output_dir = './result/' #to be changed
  ncluster = 4 #to be changed

  trainSmileGAN(train_data, ncluster, output_dir, covariate_data, start_fold, stop_fold, fold_number)





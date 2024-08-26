import pandas as pd
import numpy as np
import os
import sys

def prep_surrealgan_data(in_csv, out_demog_csv, out_roi_csv):
    """
    Create surrealgan input df
    """
    
    # Read input file
    df = pd.read_csv(in_csv)

    # Drop missing
    df = df.dropna(subset=['H_MUSE_Volume_4', 'DLICV_baseline'])

    # Select covars
    selVars = ['MRID', 'Age', 'Sex', 'DLICV_baseline', 'target']
    
    # Select rois
    selROIs = [ name for name in df.columns if (name[0:14]=='H_MUSE_Volume_' and int(name[14:])<300) and int(name[14:]) not in [4,11,49,50,51,52]] # selected single ROIs from GM and WM    
    df = df[selVars + selROIs]
    
    # Merge left and right ROIs
    #  This was done by Zhijian in the model for NatureMed paper
    mROIs = []
    for roi in selROIs:
        if int(roi[14:]) in [35,71,72,73,95]: # These five ROIs are not devided in to left and right
            mROIs.append(roi)
    selROIs = [roi for roi in selROIs if int(roi[14:]) not in [35,71,72,73,95]]
    for i in range(len(selROIs)//2):
        mROIs.append('H_MUSE_Volume_' + selROIs[i*2][14:] + '_' + selROIs[i*2+1][14:])
    for i in range(len(selROIs)//2):
        df['H_MUSE_Volume_' + selROIs[i*2][14:] + '_'+selROIs[i*2+1][14:]] = df[selROIs[i*2]] + df[selROIs[i*2+1]]


    # Rename vars 
    #   target -> "diagnosis" 
    #   MRID -> "participant_id" 
    df = df.rename(columns = {'MRID':'participant_id', 'target':'diagnosis'})
    #df = df.rename(columns = {'target':'diagnosis'})
    
    # Update values
    df['Sex'] = df.Sex.map({'F':0, 'M':1})

    # Create out csvs
    dfr = df[['participant_id','diagnosis'] + mROIs].reset_index(drop=True) # ROI dataframe
    # covariate dataframe: sex and DLICV (note that age is not a covariate for aging)
    dfd = df[['participant_id', 'diagnosis', 'Sex', 'DLICV_baseline']].reset_index(drop=True) 

    # Write out files
    dfd.to_csv(out_demog_csv, index=False)
    dfr.to_csv(out_roi_csv, index=False)

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 4:
        print("Error: Please provide all required arguments")
        print("Usage: python prep_df_surrealgan.py in_csv.csv out_csv.csv")
        sys.exit(1)

    in_csv = sys.argv[1]
    out_demog_csv = sys.argv[2]
    out_roi_csv = sys.argv[3]

    # Call the function
    prep_surrealgan_data(in_csv, out_demog_csv, out_roi_csv)

    print("Data prep complete! Output file:", out_roi_csv)


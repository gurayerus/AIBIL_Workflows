import pandas as pd
import argparse
import json
import sys

def prep_data_smilegan(in_csv, out_demog_csv, out_roi_csv):

    """
    Create smilegan input data
    """
    
    # Read input file
    df = pd.read_csv(in_csv)

    # Edit demog columns
    df = df.rename(columns = {'MRID':'participant_id', 'DX_Binary':'diagnosis'})
    df.diagnosis = df.diagnosis.map({'AD':1, 'MCI':1, 'CN':-1})
    df.Sex = df.Sex.map({'F':0, 'M':1})

    # Get demog columns
    dfd = df[['participant_id','diagnosis','Age','Sex']]

    # Get and edit demog columns
    dfr = df.drop(['Age', 'Sex'], axis=1)

    # Write out files
    dfd.to_csv(out_demog_csv, index=False)
    dfr.to_csv(out_roi_csv, index=False)

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 4:
        print("Error: Please provide all required arguments")
        print("Usage: python prep_data_smilegan.py in_csv.csv out_csv.csv")
        sys.exit(1)

    in_csv = sys.argv[1]
    out_demog_csv = sys.argv[2]
    out_roi_csv = sys.argv[3]

    # Call the function
    prep_data_smilegan(in_csv, out_demog_csv, out_roi_csv)

    print("Data prep complete! Output file:", out_roi_csv)


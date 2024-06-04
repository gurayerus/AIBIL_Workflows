import pandas as pd
import argparse
import json
import sys

def select_data_smilegan(in_csv, out_csv):

    """
    Create smilegan input data
    """
    
    # Read input file
    df = pd.read_csv(in_csv)

    # Get demog columns
    df = pd.read_csv(in_csv)
    
    # Get roi columns
    df = pd.read_csv(in_csv)

    # Write out file
    df_out.to_csv(out_csv, index=False)

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 6:
        print("Error: Please provide all required arguments")
        print("Usage: python select_sample.py in_sample.csv in_csv.csv in_vars in_rois.csv out_csv.csv")
        sys.exit(1)

    in_sample = sys.argv[1]
    in_csv = sys.argv[2]
    in_rois = sys.argv[3]
    in_vars = sys.argv[4]
    out_csv = sys.argv[5]

    # Call the function
    select_sample(in_sample, in_csv, in_rois, in_vars, out_csv)

    print("Sample selection complete! Output file:", out_csv)


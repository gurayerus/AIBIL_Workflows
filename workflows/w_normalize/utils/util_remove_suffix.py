import pandas as pd
import argparse
import json
import sys

def remove_suffix(in_csv, rm_suff, out_csv):

    """
    Remove suffix from columns
    """
    
    # Read input file
    df_out = pd.read_csv(in_csv)

    # Convert columns of dataframe to str (to handle numeric ROI indices)
    df_out.columns = df_out.columns.astype(str)

    # Remove suffix from variables
    df_out.columns = df_out.columns.str.replace(rm_suff, '')

    # Write out file
    df_out.to_csv(out_csv, index=False)

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 4:
        print("Error: Please provide all required arguments")
        print("Usage: python remove_suffix.py in_csv.csv rm_suffix out_csv.csv")
        sys.exit(1)

    in_csv = sys.argv[1]
    rm_suff = sys.argv[2]
    out_csv = sys.argv[3]

    # Call the function
    remove_suffix(in_csv, rm_suff, out_csv)

    print("Suffix removed! Output file:", out_csv)


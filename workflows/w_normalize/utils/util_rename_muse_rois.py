import pandas as pd
import argparse
import json
import sys

def rename_muse_rois(in_csv, in_dict, out_csv):

    """
    Rename columns of input csv using the muse input dictionary
     - in_dict: list of variables with columns Index (current name) and Name (new name)
     - Note: remove repeat ROIs (those in both single and composite ROIs)
    """
    
    # Read input files
    df = pd.read_csv(in_csv)
    dfd = pd.read_csv(in_dict)

    # Convert columns of dataframe to str (to handle numeric ROI indices)
    df.columns = df.columns.astype(str)
    
    # Create dictionary for variables
    dfd.Index = dfd.Index.astype(str)
    vdict = dfd.set_index('Index')['Name'].to_dict()

    # Rename ROIs
    df_out = df.rename(columns = vdict)

    # Drop duplicate columns in MUSE ROIs (ROIs repeated in single and composite ROI list)
    df_out = df_out.loc[:, df_out.columns.duplicated()==False]

    # Write out file
    df_out.to_csv(out_csv, index=False)

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 4:
        print("Error: Please provide all required arguments")
        print("Usage: python rename_columns.py in_csv.csv in_dict.csv out_csv.csv")
        sys.exit(1)

    in_csv = sys.argv[1]
    in_dict = sys.argv[2]
    out_csv = sys.argv[3]

    # Call the function
    rename_muse_rois(in_csv, in_dict, out_csv)

    print("Renaming of muse rois complete! Output file:", out_csv)


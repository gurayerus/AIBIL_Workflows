import pandas as pd
import argparse
import json
import sys

def select_vars(in_csv, in_rois, in_vars, out_csv):

    """
    Select variables from data file
    """
    
    # Read input files
    df = pd.read_csv(in_csv)
    dfr = pd.read_csv(in_rois)

    # Convert columns of dataframe to str (to handle numeric ROI indices)
    df.columns = df.columns.astype(str)

    # Get variable lists (input var list + rois)
    in_vars = in_vars.split(',')
    roi_vars = dfr.Name.astype(str).tolist()
    
    # Remove duplicate vars (in case a variable is both in roi list and input var list)
    in_vars = [x for x in in_vars if x not in roi_vars]

    # Make a list of selected variables
    sel_vars = in_vars + roi_vars 

    # Remove vars that are not in the dataframe
    df_vars = df.columns.tolist()
    sel_vars = [x for x in sel_vars if x in df_vars]
    
    # Select variables
    df_out = df[sel_vars]

    # Drop duplicate columns in MUSE ROIs (ROIs repeated in single and composite ROI list)
    df_out = df_out.loc[:, df_out.columns.duplicated()==False]

    # Write out file
    df_out.to_csv(out_csv, index=False)

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 5:
        print("Error: Please provide all required arguments")
        print("Usage: python select_vars.py in_csv.csv in_rois.csv in_vars out_csv.csv")
        sys.exit(1)

    in_csv = sys.argv[1]
    in_rois = sys.argv[2]
    in_vars = sys.argv[3]
    out_csv = sys.argv[4]

    # Call the function
    select_vars(in_csv, in_rois, in_vars, out_csv)

    print("Selection of variables complete! Output file:", out_csv)


import pandas as pd
import numpy as np
import argparse
import json
import sys

def edit_sample(in_csv, out_csv):

    """
    Custom edits to prepare harmonization train set
    """
    
    # Read input file
    df = pd.read_csv(in_csv, dtype = {'MRID':str, 'participant_id':str})
    
    # Add SITE column
    df.insert(4, 'SITE', 'ISTAGAging')
    df['SITE'] = np.random.choice(['Site1','Site2','Site3','Site4'], size = df.shape[0])


    # Rename ROIs
    df.columns = df.columns.str.replace('H_', '')
    
    # Select columns
    selcols = ['MRID', 'Age', 'Sex', 'SITE', 'DLICV'] + df.columns[df.columns.str.contains('MUSE')].tolist()
    df = df[selcols]

    # Convert sex to num
    df.Sex = df.Sex.map({'F':0, 'M':1})

    
    # Write out file
    df.to_csv(out_csv, index=False)

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 3:
        print("Error: Please provide all required arguments")
        print("Usage: python edit_sample.py in_csv.csv out_csv.csv")
        sys.exit(1)

    in_csv = sys.argv[1]
    out_csv = sys.argv[2]

    # Call the function
    edit_sample(in_csv, out_csv)

    print("Sample editing complete! Output file:", out_csv)


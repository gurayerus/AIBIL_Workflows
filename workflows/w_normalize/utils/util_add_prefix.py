import pandas as pd
import argparse
import json
import sys

def add_prefix(in_csv, prefix, out_csv):

    """
    Custom edits to prepare harmonization test set
    """
    
    # Read input file
    df = pd.read_csv(in_csv, dtype = {'MRID':str})
    
    # Add prefix
    df = df.add_prefix(prefix)

    # Rename MRID and ICV columns
    df = df.rename(columns = {prefix + 'MRID':'MRID', prefix + '702':'DLICV'})

    # Write out file
    df.to_csv(out_csv, index=False)

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 4:
        print("Error: Please provide all required arguments")
        print("Usage: python add_prefix.py in_csv.csv prefix out_csv.csv")
        sys.exit(1)

    in_csv = sys.argv[1]
    prefix = sys.argv[2]
    out_csv = sys.argv[3]

    # Call the function
    add_prefix(in_csv, prefix, out_csv)

    print("Add prefix complete! Output file:", out_csv)


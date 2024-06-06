import pandas as pd # should be 1.2 or higher
import numpy as np
import os
import sys

def filter_mri(in_csv, out_csv):

    ## Read data
    df = pd.read_csv(in_csv, dtype = {'MRID':str, 'PTID':str})

    ## Drop mrid null
    dfout = df[df.MRID.isna()==False]

    ## Write output
    dfout.to_csv(out_csv, index = False)

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 3:
        print("Error: Please provide all required arguments")
        print("Usage: python util_filter_mri.py in.csv out.csv")
        sys.exit(1)

    in_csv = sys.argv[1]
    out_csv = sys.argv[2]

    # Call the function
    filter_mri(in_csv, out_csv)

    print("Filtering complete! Output file:", out_csv)


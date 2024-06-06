import pandas as pd # should be 1.2 or higher
import numpy as np
import os
import sys

def pkl_to_csv(in_pkl, out_csv):

    ## Read data
    df = pd.read_pickle(in_pkl)

    ## Write output
    df.to_csv(out_csv, index = False)


if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 3:
        print("Error: Please provide all required arguments")
        print("Usage: python util_pkl_to_csv.py in.csv out.csv")
        sys.exit(1)

    in_csv = sys.argv[1]
    out_csv = sys.argv[2]

    # Call the function
    pkl_to_csv(in_csv, out_csv)

    print("Conversion complete! Output file:", out_csv)


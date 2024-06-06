import pandas as pd # should be 1.2 or higher
import numpy as np
import os
import sys

def sel_vars(in_pkl, out_csv):

    ## Read data
    df = pd.read_csv(in_csv, dtype = {'MRID':str, 'PTID':str})

    ## Sel vars
    selvars = ['MRID', 'PTID', 'Date', 'participant_id', 'Visit_Code', 'Phase', 'Age', 'Sex', 'Study', 'Delta_Baseline', 'Education_Years', 'APOE_Genotype', 
            'APOE4_Alleles', 'Race', 'Ethnicity', 'Diagnosis', 'DX_Binary']
    selroi = df.columns[df.columns.str.contains('MUSE')].tolist()
    selicv = df.columns[df.columns.str.contains('ICV')].tolist()

    dfout = df[selvars + selicv + selroi]

    ## Write output
    dfout.to_csv(out_csv, index = False)


if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 3:
        print("Error: Please provide all required arguments")
        print("Usage: python util_sel_vars.py in.csv out.csv")
        sys.exit(1)

    in_csv = sys.argv[1]
    out_csv = sys.argv[2]

    # Call the function
    sel_vars(in_csv, out_csv)

    print("Selection complete! Output file:", out_csv)


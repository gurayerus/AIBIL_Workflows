import pandas as pd
import sys

def merge_two(in1_csv, in2_csv, key_var, out_csv):
    """
    Merge two input data files
    Output data includes an inner merge
    """
    
    # Read csv files
    df1 = pd.read_csv(in1_csv)
    df2 = pd.read_csv(in2_csv)

    # Merge DataFrames
    #  Duplicate columns are discarded
    df_out = df1.merge(df2, on = key_var, suffixes = ['', '_tmpremovedupl'])
    df_out = df_out[df_out.columns[df_out.columns.str.contains('_tmpremovedupl')==False]]

    # Write out file
    df_out.to_csv(out_csv, index=False)

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 5:
        print("Error: Please provide all required arguments")
        print("Usage: python merge_two.py in1_csv.csv in2_csv.csv key_var out_csv.csv")
        sys.exit(1)

    in1_csv = sys.argv[1]
    in2_csv = sys.argv[2]
    key_var = sys.argv[3]
    out_csv = sys.argv[4]

    # Call the function
    merge_two(in1_csv, in2_csv, key_var, out_csv)

    print("Merge complete! Output file:", out_csv)

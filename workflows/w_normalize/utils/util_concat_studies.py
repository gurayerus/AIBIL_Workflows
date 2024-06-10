import pandas as pd
import sys

def concat_data(out_csv, list_in_csv):
    """
    Concat multiple input data files
    Output data includes only common variables to all files
    """
    list_df = []
    col_common = []
    for i, in_csv in enumerate(list_in_csv):
        # Read csv files
        df_tmp = pd.read_csv(in_csv)
        list_df.append(df_tmp)

        # Detect common columns
        col_tmp = df_tmp.columns
        if i == 0:
            col_common = df_tmp.columns.tolist()
        col_common = [x for x in df_tmp.columns if x in col_common]

    # Concat data
    df_out = pd.concat(list_df)

    df_out = df_out[col_common]

    # Write out file
    df_out.to_csv(out_csv, index=False)

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) < 4:
        print("Error: Please provide all required arguments")
        print("Usage: python merge_data.py out_csv.csv in_csv1.csv in_csv2.csv ...")
        sys.exit(1)

    out_csv = sys.argv[1]
    list_in_csv = sys.argv[2:]

    # Call the function
    #print(list_in_csv[0])
    #print('BBB')
    concat_data(out_csv, list_in_csv)

    print("Concat complete! Output file:", out_csv)

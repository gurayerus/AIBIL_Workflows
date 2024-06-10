import pandas as pd
import sys

def merge_data(out_csv, key_var, list_in_csv):
    """
    Merge multiple input data files
    Output data includes an inner merge
    """
    
    df_out = pd.read_csv(list_in_csv[0])
    for i, in_csv in enumerate(list_in_csv[1:]):
        # Read csv files
        df_tmp = pd.read_csv(in_csv)
        df_tmp = df_tmp[df_tmp[key_var].isna()==False]

        # Merge DataFrames
        df_out = df_out.merge(df_tmp, on = key_var)

    # Write out file
    df_out.to_csv(out_csv, index=False)

if __name__ == "__main__":
  # Access arguments from command line using sys.argv
  if len(sys.argv) < 4:
      print("Error: Please provide all required arguments")
      print("Usage: python merge_data.py out_csv.csv key_var in_csv1.csv,in_csv2.csv,...")
      sys.exit(1)

  out_csv = sys.argv[1]
  key_var = sys.argv[2]
  list_in_csv = sys.argv[3:]
  
  # Call the function
  merge_data(out_csv, key_var, list_in_csv)

  print("Merge complete! Output file:", out_csv)

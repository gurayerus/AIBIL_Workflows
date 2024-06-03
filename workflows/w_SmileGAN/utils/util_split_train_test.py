import pandas as pd
from sklearn.model_selection import train_test_split
import sys

def split_train_test(in_csv, strat_vars, test_ratio, out_train, out_test):
    """
    Merge two input data files
    Output data includes an inner merge
    """
    
    ## Read data
    df = pd.read_csv(in_csv)
    
    ## Check stratification variables
    df_vars = df.columns.tolist()
    strat_vars = [x for x in strat_vars if x in df_vars]
    
    ## Check if stratification variables are categorical (only binary vars included)
    strat_vars = [x for x in strat_vars if df[x].unique().shape[0]==2]
    
    print('-------------------------------------')
    print(in_csv)
    print(strat_vars)
    print('-------------------------------------')
    
    if len(strat_vars) == 0:
        df_tr, df_te = train_test_split(df, test_size = test_ratio)
    else:
        df_tr, df_te = train_test_split(df, test_size = test_ratio, stratify = df[strat_vars])
        
    # Write out file
    df_tr.to_csv(out_train, index=False)
    df_te.to_csv(out_test, index=False)    

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 6:
        print("Error: Please provide all required arguments")
        print(len(sys.argv))
        print("Usage: python split_train_test.py in_csv.csv strat_vars out_tr.csv out_te.csv")
        sys.exit(1)

    in_csv = sys.argv[1]
    strat_vars = sys.argv[2]
    test_ratio = float(sys.argv[3])
    out_train = sys.argv[4]
    out_test = sys.argv[5]

    if strat_vars == 'NONE':
        strat_vars = []
    else:
        strat_vars = strat_vars.split(',')

    # Call the function
    split_train_test(in_csv, strat_vars, test_ratio, out_train, out_test)

    print("Data split complete! Output file:", out_train)

import pandas as pd
import numpy as np
import sys
from sklearn.metrics import roc_auc_score

def eval_spare(in1_csv, in2_csv, target_var, out_csv):
    """
    Merge two input data files
    Output data includes an inner merge
    """
    
    key_var = 'MRID'
    pred_var = 'SPARE_score'
    
    # Read csv files
    df1 = pd.read_csv(in1_csv)
    df2 = pd.read_csv(in2_csv)
    
    df1 = df1[[key_var, target_var]]
    df2 = df2[[key_var, pred_var]]

    # Merge DataFrames
    #df_tmp = df1.merge(df2, on = key_var, suffixes = ['_init', '_pred'])
    df_tmp = df1.merge(df2, on = key_var)

    # Calculate score
    num_label = df1[target_var].unique().shape[0]
    num_sample = df1.shape[0]
    v1 = np.array(df_tmp[target_var].astype(float))
    v2 = np.array(df_tmp[pred_var].astype(float))
    
    ## Classification metrics
    if num_label == 2:      
        v2_bin = (v2>0).astype(float)
        acc = float((v1==v2_bin).sum()) / num_sample
        
        auc = roc_auc_score(v1, v2)        

        df_out = pd.DataFrame({'Accuracy':[acc], 'AUC':[auc]})

    ## Regression metrics
    else:      
        corr = np.corrcoef(v1, v2)[0,1]
        
        mae = (np.abs(v1 - v2)).mean()
        
        df_out = pd.DataFrame({'Corr':[corr], 'MAE': [mae]})

    # Write out file
    df_out.to_csv(out_csv, index=False)

if __name__ == "__main__":
    # Access arguments from command line using sys.argv
    if len(sys.argv) != 5:
        print("Error: Please provide all required arguments")
        print("Usage: python eval_spare.py in1_csv.csv in2_csv.csv target_var out_csv.csv")
        sys.exit(1)

    in1_csv = sys.argv[1]
    in2_csv = sys.argv[2]
    target_var = sys.argv[3]
    out_csv = sys.argv[4]

    # Call the function
    eval_spare(in1_csv, in2_csv, target_var, out_csv)

    print("Evaluation complete! Output file:", out_csv)

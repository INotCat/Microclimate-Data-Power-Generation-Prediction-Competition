import pandas as pd

def create_x_sequences(df: pd.DataFrame, n_past)-> list:
    if len(df) < n_past:
        print("ERROR: sliding window cannot be applied")
        return
        
    X = []
    L = len(df)
    for i in range(L - n_past + 1):
        if(i + n_past >= L): 
            break
        x_window = df.iloc[i : i + n_past].values  # Input window

        X.append(x_window)

    # if len(X) != n_past:
    #     print("ERROR: input X number not 50 days")
    #     return
    
    return X




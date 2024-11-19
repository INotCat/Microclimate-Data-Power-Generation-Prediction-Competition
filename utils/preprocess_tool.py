from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
from datetime import date
from itertools import tee
from copy import deepcopy as dc

#if wanna 10 mintues
def convert_to_every10mins(df: pd.DataFrame) -> pd.DataFrame:
    """
        Turn to 10 minutes
    """
    df['DateTime'] = pd.to_datetime(df['DateTime'])        
    df.set_index('DateTime', inplace=True)
    df_resampled = df.resample('10min').mean()
    df_resampled.dropna(inplace=True)
        
    # Reset index to move DateTime out of the index and make it a column again
    #df_resampled.reset_index(inplace=True)
    
    return df_resampled


def normalize(df: pd.DataFrame) -> pd.DataFrame :
    """
        Format and normalize numerical columns in a list of numpy arrays.
    """
    exclude_cols = ['DateTime', 'Power(mW)']
    
    cols_to_normalize = [col for col in df.columns if col not in exclude_cols]
    scaler = MinMaxScaler()
    
    df[cols_to_normalize] = scaler.fit_transform(df[cols_to_normalize])
    
    return df


def split_by_location(df: pd.DataFrame, location_col: str = 'LocationCode') -> dict[int, pd.DataFrame]:
    if location_col not in df.columns:
        raise ValueError(f"Column '{location_col}' not found in the DataFrame.")
    
    # Group by the location column and create a dictionary of DataFrames
    location_dfs = {loc: group_df.reset_index(drop=True) for loc, group_df in df.groupby(location_col)}
    
    return location_dfs


def split_by_day(df: pd.DataFrame, mode='10min') -> dict[date, pd.DataFrame]:
    day_dict = {}
    
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['Date'] = df['DateTime'].dt.date #new column store date only
    
    
    
    # Group by the extracted date and store in the dictionary
    for date, group in df.groupby('Date'):
        day_dict[date] = group.drop(columns=['Date'])
    
    
    ###convert to 10minus version
    if mode == '10min':
        for date, group in day_dict.items():
            day_dict[date] = convert_to_every10mins(group)#.drop(columns=['DateTime'])
    else:
        for date, group in day_dict.items():     
            day_dict[date] = group.drop(columns=['DateTime'])
            pass
            
    return day_dict  

def get_9am_window(dt):
        if dt.time() >= pd.Timestamp('09:00:00').time():
            return dt.date()  # Use today's date for 9 AM to midnight
        else:
            return (dt - pd.Timedelta(days=1)).date()  # Use previous day's date for 12:00 AM to 8:59 AM


def split_by_9am_to_next_9am(df: pd.DataFrame, mode='10min') -> dict:

    day_dict = {}
    
    # Ensure DateTime column is in datetime format
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.sort_values('DateTime', inplace=True)  # Ensure data is sorted by time
    
    
    # Group data by 9 AM windows
    df['9am_window'] = df['DateTime'].apply(get_9am_window)
    for window_start, group in df.groupby('9am_window'):
        day_dict[window_start] = group.drop(columns=['9am_window'])
    
    # Optional: Convert to 10-minute intervals or drop columns
    if mode == '10min':
        for date, group in day_dict.items():
            day_dict[date] = convert_to_every10mins(group)
    else:
        for date, group in day_dict.items():
            day_dict[date] = group

    return day_dict

def pairwise(df: dict):
    
    df_next = df.copy()
    


def split_by_XY(df: pd.DataFrame)-> list[pd.DataFrame]:
    
    
    X = df.iloc[:, :-1] #deep copy?
    Y = df.iloc[:, -1:]
    return X, Y

def create_sequences(df_X: pd.DataFrame, df_Y: pd.DataFrame , n_past, n_predict): 
    ###
    if len(df_X) < (n_past):
        #print('lower than')
        return 

    X,Y = [],[]
    L = len(df_X)
    for i in range(L - n_past + 1):
        x_window = df_X.iloc[i : i + n_past].values  # Input window
        y_window = df_Y.iloc[i : i + n_predict].values  # Output targets

        if(len(x_window) == len(y_window)): ##do not know why it would 60,59,60,60
            X.append(x_window)
            Y.append(y_window)

    return X, Y
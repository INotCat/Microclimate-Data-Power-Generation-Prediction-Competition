import os
import pandas as pd
from datetime import datetime, timedelta
def read_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def read_all_csvs(directory: str) -> pd.DataFrame:
    csv_files = sorted(
        [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]
    )
    
    # Combine all CSV files into a single DataFrame
    data_frames = [pd.read_csv(file) for file in csv_files]
    combined_df = pd.concat(data_frames, ignore_index=True)
    
    return combined_df

def format_date(date):
    """
    將日期從簡化形式 (如 "0101") 格式化為完整日期格式 (如 "2024-01-01")
    """
    return f"2024-{date[:2]:0>2}-{date[2:]:0>2}"


def filter_data_by_date(path, loc, date):
    """
    從 path(csv) 取得 dataframe，篩選指定日期上午 9 點後至隔天上午 9 點前的數據，並將 LocationCode 設為索引。
    @param date : 日期 (格式如 "0101")
    @return : 如果篩選後的 dataframe 為 empty，返回 tuple(loc, date) (string, string)
              否則返回 tuple(loc, dataframe) (int, df)
    """
    try:
        # 檢查檔案是否存在
        if not os.path.exists(path):
            print(f"File {path} does not exist.")
            return (f"{loc}", f"{date}")

        data = pd.read_csv(path)

        # 格式化日期和計算範圍
        formatted_date = format_date(date)  # 將 "0101" 格式化為 "2024-01-01"
        start_time = datetime.strptime(formatted_date, "%Y-%m-%d") + timedelta(hours=9)
        end_time = start_time + timedelta(days=1)

        # 確保 DateTime 欄位為 datetime 格式
        data['DateTime'] = pd.to_datetime(data['DateTime'])

        # 過濾符合條件的行
        filtered_df = data[(data['DateTime'] >= start_time) & (data['DateTime'] < end_time)]

        # 設定 LocationCode 為索引，保留 DateTime 欄位
        if not filtered_df.empty:
            filtered_df.set_index('LocationCode', inplace=True, drop=False)
            print(filtered_df)
            return (int(loc), filtered_df)
        else:
            return (f"{loc}", f"{date}")  # 如果沒有找到，返回 loc 和日期
    except Exception as e:
        print(f"Error processing file {path}: {e}")
        return (f"{loc}", f"{date}")
    
    
def process_filter_data(root_path, location_to_days) -> list:
    '''
    @param ROOT_PATH : csv datas' root
    @param location_to_days : loc mapping to date
    
    '''
    targets = []
    
    if not os.path.exists(root_path):
        print(f"Root path {root_path} does not exist.")

    for loc, dates in location_to_days.items():
        print(f"loc : {loc}")
        # make full path
        loc_str = int(loc)
        path = f"L{loc_str}_Train.csv"
        file_path = os.path.join(root_path, path) 
        # check exist
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist. Skipping...")
            continue
        # get filtered data
        for date in dates:
            result = filter_data_by_date(file_path, loc, date)
            targets.append(result)
        
    return targets
            # deal with result

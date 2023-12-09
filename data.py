import pandas as pd
import pyarrow
import os

# Extract the info I want out of the dicts in the df
def extract_value(data:dict, key:str):
    return data.get(key)

def check_same_headings():
    previous = None
    # Loop through each data file
    for i in os.listdir('wejo/2022-08-19'):
        for j in os.listdir('wejo/2022-08-19/' + i):
            # Get each file
            df = pd.read_parquet('wejo/2022-08-19/' + i + '/' + j, engine='pyarrow')
            if previous is not None and previous != df.columns.to_list():
                # Extract the data I want
                print('Differing data header at wejo/2022-08-19/' + i + '/' + j)
                break
            else:
                previous = df.columns.to_list()
    print(f'All data has same headings: {previous}')

def combine_data():
    columns = ['time', 'speed', 'latitude', 'longitude']

    my_data = pd.DataFrame(columns=columns)
    # Loop through each data file
    for i in os.listdir('wejo/2022-08-19'):
        for j in os.listdir('wejo/2022-08-19/' + i):
            # Get each file
            df = pd.read_parquet('wejo/2022-08-19/' + i + '/' + j, engine='pyarrow')
            temp = pd.DataFrame(columns=columns)
            # Pull out the data I want
            temp['time'] = df['capturedTimestamp']
            temp['speed'] = df['metrics'].apply(lambda x: extract_value(x, 'speed'))
            temp['latitude'] = df['location'].apply(lambda x: extract_value(x, 'latitude'))
            temp['longitude'] = df['location'].apply(lambda x: extract_value(x, 'longitude'))
            # Add the data to the running list
            my_data = pd.concat([my_data, temp], ignore_index=True)
            
    my_data.to_parquet('TotalDataAug19.parquet', engine='pyarrow')

df = pd.read_parquet('wejo/TotalDataAug19.parquet', engine='pyarrow')
print(df.tail(10))
print(df['speed'].max())
print('Zeroes in speed:', (df['speed'] == 0).sum())
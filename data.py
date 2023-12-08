import pandas as pd
import pyarrow
import io

#Extract the info I want out of the dicts in the df
def extract_value(data:dict, key:str):
    return data.get(key)

#Just using this file to play with the data
test_data = pd.read_parquet('wejo\part-00007-tid-3851099292331252689-9e71c5e6-c05e-4508-b8c6-abb52c06c814-9855-1.c000.gz.parquet', engine='pyarrow')
test_data = test_data.iloc[0:5]
test_data.drop(columns=['journeyId', 'status', 'event'], axis=1, inplace=True)
test_data['latitude'] = test_data['location'].apply(lambda x: extract_value(x, 'latitude'))
print(test_data.size)
print(test_data.columns)
print(test_data.head())
print(test_data.iloc[0]['location'].get('latitude'))

test_data.to_csv('TEST.csv')
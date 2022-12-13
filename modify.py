import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d  
import sklearn
from tqdm import tqdm
import os
from text_preprocessing import preprocess_text
from numpy import save
from numpy import load
df = pd.read_csv("./dataset_modified/Bus Arrival Departure Times Apr-June 2020.csv")


df = df.drop(df.columns[[0]],axis = 1)
df = df[ df['time_point_id'].astype(str).str.contains('nuniv') == True]
print(df.info())
df.to_csv('./dataset_filtered/Bus Arrival Departure Times Apr-June 2020.csv', index=None)

"""
with pd.read_csv("./dataset_modified/Bus Arrival Departure Times Apr-June 2020.csv", chunksize=1000) as reader:
    reader 
    for chunk in reader: 
        chunk = chunk[chunk.drop(df.columns[[0]],axis = 1)]
        chunk = chunk[chunk['time_point_id'].astype(str).str.contains('nuniv') == True]
        df = pd.concat([df, chunk ])

print(df.head())
#save('./dataset_filtered/Bus Arrival Departure Times Apr-June 2020.npy', df)
df.to_csv('./dataset_filtered/Bus Arrival Departure Times Apr-June 2020.csv')
"""



""" 
def saveDataFrame(data_temp):
    
    path = "./dataset/MBTA_Rapid_Transit_Headways_2020_2.csv"
    if os.path.isfile(path):
        with open(path, 'a') as f:
            data_temp.to_csv(f, header=False)
    else:
        data_temp.to_csv(path, index=False)
        
# Define chunksize
chunk_size = 10**3
# Read and process the dataset in chunks
for chunk in tqdm(pd.read_csv("./dataset/MBTA_Rapid_Transit_Headways_2020.csv", chunksize=chunk_size)):
    preprocessed_review = preprocess_text(chunk['review'].values)
    
    saveDataFrame(pd.DataFrame({'preprocessed_review':preprocessed_review, 
                                'target':chunk['target'].values
                               }))
"""

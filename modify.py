import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d  
import sklearn
from tqdm import tqdm
import os
from text_preprocessing import preprocess_text

df = pd.read_csv("./dataset/Bus Arrival Departure Times Oct-Dec 2020.csv", nrows=1)

with pd.read_csv("./dataset/Bus Arrival Departure Times Oct-Dec 2020.csv", chunksize=1000) as reader:
    reader 
    for chunk in reader: 
        chunk = chunk[chunk['Route'].astype(str).str.contains('39') == True]
        df = pd.concat([df, chunk ])

print(df.head())

df.to_csv('./dataset_modified/Bus Arrival Departure Times Oct-Dec 2020.csv')

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

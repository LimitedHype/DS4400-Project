import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd
import os

def calc_delta(df): 
    df['scheduled'] = pd.to_datetime(df['scheduled'])
    df['actual'] = pd.to_datetime(df['actual'])
    df['actual'] = (df['actual'] - df['actual'].dt.normalize()).dt.total_seconds()
    df['scheduled'] = (df['scheduled'] - df['scheduled'].dt.normalize()).dt.total_seconds()
    df = df.assign(delta = abs(df.scheduled - df.actual))
    #for _, row in df.iterrows():
        #row['delta'] = abs(row['scheduled'] - row['actual'])
    print(df['delta'])

import pandas as pd
import numpy as np

weather = pd.read_csv('../dataset_filtered/weather.csv')

# Serivce Date => Day of Year mod 365
# Time Actual
#input = current time, weather, location,



# We modify the original weather dataframe such that we invoke the datetime conversion on the ['day'] column
def relabel_weather(weather_df): 
    weather_df['day'] = weather_df['day'].astype(str) + "-2020"
    weather_df['day'] = pd.to_datetime(weather_df['day'])
    weather_df.to_csv(f'../../dataset_filtered/weather.csv', index=None)


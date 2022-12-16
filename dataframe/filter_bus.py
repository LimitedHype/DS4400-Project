import pandas as pd
import numpy as np


apr_june = pd.read_csv('../../dataset_filtered_local/bus_arrival_departure_northeastern_apr_june.csv')
jan_mar = pd.read_csv('../../dataset_filtered_local/bus_arrival_departure_northeastern_jan_mar.csv')
jul_sep = pd.read_csv('../../dataset_filtered_local/bus_arrival_departure_northeastern_jul_sep.csv')
oct_dec = pd.read_csv('../../dataset_filtered/bus_times_q4.csv')
weather = pd.read_csv('../../dataset_filtered/weather.csv')

# Serivce Date => Day of Year mod 365
# Time Actual
#input = current time, weather, location,



def filter_missing_values(df, file_path): 
    df = df.drop(df.columns[[0]],axis = 1)
    df = df[df['scheduled'].notnull() & df['actual'].notnull()]
    print(df.info())
    df.to_csv(f'../../dataset_filtered/{file_path}.csv')


#filter_missing_values(apr_june, "bus_times_q2")
#filter_missing_values(jan_mar, "bus_times_q1")
#filter_missing_values(jul_sep, "bus_times_q3")
filter_missing_values(oct_dec, "bus_times_q4")
def normalize_columns(df=oct_dec, file_path='bus_times_q4'): 
    df = df.rename(columns={"ServiceDate" : "service_date" ,"Route" : "route_id","Direction" : "direction", "HalfTripId" : "half_trip_id","Stop" : "stop_id","Timepoint" : "time_point_id","TimepointOrder" : "time_point_order","PointType" : "point_type","StandardType" : "standard_type","Scheduled" : "scheduled","Actual" : "actual","ScheduledHeadway" :"scheduled_headway" ,"Headway" : "headway"})
    df.to_csv(f'../../dataset_filtered/{file_path}.csv', index=None)

#normalize_columns()
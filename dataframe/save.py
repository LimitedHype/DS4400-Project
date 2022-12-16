import pandas as pd
import numpy as np

import random
RANDOM_SEED = 4400

# Bus Arrival and Departure Time Datasets

sample_frames = ('../datasets/Bus Arrival Departure Times Apr-June 2020.csv', 'apr_june')
jan_mar = ('../datasets/Bus Arrival Departure Times Jan-Mar 2020.csv', 'jan_mar')
jul_sep = ('../datasets/Bus Arrival Departure Times Jul-Sep 2020.csv', 'jul_sep')
oct_dec = ('../datasets/Bus Arrival Departure Times Oct-Dec 2020.csv', 'oct_dec')

# Names
bus_arrival_departure_list = [sample_frames, jan_mar, jul_sep, oct_dec]


def loadDataFrame(path: str, chunksize_: int) -> None:
    print('Loading: ' + str(path))
    new_frames = pd.DataFrame()
    for i, chunk in enumerate(pd.read_csv(path, chunksize=chunksize_)):
        try:
            new_frame = chunk[pd.notnull(chunk.actual)]
            new_frames = pd.concat([new_frames, new_frame])
        except:
            pass
    return new_frames

def loadDataFrameOct(path: str, chunksize_: int) -> None:
    print('Loading: ' + str(path))
    new_frames = pd.DataFrame()
    for i, chunk in enumerate(pd.read_csv(path, chunksize=chunksize_)):
        try:
            new_frame = chunk[pd.notnull(chunk.Actual)]
            new_frame = new_frame.rename(columns={"ServiceDate" : "service_date" ,"Route" : "route_id","Direction" : "direction", "HalfTripId" : "half_trip_id","Stop" : "stop_id","Timepoint" : "time_point_id","TimepointOrder" : "time_point_order","PointType" : "point_type","StandardType" : "standard_type","Scheduled" : "scheduled","Actual" : "actual","ScheduledHeadway" :"scheduled_headway" ,"Headway" : "headway"})
            new_frames = pd.concat([new_frames, new_frame])
        except:
            pass
    return new_frames

# def save_as_numpy(fileName: str, df):
#     new_df = df.to_numpy()
#     np.save(fileName, new_df)

list_of_path_parsed = []

# filter_id = ['nuniv', 'brghm', 'hlong', 'shunt', 'fhill', 'hunbv', 'bbsta', 'jpctr', 'heath']

for path, name in bus_arrival_departure_list:
    if name == 'oct_dec':
        new_dataFrame = loadDataFrameOct(path=path, chunksize_=1000)
    else:
        new_dataFrame = loadDataFrame(path=path, chunksize_=1000)
    print("Saving: " + str(path))
    new_dataFrame.to_csv('../dataset_filtered/bus_arrival_departure_northeastern_' + str(name) + '.csv')
    new_tuple = '../dataset_filtered/bus_arrival_departure_northeastern_' + str(name) + '.csv', 'name'
    list_of_path_parsed.append(new_tuple)

sample_frames = pd.DataFrame()
for path, name in list_of_path_parsed:
    for i, chunk in enumerate(pd.read_csv(path, chunksize=1000)):
        try:
            sample_frame = chunk.sample(frac=0.01, replace=False, random_state=RANDOM_SEED)
            sample_frames = pd.concat([sample_frames, sample_frame])
        except:
            pass

# Convert to DateTime
sample_frames['scheduled'] = pd.to_datetime(sample_frames['scheduled'])
sample_frames['actual'] = pd.to_datetime(sample_frames['actual'])
sample_frames['actual'] = (sample_frames['actual'] - sample_frames['actual'].dt.normalize()).dt.total_seconds()
sample_frames['scheduled'] = (sample_frames['scheduled'] - sample_frames['scheduled'].dt.normalize()).dt.total_seconds()

def calc_delta(df): 
    df['scheduled'] = pd.to_datetime(df['scheduled'])
    df['actual'] = pd.to_datetime(df['actual'])
    actual_df = (df['actual'] - df['actual'].dt.normalize()).dt.total_seconds()
    scheduled_df = (df['scheduled'] - df['scheduled'].dt.normalize()).dt.total_seconds()
    return df.assign(delta = abs(scheduled_df - actual_df))

sample_frames = calc_delta(sample_frames)

# pass in a dataframe, and a file name, and change the service_date datetime object to a date object
def fix_times(df): 
    df['service_date'] = pd.to_datetime(df['service_date'])
    return df

sample_frames = fix_times(sample_frames)

print("Saving sampled frames!")
sample_frames.to_csv('../dataset_filtered/bus_arrival_departure_northeastern_sampled' + '.csv')


import pandas as pd
import numpy as np

import random
RANDOM_SEED = 4400

# Bus Arrival and Departure Time Datasets

apr_june = ('../datasets/Bus Arrival Departure Times Apr-June 2020.csv', 'apr_june')
jan_mar = ('../datasets/Bus Arrival Departure Times Jan-Mar 2020.csv', 'jan_mar')
jul_sep = ('../datasets/Bus Arrival Departure Times Jul-Sep 2020.csv', 'jul_sep')
oct_dec = ('../datasets/Bus Arrival Departure Times Oct-Dec 2020.csv', 'oct_dec')

# Names
bus_arrival_departure_list = [apr_june, jan_mar, jul_sep, oct_dec]

def loadDataFrame(filter_id: str, path: str, chunksize_: int) -> None:
    print('Loading: ' + str(path))
    new_frames = pd.DataFrame()
    for i, chunk in enumerate(pd.read_csv(path, chunksize=chunksize_)):
        try:
            new_frame = chunk[(chunk.time_point_id == filter_id) & (pd.notnull(chunk.actual))]
            new_frames = pd.concat([new_frames, new_frame])
        except:
            pass
    return new_frames

def loadDataFrameOct(filter_id: str, path: str, chunksize_: int) -> None:
    print('Loading: ' + str(path))
    new_frames = pd.DataFrame()
    for i, chunk in enumerate(pd.read_csv(path, chunksize=chunksize_)):
        try:
            new_frame = chunk[(chunk.Timepoint == filter_id) & (pd.notnull(chunk.Actual))]
            new_frame = new_frame.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'})
            new_frames = pd.concat([new_frames, new_frame])
        except:
            pass
    return new_frames

# def save_as_numpy(fileName: str, df):
#     new_df = df.to_numpy()
#     np.save(fileName, new_df)

list_of_path_parsed = []

for path, name in bus_arrival_departure_list:
    if name == 'oct_dec':
        new_dataFrame = loadDataFrameOct(filter_id='nuniv', path=path, chunksize_=1000)
    else:
        new_dataFrame = loadDataFrame(filter_id='nuniv', path=path, chunksize_=1000)
    print("Saving: " + str(path))
    new_dataFrame.to_csv('../dataset_filtered/bus_arrival_departure_northeastern_' + str(name) + '.csv')
    new_tuple = '../dataset_filtered/bus_arrival_departure_northeastern_' + str(name) + '.csv', 'name'
    list_of_path_parsed.append(new_tuple)

sample_frames = pd.DataFrame()
for path, name in list_of_path_parsed:
    for i, chunk in enumerate(pd.read_csv(path, chunksize=1000)):
        try:
            sample_frame = chunk.sample(frac=0.25, replace=False, random_state=RANDOM_SEED)
            sample_frames = pd.concat([sample_frames, sample_frame])
        except:
            pass

print("Saving sampled frames!")
sample_frames.to_csv('../dataset_filtered/bus_arrival_departure_northeastern_sampled' + '.csv')

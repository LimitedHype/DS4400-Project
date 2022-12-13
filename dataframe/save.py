import pandas as pd
import numpy as np

path_one = '../datasets/Bus Arrival Departure Times Apr-June 2020.csv'

def loadDataFrame(filter_id: str, path: str, chunksize_: int) -> None:
    new_frames = pd.DataFrame()
    for chunk in pd.read_csv(path, chunksize=chunksize_):
        new_frame = chunk[chunk.time_point_id == filter_id]
        pd.concat([new_frames, new_frame])
        # print(new_frame)
    return new_frames

def save_as_numpy(fileName: str, df):
    new_df = df.to_numpy()
    np.save(fileName, new_df)

new_dataFrame = loadDataFrame(filter_id='nuniv', path=path_one, chunksize_=1000)
save_as_numpy('../dataset_filtered/bus_arrival_departure_northeastern_april_june', new_dataFrame)

new_dataFrame = loadDataFrame(filter_id='nuniv', path=path, chunksize_=1000)
save_as_numpy('../dataset_filtered/bus_arrival_departure_northeastern_april_june', new_dataFrame)
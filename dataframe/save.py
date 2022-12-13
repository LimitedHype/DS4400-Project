import pandas as pd
import numpy as np

apr_june = ('../datasets/Bus Arrival Departure Times Apr-June 2020.csv', 'apr_june')
jan_mar = ('../datasets/Bus Arrival Departure Times Jan-Mar 2020.csv', 'jan_mar')
jul_sep = ('../datasets/Bus Arrival Departure Times Jul-Sep 2020.csv', 'jul_sep')
oct_dec = ('../datasets/Bus Arrival Departure Times Oct-Dec 2020.csv', 'oct_dec')

bus_arrival_departure_list = [apr_june, jan_mar, jul_sep, oct_dec]

def loadDataFrame(filter_id: str, path: str, chunksize_: int) -> None:
    new_frames = pd.DataFrame()
    for i, chunk in enumerate(pd.read_csv(path, chunksize=chunksize_)):
        try:
            new_frame = chunk[(chunk.time_point_id == filter_id) & (pd.notnull(chunk.actual))]
            new_frames = pd.concat([new_frames, new_frame])
        except:
            pass
    return new_frames

# def save_as_numpy(fileName: str, df):
#     new_df = df.to_numpy()
#     np.save(fileName, new_df)

for month, name in bus_arrival_departure_list:
    new_dataFrame = loadDataFrame(filter_id='nuniv', path=month, chunksize_=1000)
    new_dataFrame.to_csv('../dataset_filtered/bus_arrival_departure_northeastern_' + str(name))

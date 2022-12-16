import pandas as pd
import numpy as np
import datetime as dt
np.set_printoptions(threshold=np.inf)

RANDOM_SEED = 4400
np.random.seed(4400)

sampled_dataframe = pd.read_csv('../dataset_filtered/bus_arrival_departure_northeastern_sampled.csv')
weather_dataframe = pd.read_csv('../dataset_filtered/weather.csv')

time_point_ids = ['nuniv', 'brghm', 'hlong', 'shunt', 'fhill', 'hunbv', 'bbsta', 'jpctr', 'heath', 'bdal', 'copst']


def binary_encoder(sampled_df, weather_df=weather_dataframe):
    features = np.empty((0,312), float)
    labels = []

    for index, row in sampled_df.iloc[1:].iterrows():
        bitmap_years = np.zeros(100)
        bitmap_months = np.zeros(12)
        bitmap_days = np.zeros(31)
        bitmap_hours = np.zeros(24)
        bitmap_minutes = np.zeros(60)
        bitmap_seconds = np.zeros(60)
        time_bitmaps = np.zeros(len(time_point_ids))
        time_point_orders_bitmap = np.zeros(10)

        date_ex = row['service_date']
        weather_row = weather_df.loc[weather_df['day'] == date_ex]
        weather_list = weather_row.values.tolist()[0]
        date_ex = pd.to_datetime(date_ex)
        year = date_ex.year
        bitmap_years[year % 2000 - 1] = 1
        month = date_ex.month
        bitmap_months[month - 1] = 1
        day = date_ex.day
        bitmap_days[day - 1] = 1
        hour = date_ex.hour
        bitmap_hours[hour - 1] = 1
        minute = date_ex.minute
        bitmap_minutes[minute - 1] = 1
        second = date_ex.second
        bitmap_seconds[second - 1] = 1

        time_point_id = row['time_point_id']
        time_point_order = row['time_point_order']
        time_point_orders_bitmap[int(time_point_order) - 1] = 1

        location_index = np.where(time_point_ids == time_point_id)[0]
        time_bitmaps[location_index] = 1
        bitmap_total = np.concatenate((weather_list[1:], time_bitmaps, time_point_orders_bitmap, bitmap_years, bitmap_months, bitmap_days, bitmap_hours, bitmap_minutes, bitmap_seconds))
        features = np.vstack([features, bitmap_total])
        labels = np.append(labels, row['delta'])
    return features, labels

def simple_encoder(sampled_df, weather_df=weather_dataframe):
    time_bitmaps = np.zeros(len(time_point_ids))

    features = np.empty((0,22), float)
    labels = []

    for index, row in sampled_df.iloc[1:].iterrows():
        date_ex = row['service_date']
        weather_row = weather_df.loc[weather_df['day'] == date_ex]
        weather_list = weather_row.values.tolist()[0]
        date_ex = pd.to_datetime(date_ex)
        year = date_ex.year

        month = date_ex.month

        day = date_ex.day

        hour = date_ex.hour

        minute = date_ex.minute

        second = date_ex.second

        time_point_id = row['time_point_id']
        time_point_order = row['time_point_order']

        location_index = np.where(time_point_ids == time_point_id)[0]
        time_bitmaps[location_index] = 1
        features_total = np.concatenate((weather_list[1:], time_bitmaps, [time_point_order], [year], [month], [day], [hour], [minute], [second]))
        features = np.vstack([features, features_total])
        labels = np.append(labels, row['delta'])
    return features, labels

def positional_encoding_fn(list_of_times, L_=6):
    ret_vals = [list_of_times]
    for i in range(L_):
        ret_vals.append(np.sin(2.**i * list_of_times))
        ret_vals.append(np.cos(2.**i * list_of_times))
    return np.concatenate(ret_vals)

def positional_encoder(sampled_df, weather_df=weather_dataframe):
    features = np.empty((0,4008), float)
    labels = []

    for index, row in sampled_df.iloc[1:].iterrows():
        bitmap_years = np.zeros(100)
        bitmap_months = np.zeros(12)
        bitmap_days = np.zeros(31)
        bitmap_hours = np.zeros(24)
        bitmap_minutes = np.zeros(60)
        bitmap_seconds = np.zeros(60)
        time_bitmaps = np.zeros(len(time_point_ids))
        time_point_orders_bitmap = np.zeros(10)

        date_ex = row['service_date']
        weather_row = weather_df.loc[weather_df['day'] == date_ex]
        weather_list = weather_row.values.tolist()[0]
        date_ex = pd.to_datetime(date_ex)
        year = date_ex.year
        bitmap_years[year % 2000 - 1] = 1
        month = date_ex.month
        bitmap_months[month - 1] = 1
        day = date_ex.day
        bitmap_days[day - 1] = 1
        hour = date_ex.hour
        bitmap_hours[hour - 1] = 1
        minute = date_ex.minute
        bitmap_minutes[minute - 1] = 1
        second = date_ex.second
        bitmap_seconds[second - 1] = 1

        time_point_id = row['time_point_id']
        time_point_order = row['time_point_order']
        time_point_orders_bitmap[int(time_point_order) - 1] = 1

        location_index = np.where(time_point_ids == time_point_id)[0]
        time_bitmaps[location_index] = 1
        time_bitmap_total = np.concatenate((time_bitmaps, time_point_orders_bitmap, bitmap_years, bitmap_months, bitmap_days, bitmap_hours, bitmap_minutes, bitmap_seconds))
        weather_bitmaps_total = weather_list[1:]
        time_bitmap_encoded = positional_encoding_fn(time_bitmap_total)
        bitmap_total = np.concatenate((weather_bitmaps_total, time_bitmap_encoded))
        features = np.vstack([features, bitmap_total])
        labels = np.append(labels, row['delta'])
    return features, labels




# Splits data into 80, 10, 10
# https://stackoverflow.com/questions/38250710/how-to-split-data-into-3-sets-train-validation-and-test
def train_validate_test_split(df, train_percent=.8, validate_percent=.1):
    perm = np.random.permutation(df.index)
    m = len(df.index)
    train_end = int(train_percent * m)
    validate_end = int(validate_percent * m) + train_end
    train = df.iloc[perm[:train_end]]
    validate = df.iloc[perm[train_end:validate_end]]
    test = df.iloc[perm[validate_end:]]
    return train, validate, test

train_set, validate_set, test_set = train_validate_test_split(sampled_dataframe)

def save_binary_encoder(train_set, validate_set, test_set):
    print("Saving encoded bitmaps!")
    X_train, Y_train = binary_encoder(train_set)
    np.save('../training_sets/Xtrain_binary_set_data.npy', X_train)
    np.save('../training_sets/Ytrain_binary_set_data.npy', Y_train)

    X_val, Y_val = binary_encoder(validate_set)
    np.save('../training_sets/Xvalidate_binary_set_data.npy', X_val)
    np.save('../training_sets/Yvalidate_binary_set_data.npy', Y_val)

    X_test, Y_test = binary_encoder(test_set)
    np.save('../training_sets/Xtest_binary_set_data.npy', X_test)
    np.save('../training_sets/Ytest_binary_set_data.npy', Y_test)

def save_simple_encoder(train_set, validate_set, test_set):
    print("Saving simple bitmaps!")
    X_train, Y_train = simple_encoder(train_set)
    np.save('../training_sets/Xtrain_simple_set_data.npy', X_train)
    np.save('../training_sets/Ytrain_simple_set_data.npy', Y_train)

    X_val, Y_val = simple_encoder(validate_set)
    np.save('../training_sets/Xvalidate_simple_set_data.npy', X_val)
    np.save('../training_sets/Yvalidate_simple_set_data.npy', Y_val)

    X_test, Y_test = simple_encoder(test_set)
    np.save('../training_sets/Xtest_simple_set_data.npy', X_test)
    np.save('../training_sets/Ytest_simple_set_data.npy', Y_test)

def save_positional_encoder(train_set, validate_set, test_set):
    print("Saving positional bitmaps!")
    X_train, Y_train = positional_encoder(train_set)
    np.save('../training_sets/Xtrain_positional_set_data.npy', X_train)
    np.save('../training_sets/Ytrain_positional_set_data.npy', Y_train)

    X_val, Y_val = positional_encoder(validate_set)
    np.save('../training_sets/Xvalidate_positional_set_data.npy', X_val)
    np.save('../training_sets/Yvalidate_positional_set_data.npy', Y_val)

    X_test, Y_test = positional_encoder(test_set)
    np.save('../training_sets/Xtest_positional_set_data.npy', X_test)
    np.save('../training_sets/Ytest_positional_set_data.npy', Y_test)

save_binary_encoder(train_set, validate_set, test_set)
save_simple_encoder(train_set, validate_set, test_set)
save_positional_encoder(train_set, validate_set, test_set)
# imports for the full pipeline
import numpy as np
import pandas as pd
import pyxdf
from sklearn import linear_model

# import xdf data
# define the name of the stream of interest
stream_name = "pupil_labs_Event"

# load xdf data
path_to_recording = "./lsl_recordings/recorded_xdf_file.xdf"
data, header = pyxdf.load_xdf(path_to_recording, select_streams=[{"name": stream_name}])

# when recording from one device, there will be only one event stream
# extract this stream from the data
event_stream = data[0]

# extract event names and lsl time stamps into a pandas data frames
event_column_name = "name"
event_column_timestamp = "timestamp [s]"

lsl_event_data = pd.DataFrame(columns=[event_column_name, event_column_timestamp])
lsl_event_data[event_column_name] = [name[0] for name in event_stream["time_series"]]
lsl_event_data[event_column_timestamp] = event_stream["time_stamps"]

# import cloud data
path_to_cloud_events = "./cloud_recordings/events.csv"
cloud_event_data = pd.read_csv(path_to_cloud_events)

# transform cloud timestamps to seconds
cloud_event_data[event_column_timestamp] = cloud_event_data["timestamp [ns]"] * 1e-9

# filter events that were recorded in the lsl stream and in cloud
name_intersection = np.intersect1d(
    cloud_event_data[event_column_name], lsl_event_data[event_column_name]
)

# filter timestamps by the event intersection
filtered_cloud_event_data = cloud_event_data[
    cloud_event_data[event_column_name].isin(name_intersection)
]

filtered_lsl_event_data = lsl_event_data[
    lsl_event_data[event_column_name].isin(name_intersection)
]

# fit a linear model
time_mapper = linear_model.LinearRegression()
time_mapper.fit(
    filtered_cloud_event_data[[event_column_timestamp]],
    filtered_lsl_event_data[event_column_timestamp],
)

# use convert gaze time stamps from cloud to lsl time
cloud_gaze_data = pd.read_csv("./cloud_recordings/gaze.csv")

# map from nanoseconds to seconds
cloud_gaze_data[event_column_timestamp] = cloud_gaze_data["timestamp [ns]"] * 1e-9

# predict lsl time in seconds
cloud_gaze_data["lsl_time [s]"] = time_mapper.predict(
    cloud_gaze_data[[event_column_timestamp]]
)

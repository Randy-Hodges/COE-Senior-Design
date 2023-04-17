#!/usr/bin/python3 
#
#
# Desc: Runs all of the different teams code together to recognize targets, map out plane paths, map out the targets
#       and eventually time the payload drop on critical targets. (further implementation details go here)
#
# Warnings:
#
# TODO: 
#  
  
import numpy as np
import cv2
import os
import csv
from csv import writer
import time
import numpy as np
import rasterio 
from crosscorr_screenshot import target_recognition
from map import mapping
from payload_algorithm import calculate_range, calculate_release_point, release_payload
import pandas as pd

# ---------------------------------------

  
if __name__ == "__main__":
    # target recognition 
    target_recognition()

    # mapping function
    target_locations = mapping() # assumes this returns a list of target lats and longs

    for i in range(len(target_locations)):
        target_lat = target_locations[i][0]
        target_long = target_locations[i][1]

        # payload algorithm
        while True:
            mission_data = pd.read_csv('./../Pixhawk Connection/mission_callbacks/mission_callbacks.csv')
            """ Old data format """
            #critical_data = mission_data.drop(columns=['Global Location (relative altitude)', 'Local Location', 'Attitude', 'GPS'])
            #critical_data[['lat', 'long', 'alt']] = mission_data['Global Location'].str.split(',', expand=True)
            #critical_data['lat'] = critical_data['lat'].str.replace('LocationGlobal:lat=', '')
            #critical_data['long'] = critical_data['long'].str.replace('lon=', '')
            #critical_data['alt'] = critical_data['alt'].str.replace('alt=', '')
            #critical_data = critical_data.drop(columns=['Global Location'])
            #critical_data['Velocity'] = critical_data['Velocity'].apply(lambda x: x.strip('[]').split(','))

            """ New data format """
            # fieldnames = ['TIMESTAMP', 'yaw', 'pitch', 'roll', 'ground speed', 'air_speed', 'latitude', 'altitude', 'longitude', 'wind direction', 'wind speed', 'Heartbeat']
            critical_data = mission_data.drop(columns=['yaw', 'pitch', 'roll', 'Heartbeat'])
            critical_data['latitude'] = critical_data['latitude'].str.replace('lat=', '')
            critical_data['longitude'] = critical_data['longitude'].str.replace('lon=', '')
            critical_data['altitude'] = critical_data['altitude'].str.replace('alt=', '')

            x = critical_data['latitude'].iloc[-1]
            y = critical_data['longitude'].iloc[-1]
            v = critical_data['ground_speed'].iloc[-1] # assuming single value
            v_z = 0 # assuming 0
            wind_speed = critical_data['wind speed'].iloc[-1] # assuming single value and head-on
            # future work: depending on how wind_speed is recorded, we may need to account for wind direction if not head-on
            altitude = critical_data['altitude'].iloc[-1]
            time_delay = 2 # time delay in seconds
            R = calculate_range(v, v_z, altitude, wind_speed, time_delay)
            release_point_lat, release_point_long = calculate_release_point(R, target_lat, target_long, x, y)
            release_payload(v, altitude, R, x, y, target_lat, target_long, release_point_lat, release_point_long)
# Python code for Multiple Color Detection
  
  
import numpy as np
import cv2
from payload_algorithm import calculate_range, calculate_release_point, release_payload
from map import mapping
"""Need to import target recognition here"""

  
if __name__ == "__main__":
    # target recognition function goes here
    
    # mapping function
    target_lat, target_long = mapping()

    # payload algorithm
    while True:
        x = pixhawk.get_lat()
        y = pixhawk.get_long()
        v_x = pixhawk.get_vx()
        v_y = pixhawk.get_vy()
        v = np.sqrt(v_x**2 + v_y**2)
        v_z = pixhawk.get_vz()
        wind_speed = pixhawk.get_wind_speed()
        altitude = pixhawk.get_altitude()
        R = calculate_range(v, v_z, altitude, wind_speed)
        release_point_lat, release_point_long = calculate_release_point(R, target_lat, target_long, x, y)
        release_payload(R, x, y, target_lat, target_long, release_point_lat, release_point_long)
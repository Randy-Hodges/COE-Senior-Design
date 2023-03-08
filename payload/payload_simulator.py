from payload_algorithm import calculate_range
from payload_algorithm import calculate_release_point
import numpy as np
import matplotlib.pyplot as plt
""" 
The point of this simulator is to test our drop algorithm against various input conditions (aircraft velocity & position, 
target velocity & position, wind speed).

"""

def payload_ground_hit_location(release_point_lat, release_point_long, target_lat, target_long, altitude, v_x, v_y, wind_speed, wind_direction):
    # re-implement ballistic equation
    # include crosswinds as accelerations in x and y directions
    # wind direction is the angle of attack of the wind relative to the plane (so 0 degrees is head-on, 180 degrees is from the back, etc.)
    # include a slight time delay (i.e. release point lat & long are a bit behind the actual drop locations)
    # include streamer effects?

    # time delay effects (aircraft will be some distance ahead of our release point due to a trigger delay)
    time_delay = 1 # assume 1 second time delay
    release_point_lat = v_y*time_delay + release_point_lat # y is latitude I think
    release_point_long = v_x * time_delay + release_point_long # x is longtidue I think

    # ballistic equation
    rho = 1.225 # kg/m^3 for density of air at sea level
    C_d = 0.3 # just ballparking this, we should experimentally test it though
    A =  2 * np.pi * 0.05 * 0.3 # guessing 10cm in diameter, 30cm in height (forumla for surface area of computer)
    m = 0.5 # roughly half a kilo in weight
    g = 9.8 # m/s^2
    
    q = 0.5 * rho * C_d * A

    h = 0.02
    N = 3000

    t = 0
    R = 0
    n = 0

    while n < N:
        a_x = - q * (v_x ** 2) / m - q * (wind_speed*np.sin(wind_direction)) / m # first term is drag due to airplane speed, second term is drag due to crosswind
        a_y = g -  q * (v_y ** 2) / m  - q * (wind_speed*np.cos(wind_direction)) / m
        v_x += a_x * h
        v_y += a_y * h
        x_temp = x + v_x * h + 0.5 * a_x * (h**2)
        y_temp = y + v_y * h + 0.5 * a_y * (h**2)
        x = x_temp
        y = y_temp
        t += h
    
        if y == altitude:
            R = x
            break

        n +=1

    # return target latitude - Rsintheta, target longitude - Rcostheta
if __name__ == "__main__":
   lat, long = payload_ground_hit_location(args)
   lat_error = target_lat - lat
   long_error = target_long - long

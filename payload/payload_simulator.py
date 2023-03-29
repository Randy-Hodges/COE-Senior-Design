from payload_algorithm import calculate_range
from payload_algorithm import calculate_release_point
import numpy as np
import matplotlib.pyplot as plt
""" 
The point of this simulator is to test our drop algorithm against various input conditions (aircraft velocity & position, 
target velocity & position, wind speed).

"""

def payload_ground_hit_location(release_point_long, target_lat, target_long, altitude, v_x, v_y, wind_speed):
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
    x = 0
    y = 0

    while True:
        a_x = - q * (v_x ** 2) / m - q * (wind_speed ** 2) / m # first term is drag due to airplane speed, second term is drag due to headwind
        a_y = g -  q * (v_y ** 2) / m 
        v_x += a_x * h
        v_y += a_y * h
        x_temp = x + v_x * h + 0.5 * a_x * (h**2)
        y_temp = y + v_y * h + 0.5 * a_y * (h**2)
        x = x_temp
        y = y_temp
        t += h
    
        if y >= altitude*.995:
            R = x
            break

        n +=1

    
    theta = np.arctan(target_long - release_point_long)/(target_lat - target_long)
    ground_hit_long = R * np.cos(theta)
    ground_hit_lat = R * np.sin(theta)

    return ground_hit_lat, ground_hit_long

if __name__ == "__main__":

    long_errors = []
    lat_errors = []
    lats = []
    longs = []
    for i in range(10):
        target_lat = 30
        target_long = 29
        altitude = 100 + 10*i
        v_x = 15
        v_y = 15
        range = calculate_range(v_x, v_y, altitude)
        print(range)
        release_point_lat, release_point_long = calculate_release_point(range, target_long, target_lat, )
        
        
        wind_speed = 0
        wind_direction = 0     # angle in radians

        lat, long = payload_ground_hit_location(release_point_lat, release_point_long, target_lat, target_long, altitude, v_x, v_y, wind_speed, wind_direction)
        #print(long)
        #print(lat)
        #print("")
        lat_error = target_lat - lat
        long_error = target_long - long

        long_errors.append(long_error)
        lat_errors.append(lat_error)


        
    print(long_errors)
    print(lat_errors)
    plt.scatter(lat, long, color="blue")
    plt.scatter(target_long, target_lat, color="red")
    plt.show()
        


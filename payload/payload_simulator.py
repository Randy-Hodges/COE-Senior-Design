from payload_algorithm import calculate_range
from payload_algorithm import calculate_release_point
from payload_algorithm import release_payload_simulator
import numpy as np
import matplotlib.pyplot as plt
import random
""" 
The point of this simulator is to test our drop algorithm against various input conditions (aircraft velocity & position, 
target velocity & position, wind speed).

"""

def payload_ground_hit_location(release_point_lat, release_point_long, target_lat, target_long, altitude, v_x, v_z, wind_speed, time_delay, velocity_error):
    # re-implement ballistic equation
    # include crosswinds as acceleration in the x direction
    # wind direction is the angle of attack of the wind relative to the plane (so 0 degrees is head-on, 180 degrees is from the back, etc.)
    # include a slight time delay (i.e. release point lat & long are a bit behind the actual drop locations)
    # include streamer effects?

    
    # ballistic equation
    rho = 1.225 # kg/m^3 for density of air at sea level
    C_d = 0.3 # just ballparking this, we should experimentally test it though
    A =  0.05 * 0.3 # guessing 10cm in diameter, 30cm in height (frontal surface area)
    m = 0.5 # roughly half a kilo in weight
    g = 9.8 # m/s^2
    
    q = 0.5 * rho * C_d * A

    h = 0.02
    N = 3000

    t = 0
    R = 0
    n = 0
    x = 0
    z = 0

    v_x = v_x * random.uniform(1-velocity_error, 1+velocity_error) #% variation in velocity

    # time delay effects (aircraft will be some distance ahead of our release point due to a trigger delay)
    #time_delay = 1 # assume 1 second time delay
    x = v_x * time_delay 

    terminal_velocity = np.sqrt((2*m*g)/(rho * A * C_d))

    while True:
        #print("X velocity is: ", v_x, "Z velocity is: ", v_z)

        a_x = - q * (v_x ** 2) / m - q * (wind_speed ** 2) / m # first term is drag due to airplane speed, second term is drag due to headwind
        a_z = g -  q * (v_z ** 2) / m 
        if wind_speed > 0 and v_x < 0 and abs(v_x) >= wind_speed: # if there is a headwind and the payload's velocity in that direction is greater than the headwind, set velocity to headwind
            v_x = wind_speed
        else:
            v_x += a_x * h
        if v_z < terminal_velocity:
            v_z += a_z * h
        else:
            v_z = terminal_velocity
        x_temp = x + v_x * h + 0.5 * a_x * (h**2)
        z_temp = z + v_z * h + 0.5 * a_z * (h**2)
        x = x_temp
        z = z_temp
        t += h
    
        if z >= altitude:
            R = x
            #print("Simulator Z is: ", z)
            break

        n +=1


    #theta = np.arccos(np.dot([target_lat, target_long], [release_point_lat, release_point_long])/(np.linalg.norm([target_lat, target_long])*np.linalg.norm([release_point_lat, release_point_long])))  
    #theta = np.arctan(target_long - release_point_long)/(target_lat - release_point_lat)
    r = [target_lat - release_point_lat, target_long - release_point_long] # position vector from release point to target
    theta = np.arctan2(r[1], r[0])
    ground_hit_lat = release_point_lat + R * np.cos(theta)
    ground_hit_long = release_point_long + R * np.sin(theta)
    print("GROUND HIT LAT IS:", ground_hit_lat)
    print("GROUND HIT LONG IS:", ground_hit_long)

    return ground_hit_lat, ground_hit_long

if __name__ == "__main__":

    long_errors = []
    lat_errors = []
    g_lats = [] # ground hit latitudes
    g_longs = [] # ground hit longitudes
    rp_lats = [] # release point latitudes
    rp_longs = [] # release point longitudes
    for i in range(10):
        target_lat = -1
        target_long = 200
        v_x = 0 # x velocity
        v_y = 10 # y velocity
        v_z = 0 # downwards velocity
        v = np.sqrt(v_x**2 + v_y**2) # x and y velocity, assuming plane is on straight path towards target
        x = -1
        y = 0
        z = 55 + 5*i # altitude in meters, which is 200 feet
        wind_speed = np.random.randint(low=0, high=10) # 10 m/s is 22 mph
        wind_speed = 5
        #wind_direction = np.pi/4     # angle in radians
        wind_direction = 0
        time_delay = 2 # assume 1 second time delay
        velocity_error = 0   # 20% variation in velocity
        range = calculate_range(v, v_z, z, wind_speed, time_delay)
        release_point_lat, release_point_long = release_payload_simulator(range, x, y, v_x, v_y, target_lat, target_long)
        

        g_lat, g_long = payload_ground_hit_location(release_point_lat, release_point_long, target_lat, target_long, z, v, v_z, wind_speed, time_delay, velocity_error) # ground hit location lat and long
        lat_error = target_lat - g_lat
        long_error = target_long - g_long

        lat_errors.append(abs(lat_error))
        long_errors.append(abs(long_error))
        g_lats.append(g_lat)
        g_longs.append(g_long)
        rp_lats.append(release_point_lat)
        rp_longs.append(release_point_long)

    print("ALGO RANGE IS:", range)
    print("TARGET LOCATION: (", target_lat, ",", target_long, ")")
    print("RELEASE POINT LOCATION: (", release_point_lat, ",", release_point_long, ")")
    print("GROUND HIT LOCATION: (", g_lat, ",", g_long, ")")
        #print(lat_errors)
    print(long_errors)
    #print the average of long errors
    print(np.median(long_errors))
    print(max(long_errors))
    plt.scatter(g_lats, g_longs, color="blue", label = "Ground Hit Location")
    plt.scatter(rp_lats, rp_longs, color="green", label = "Release Point Location")
    plt.scatter(target_lat, target_long, color="red", label = "Target Location")
    plt.ylim(0,220)
    plt.xlim(-5,5)
    plt.title(label = "Time delay of %d seconds" %time_delay + ", Wind speed of %d m/s" %wind_speed)
    plt.legend()
    plt.show()



import numpy as np

def calculate_range(v_x, v_y, H):
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
        a_x = - q * (v_x ** 2) / m
        a_y = g -  q * (v_y ** 2) / m
        v_x += a_x * h
        v_y += a_y * h
        x_temp = x + v_x * h + 0.5 * a_x * (h**2)
        y_temp = y + v_y * h + 0.5 * a_y * (h**2)
        x = x_temp
        y = y_temp
        t += h
    
        if y >= H*.995:
            R = x
            break

        n +=1
    return R
    

def calculate_release_point(R, T_long, T_lat, P_long):
    theta = np.arctan((T_long - P_long)/(T_lat - T_long))
    release_point_lat = T_lat - R * np.sin(theta)
    release_point_long = T_long - R * np.cos(theta)

    return release_point_lat, release_point_long

def release_payload(R, initial_long, initital_lat, v_x, v_y, target_long, target_lat):
    # send plane along a trajectory determined by vx and vy
    # continually update position, call it p_long and p_lat
    # at each update, run calculate_release_point
    # if p_long ~ release_point_long and p_lat ~ release_point_lat, release payload

    
    x = initial_long
    y = initital_lat
    h = 0.02 # timestep
    for i in range(10000000):
        x += v_x*h
        y += v_y*h
        release_point_lat, release_point_long = calculate_release_point(R, T_long, T_lat, x)
        if (0.95*release_point_long <= x <= 1.05*release_point_long) and (0.95*release_point_lat <= y <= 1.05*release_point_lat):
            return x,y

""" We need to talk with mapping about generating the flight path to the targets. Since this assumes constant altitude and 
aircraft velocity to calculate the release point along the path, we should really only start this program once we're somewhat close
to the target so that error propagation is minimized"""

""" I.e., given a constant trajectory and altitude, this will calculate the best release point along the path"""

""" It's not *precisely* the aircraft's velocity that matters when the calcs are run, but rather what the velocity of the aircraft will be when 
the payload is released. That is what drives the release point calculations. A constant velocity is a simplifying assumption, but not
completely necessary."""

if __name__ == "__main__":

    # placeholder
    x = pixhawk.x_pos
    y = pixhawk.y_pos
    v_x = pixhawk.x_vel 
    v_y = pixhawk.y_vel 
    H = pixhawk.altitude

    R = calculate_range(v_x, v_y, H)

    # placeholder
    T_long = mapping.target_long
    T_lat = mapping.target_lat
    P_long = x
    P_lat = y

    RP_lat, RP_long = calculate_release_point(R, T_long, T_lat, P_long, P_lat)

    while 1:
        if x == RP_long * 1.02 and y == RP_lat * 1.02: # if we're within 2% of the release point 
            release_payload() # this interacts with the pixhawk, needs to be written

import numpy as np

def calculate_range(v_x, v_z, H, wind_speed):
    rho = 1.225 # kg/m^3 for density of air at sea level
    C_d = 0.3 # just ballparking this, we should experimentally test it though
    A =  0.05 * 0.3 # guessing 10cm in diameter, 30cm in height
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

    time_delay = 1 # assume 1 second time delay
    x = v_x * time_delay 

    terminal_velocity = np.sqrt((2*m*g)/(rho * A * C_d))

    while True:
        a_x = - q * (v_x ** 2) / m - q * (wind_speed ** 2) / m
        a_z = g -  q * (v_z ** 2) / m
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
    
        if z >= H:
            R = x
            break

        n +=1
    return R
    

def calculate_release_point(R, target_lat, target_long, plane_lat, plane_long):
    r = [target_lat - plane_lat, target_long - plane_long] # position vector from release point to target
    theta = np.arctan2(r[1], r[0])
    release_point_lat = target_lat - R * np.cos(theta)
    release_point_long = target_long - R * np.sin(theta)

    #theta = np.arctan((target_long - plane_long)/(target_lat - plane_lat))
    #release_point_lat = target_lat - R * np.sin(theta)
    #release_point_long = target_long - R * np.cos(theta)

    print("RELEASE POINT LAT IS: ", release_point_lat)
    print("RELEASE POINT LONG IS: ", release_point_long)

    return release_point_lat, release_point_long

def release_payload_simulator(R, initial_lat, initial_long, v_x, v_y, target_lat, target_long):
    # send plane along a trajectory determined by vx and vy
    # continually update position, call it p_long and p_lat
    # at each update, run calculate_release_point
    # if p_long ~ release_point_long and p_lat ~ release_point_lat, release payload

    
    x = initial_lat
    y = initial_long
    h = 0.02 # timestep
    release_point_lat, release_point_long = calculate_release_point(R, target_lat, target_long, x, y)

    r = [target_lat - x, target_long - y] # position vector from release point to target
    # return x,y when R is less than the distance between the release point and the target
    if np.linalg.norm(r) < R:
        print("RELEASE POINT IS NOT ON THE PATH")
        return x,y

    for i in range(100000):
        x += v_x*h
        y += v_y*h
        threshold = 0.05     # % error
        if i % 100 == 0:
            #print("X IS: ", x)
            #print("Y IS: ", y)
            print((1 - threshold)*release_point_lat, abs(x), abs((1 + threshold)*release_point_lat))
            print((1 - threshold)*release_point_long, abs(y), abs((1 + threshold)*release_point_long))
            continue
        if ((1 - threshold)*release_point_lat <= abs(x) <= abs((1 + threshold)*release_point_lat)) and ((1 - threshold)*release_point_long <= abs(y) <= abs((1 + threshold)*release_point_long)):
            print("RELEASED WITHIN THRESHOLD")
            return x,y
        
    return x,y

def release_payload(R, x, y, target_lat, target_long, release_point_lat, release_point_long):
    # if p_long ~ release_point_long and p_lat ~ release_point_lat, release payload

    r = [target_lat - x, target_long - y] # position vector from release point to target
    # return x,y when R is less than the distance between the release point and the target
    if np.linalg.norm(r) < R:
        print("RELEASE POINT IS NOT ON THE PATH")
        send_pixhawk_signal()

    threshold = 0.05 # % error
    if ((1 - threshold)*release_point_lat <= abs(x) <= abs((1 + threshold)*release_point_lat)) and ((1 - threshold)*release_point_long <= abs(y) <= abs((1 + threshold)*release_point_long)):
        print("RELEASED WITHIN THRESHOLD")
        send_pixhawk_signal()
        
#!/usr/bin/env python

from dronekit import connect
import time
import os
import time
import os
import csv
from csv import writer

# Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
parser.add_argument('--connect', 
                   help="vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None

# Start timer
start = time.time()

# Delete CSV of previous mission callbacks
folder_path = ('mission_callbacks')
folder = os.listdir(folder_path)
for csvfile in folder:
    if csvfile.endswith(".csv"):
        os.remove(os.path.join(folder_path, csvfile))

# Create blank CSV for upcoming mission callbacks
with open('mission_callbacks/mission_callbacks.csv', 'w', newline='') as csvfile:
            fieldnames = ['TIMESTAMP', 'Global Location', 'Global Location (relative altitude)', 'Local Location', 'Attitude', 'Velocity', 'GPS', 'Wind', 'Last Heartbeat']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

## Connect to the AIRCRAFT ##
    # Connection string options: 
    # Serial port: /dev/ttyTHS1 also set baud=57600 
    # (baud must match baud value inputed in the Mission Planner)
    # USB: /dev/ttyUSB<N>
    # may need to set 'wait_ready' to False
    
# Specify connection string: UNCOMMENT THIS TO CONNECT TO PIXHAWK
# connection_string = '/dev/ttyTHS1'

if connection_string:
    print('\nConnecting to aircraft on /dev/ttyTHS1 ...')
    vehicle = connect(connection_string, wait_ready=True, baud=57600)
    print("\nSuccessfully connected to aircraft. Begin mission!")


## Start SIMULATION if no connection string specified ##
if not connection_string:
    import dronekit_sitl
    print("\nBegin mission simulation")
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()
    
    # Connect to the Vehicle. 
    #   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
    print("\nConnecting to vehicle on: %s" % connection_string)
    vehicle = connect(connection_string, wait_ready=True)
    print("Mode: %s" % vehicle.mode.name)
    vehicle.wait_ready('autopilot_version')
    
# Get some vehicle attributes (state)
print("\nInitial vehicle attribute values:")
print(" Global Location: %s" % vehicle.location.global_frame)
print(" Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
print(" Local Location: %s" % vehicle.location.local_frame)
print(" Attitude: %s" % vehicle.attitude)
print(" Velocity: %s" % vehicle.velocity)
print(" GPS: %s" % vehicle.gps_0)
print(" Wind Direction: %s" % vehicle.wind)
print(" Wind Speed: %s" % vehicle.wind)
print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
print(" Battery: %s" % vehicle.battery)


# Function to arm and then takeoff to a user specified altitude
def arm_and_takeoff(aTargetAltitude):

    print ("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print (" Waiting for vehicle to initialise...")
        time.sleep(1)
        
    print ("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    while not vehicle.armed:
        print (" Waiting for arming...")
        time.sleep(1)

    print ("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

  # Check that vehicle has reached takeoff altitude
    while True:
        print (" Altitude: ", vehicle.location.global_relative_frame.alt) 
        
        #Break and return from function just below target altitude.        
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
            print("Reached target altitude")
            break
        time.sleep(1)

# Initialize the takeoff sequence to 20m
arm_and_takeoff(20)

print("Take off complete")

# Hover for 10 seconds
time.sleep(10)

print("Now let's land")
vehicle.mode = VehicleMode("LAND")

# Close vehicle object
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()

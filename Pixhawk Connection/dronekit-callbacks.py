#!/usr/bin/env python

from dronekit import connect
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
def delete_csv():
    folder_path = ('mission_callbacks')
    folder = os.listdir(folder_path)
    for csvfile in folder:
        if csvfile.endswith(".csv"):
            os.remove(os.path.join(folder_path, csvfile))
            
# delete_csv()

# Create blank CSV for upcoming mission callbacks
with open('mission_callbacks/mission_callbacks.csv', 'a', newline='') as csvfile:
            fieldnames = ['TIMESTAMP', 'Global Location', 'Global Location (relative altitude)', 'Local Location', 'Attitude', 'Velocity', 'GPS', 'Last Heartbeat']
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


## Add and remove and attribute callbacks ##

# Define callback for GLOBAL FRAME observer
last_global_frame_cache = None
def global_frame_callback(self, attr_name, value):
    # `attr_name` - the observed attribute (used if callback is used for multiple attributes)
    # `self` - the associated vehicle object (used if a callback is different for multiple vehicles)
    # `value` is the updated attribute value.
    global last_global_frame_cache
    # Only publish when value changes
    if value!=last_global_frame_cache:
        print(" CALLBACK: (%s): %s" % (attr_name,value))
        # publish value change to CSV 
        with open('mission_callbacks/mission_callbacks.csv', 'a', newline='') as csvfile:
            writer_object = csv.writer(csvfile)
            new_entry = [time.perf_counter(), value, vehicle.location.global_relative_frame, vehicle.location.local_frame, vehicle.attitude, vehicle.velocity, vehicle.gps_0, vehicle.wind, vehicle.last_heartbeat]
            writer_object.writerow(new_entry)
            csvfile.close()
        last_global_frame_cache=value

# Define callback for RELATIVE FRAME observer
last_global_relative_frame_cache = None
def global_relative_frame_callback(self, attr_name, value):
    # `attr_name` - the observed attribute (used if callback is used for multiple attributes)
    # `self` - the associated vehicle object (used if a callback is different for multiple vehicles)
    # `value` is the updated attribute value.
    global last_global_relative_frame_cache
    # Only publish when value changes
    if value!=last_global_relative_frame_cache:
        print(" CALLBACK: (%s): %s" % (attr_name,value))
        # publish value change to CSV 
        with open('mission_callbacks/mission_callbacks.csv', 'a', newline='') as csvfile:
            writer_object = csv.writer(csvfile)
            new_entry = [time.perf_counter(), vehicle.location.global_frame, value, vehicle.location.local_frame, vehicle.attitude, vehicle.velocity, vehicle.gps_0, vehicle.wind, vehicle.last_heartbeat]
            writer_object.writerow(new_entry)
            csvfile.close()
        last_global_relative_frame_cache=value

# Define callback for LOCAL FRAME observer
last_local_frame_cache = None
def local_frame_callback(self, attr_name, value):
    # `attr_name` - the observed attribute (used if callback is used for multiple attributes)
    # `self` - the associated vehicle object (used if a callback is different for multiple vehicles)
    # `value` is the updated attribute value.
    global last_local_frame_cache
    # Only publish when value changes
    if value!=last_local_frame_cache:
        print(" CALLBACK: (%s): %s" % (attr_name,value))
        # publish value change to CSV 
        with open('mission_callbacks/mission_callbacks.csv', 'a', newline='') as csvfile:
            writer_object = csv.writer(csvfile)
            new_entry = [time.perf_counter(), vehicle.location.global_frame, vehicle.location.global_relative_frame, value, vehicle.attitude, vehicle.velocity, vehicle.gps_0, vehicle.wind, vehicle.last_heartbeat]
            writer_object.writerow(new_entry)
            csvfile.close()
        last_local_frame_cache=value

# Define callback for ATTITUDE observer
last_attitude_cache = None
def attitude_callback(self, attr_name, value):
    # `attr_name` - the observed attribute (used if callback is used for multiple attributes)
    # `self` - the associated vehicle object (used if a callback is different for multiple vehicles)
    # `value` is the updated attribute value.
    global last_attitude_cache
    # Only publish when value changes
    if value!=last_attitude_cache:
        print(" CALLBACK: (%s): %s" % (attr_name,value))
        # publish value change to CSV 
        with open('mission_callbacks/mission_callbacks.csv', 'a', newline='') as csvfile:
            writer_object = csv.writer(csvfile)
            new_entry = [time.perf_counter(), vehicle.location.global_frame, vehicle.location.global_relative_frame, vehicle.location.local_frame, value, vehicle.velocity, vehicle.gps_0, vehicle.wind, vehicle.last_heartbeat]
            writer_object.writerow(new_entry)
            csvfile.close()
        last_attitude_cache=value

# Define callback for VELOCITY observer
last_velocity_cache = None
def velocity_callback(self, attr_name, value):
    # `attr_name` - the observed attribute (used if callback is used for multiple attributes)
    # `self` - the associated vehicle object (used if a callback is different for multiple vehicles)
    # `value` is the updated attribute value.
    global last_velocity_cache
    # Only publish when value changes
    if value!=last_velocity_cache:
        print(" CALLBACK: (%s): %s" % (attr_name,value))
        # publish value change to CSV 
        with open('mission_callbacks/mission_callbacks.csv', 'a', newline='') as csvfile:
            writer_object = csv.writer(csvfile)
            new_entry = [time.perf_counter(), vehicle.location.global_frame, vehicle.location.global_relative_frame, vehicle.location.local_frame, vehicle.attitude, value, vehicle.gps_0, vehicle.wind, vehicle.last_heartbeat]
            writer_object.writerow(new_entry)
            csvfile.close()
        last_velocity_cache=value

# Define callback for GPS observer
last_gps_0_cache = None
def gps_0_callback(self, attr_name, value):
    # `attr_name` - the observed attribute (used if callback is used for multiple attributes)
    # `self` - the associated vehicle object (used if a callback is different for multiple vehicles)
    # `value` is the updated attribute value.
    global last_gps_0_cache
    # Only publish when value changes
    if value!=last_gps_0_cache:
        print(" CALLBACK: (%s): %s" % (attr_name,value))
        # publish value change to CSV 
        with open('mission_callbacks/mission_callbacks.csv', 'a', newline='') as csvfile:
            writer_object = csv.writer(csvfile)
            new_entry = [time.perf_counter(), vehicle.location.global_frame, vehicle.location.global_relative_frame, vehicle.location.local_frame, vehicle.attitude, vehicle.velocity, value, vehicle.wind, vehicle.last_heartbeat]
            writer_object.writerow(new_entry)
            csvfile.close()
        last_gps_0_cache=value

# Define callback for WIND observer
last_wind_cache = None
def wind_callback(self, attr_name, value):
    # `attr_name` - the observed attribute (used if callback is used for multiple attributes)
    # `self` - the associated vehicle object (used if a callback is different for multiple vehicles)
    # `value` is the updated attribute value.
    global last_wind_cache
    # Only publish when value changes
    if value!=last_wind_cache:
        print(" CALLBACK: (%s): %s" % (attr_name,value))
        print(" Wind: %s" % vehicle.wind)
        # publish value change to CSV 
        with open('mission_callbacks/mission_callbacks.csv', 'a', newline='') as csvfile:
            writer_object = csv.writer(csvfile)
            new_entry = [time.perf_counter(), vehicle.location.global_frame, vehicle.location.global_relative_frame, vehicle.location.local_frame, vehicle.attitude, vehicle.velocity, vehicle.gps_0, value, vehicle.last_heartbeat]
            writer_object.writerow(new_entry)
            csvfile.close()
        last_last_heartbeat_cache=value

# Define callback for LAST HEARTBEAT observer
last_last_heartbeat_cache = None
def last_heartbeat_callback(self, attr_name, value):
    # `attr_name` - the observed attribute (used if callback is used for multiple attributes)
    # `self` - the associated vehicle object (used if a callback is different for multiple vehicles)
    # `value` is the updated attribute value.
    global last_last_heartbeat_cache
    # Only publish when value changes
    if value!=last_last_heartbeat_cache:
        print(" CALLBACK: (%s): %s" % (attr_name,value))
        # publish value change to CSV 
        with open('mission_callbacks/mission_callbacks.csv', 'a', newline='') as csvfile:
            writer_object = csv.writer(csvfile)
            new_entry = [time.perf_counter(), vehicle.location.global_frame, vehicle.location.global_relative_frame, vehicle.location.local_frame, vehicle.attitude, vehicle.velocity, vehicle.gps_0, vehicle.wind, value]
            writer_object.writerow(new_entry)
            csvfile.close()
        last_last_heartbeat_cache=value

# Add observers with `add_attribute_listener()` specifying the attribute and callback function
print("\nAdd `global frame` attribute callback/observer on `vehicle`")     
vehicle.add_attribute_listener('location.global_frame', global_frame_callback)
print("Add `relative frame` attribute callback/observer on `vehicle`")     
vehicle.add_attribute_listener('location.global_relative_frame', global_relative_frame_callback)
print("Add `local frame` attribute callback/observer on `vehicle`")     
vehicle.add_attribute_listener('location.local_frame', local_frame_callback)
print("Add `attitude` attribute callback/observer on `vehicle`")     
vehicle.add_attribute_listener('attitude', attitude_callback)
print("Add `velocity` attribute callback/observer on `vehicle`")     
vehicle.add_attribute_listener('velocity', velocity_callback)
print("Add `gps_0` attribute callback/observer on `vehicle`")     
vehicle.add_attribute_listener('gps_0', gps_0_callback)
print("Add `wind` attribute callback/observer on `vehicle`")     
vehicle.add_attribute_listener('wind', wind_callback)
print("Add `last_heartbeat` attribute callback/observer on `vehicle`")     
vehicle.add_attribute_listener('last_heartbeat', last_heartbeat_callback)


## Define how long to observe callbacks for ##
print("\n Wait 5s so callback invoked before observer removed")
print(" ")
time.sleep(5)

# Remove observer added with `add_attribute_listener()` specifying the attribute and callback function
print("\nRemove `global frame` attribute callback/observer on `vehicle`")     
vehicle.remove_attribute_listener('location.global_frame', global_frame_callback)
print("Remove `relative frame` attribute callback/observer on `vehicle`")     
vehicle.remove_attribute_listener('location.global_relative_frame', global_relative_frame_callback)
print("Remove `local frame` attribute callback/observer on `vehicle`")     
vehicle.remove_attribute_listener('location.local_frame', local_frame_callback)
print("Remove `attitude` attribute callback/observer on `vehicle`")     
vehicle.remove_attribute_listener('attitude', attitude_callback)
print("Remove `velocity` attribute callback/observer on `vehicle`")     
vehicle.remove_attribute_listener('velocity', velocity_callback)
print("Remove `gps_0` attribute callback/observer on `vehicle`")     
vehicle.remove_attribute_listener('gps_0', gps_0_callback)
print("Remove `wind` attribute callback/observer on `vehicle`")     
vehicle.remove_attribute_listener('wind', wind_callback)
print("Remove `last_heartbeat` attribute callback/observer on `vehicle`")     
vehicle.remove_attribute_listener('last_heartbeat', last_heartbeat_callback)

#Close vehicle object before exiting script
print("\nClose vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()

print("\nMission Completed")
print(" ")

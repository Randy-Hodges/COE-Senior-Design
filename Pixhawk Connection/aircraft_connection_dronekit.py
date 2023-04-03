from dronekit import connect, VehicleMode
import time
import os
from csv import writer

# start = time.time()

# folder_path = ('attributes.csv')
# folder = os.listdir(folder_path)
# for csvfile in folder:
#     if csvfile.endswith(".csv"):
#         os.remove(os.path.join(folder_path, csvfile))
        
# Connect to aircraft
    # Connection string options: 
    # Serial port: /dev/ttyTHS1 also set baud=57600 
    # (baud must match baud value inputed in the Mission Planner)
    # USB: /dev/ttyUSB<N>
print('connecting to aircraft on /dev/ttyUSB0')
vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=57600)

print("CONECTED!!!!!!!!")

# Get some aircraft attributes
print(" Autopilot capabilities")
print(" Global Location: %s" % vehicle.location.global_frame)
print(" Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
print(" Local Location: %s" % vehicle.location.local_frame)
print(" Attitude: %s" % vehicle.attitude)
print(" Velocity: %s" % vehicle.velocity)
print(" GPS: %s" % vehicle.gps_0)
print(" Last Heartbeat: %s" % vehicle.last_heartbeat)

vehicle.close

# need to add callback fuctions to update vehicles status 
# https://dronekit-python.readthedocs.io/en/latest/examples/vehicle_state.html
#https://www.samba.org/tridge/UAV/pymavlink/apidocs/mavlink.MAVLink_global_position_int_message.html (*)
# ^^ mavlink message functions

# Create a message listener using the decorator.

# # GPS Coordinates
# @vehicle.on_message('global_position_int_message')
# def listener_GPS(self, name, message):
#     print('GPS coordiantes')
#     print message.lat
#     print message.lon
#     print message.alt


# # Shows that system is present and responding
# @vehicle.on_message('heartbeat_message')
# def listener_heartbeat(self, name, message):
#     print('hearbeat')
#     print (message)

# # Shows that system is present and responding
# @vehicle.on_message('attitude_message')
# def listener_attitude(self, name, message):
#     print('attitude')
#     print message.roll
#     print message.pitch
#     print message.yaw

# #OR!!! with attributes cant find message class that has velocity (differnet mesege classes linked above  (*))

# #Velocity
# @vehicle.on_attributes('velocity')
# def velocity_listener(self, name, value):
#     print(value)

    
# #Close vehicle object
# vehicle.close



# # # GPS Coordinates
# # @vehicle.on_message('global_position_int_message')
# # def listener_GPS(self, name, message):
# #     print('GPS coordiantes')
# #     print message.lat
# #     print message.lon
# #     print message.alt


# # # Shows that system is present and responding
# # @vehicle.on_message('heartbeat_message')
# # def listener_heartbeat(self, name, message):
# #     print('hearbeat')
# #     print (message)

# # # Shows that system is present and responding
# # @vehicle.on_message('attitude_message')
# # def listener_attitude(self, name, message):
# #     print('attitude')
# #     print message.roll
# #     print message.pitch
# #     print message.yaw

# # #OR!!! with attributes cant find message class that has velocity (differnet mesege classes linked above  (*))

# # #Velocity
# # @vehicle.on_attributes('velocity')
# # def attitude_listener(self, name,message):
# #     print message 

    
# # #Close vehicle object
# # vehicle.close
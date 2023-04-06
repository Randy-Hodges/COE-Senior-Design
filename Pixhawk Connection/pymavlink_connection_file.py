from pymavlink import mavutil
import time
import os
import time
import csv
from csv import writer

# Start timer
start = time.time()

# Delete CSV of previous mission callbacks
folder_path = ('mission_callbacks')
folder = os.listdir(folder_path)
for csvfile in folder:
    if csvfile.endswith('.csv'):
        os.remove(os.path.join(folder_path, csvfile))

# Create blanck CSV for upcoming mission callbacks
with open('mission_callbacks/mission_callbacks.csv', 'w', newline='') as csvfile:
    fieldnames = ['TIMESTAMP', 'yaw', 'pitch', 'roll', 'ground speed', 'air_speed', 'latitude', 'altitude', 'longitude', 'wind direction', 'wind speed', 'Heartbeat']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() 



# Start connection listenning to the TELEM2 Port 
master = mavutil.mavlink_connection('/dev/ttyTHS1', baud=57600)

# Wait for the first heartbeat
master.wait_heartbeat()
print('heartbeat from system (system %u component %u)' %(master.target_system, master.target_component))









# Atribute reader function
def atribute_reader():
    while True:
        msg = master.recv_match()
        if not msg:
            continue
        if msg.get_type() in ('ATTITUDE', 'VFR_HUD', 'GLOBAL_POSITION_INT', 'WIND','HEARTBEAT'):

            atribute_dict = msg.to_dict()
		
            if msg.get_type() == 'ATTITUDE':
                yaw = atribute_dict['yaw']
                pitch = atribute_dict['pitch']
                roll = atribute_dict['roll']

            elif msg.get_type() == 'VFR_HUD':
                ground_speed = atribute_dict['groundspeed']
                air_speed = atribute_dict['airspeed']
            
            elif msg.get_type() == 'GLOBAL_POSITION_INT':
                latitude = atribute_dict['lat']
                altitude = atribute_dict['alt']
                longitude = atribute_dict['lon']
            
            elif msg.get_type() == 'WIND':
                wind_direction = atribute_dict['direction']
                wind_speed = atribute_dict['speed']
            
            
            elif msg.get_type() == 'HEARTBEAT':
                system_status = atribute_dict['system_status']
	         # publish value change to CSV 
                with open('mission_callbacks/mission_callbacks.csv', 'a', newline='') as csvfile:
                    writer_object = csv.writer(csvfile)
                    new_entry = [time.perf_counter(), yaw, pitch, roll, ground_speed, air_speed, latitude, altitude, longitude, wind_direction, wind_speed, system_status]
                    writer_object.writerow(new_entry)
                    csvfile.close()

atribute_reader()
		






# function to request messeges at different frequencies
def request_message_interval(message_id, frequency_hz):
	master.mav.command_long_send(
		master.target_system, master.target_component, 		   			    
		mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 
		0, message_id, 1e6/frequency_hz, 0,0,0,0,0)

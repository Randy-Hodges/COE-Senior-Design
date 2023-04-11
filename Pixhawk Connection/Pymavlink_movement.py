from pymavlink import mavutil

# Start connection listenning to the TELEM2 Port 
master = mavutil.mavlink_connection('/dev/ttyTHS1', baud=57600)

# Wait for the first heartbeat
master.wait_heartbeat()
print('heartbeat from system (system %u component %u)' %(master.target_system, master.target_component))



# Function sends aircraft to location (lon, lat, alt)
def send_to_target(lon, lat, alt):
    master.mav.send(mavutil.mavlink.MAV_set_position_target_global_int_message(
        10, 
        master.target_system, # system ID of vehicle
        master.target_component, # Component ID of flight coontroler
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, # coordinate frame
        int(0b110111111000), # type mask, use Position 
        int(lat* 10 ** 7), # latitude 
        int(lon* 10 ** 7), # longitude
        alt, # altitude in meters above home!
        0, 0, 0, 0, 0, 0,
        0, # yaw
        0 # yaw rate
        ))
    
# Fuction send aircraft to loaction using waypoint message  
def send_to_target_2(acc_radius,pass_by,lat,lon,alt):
      master.mav.send(mavutil.mavlink.MAV_CMD_NAV_WAYPOINT(
        0,
        acc_radius, # Acceptance radius in meters (waypoint is complete when the plane is this close to the waypoint location
        pass_by, #0 to pass through the WP, if > 0 radius in meters to pass by WP. Positive value for clockwise orbit, negative value for counter-clockwise orbit. Allows trajectory control.
        0, # yaw
        lat, # latitude
        lon, # longitude
        alt # altitude
        ))
      
# Function sends aircraft to taget and circles around target for a designated number of turns
def survey_target_turns(turns,radius,lat,lon,alt):
     master.mav.send(mavutil.mavlink.MAV_CMD_NAV_LOITER_TURNS(
        turns, # number of turns
        0, # "Heading Required" minValue="0" maxValue="1" Leave loiter circle only once heading towards the next waypoint (0 = False)
        radius, # Radius around waypoint, in meters. Specify as a positive value to loiter clockwise, negative to move counter-clockwise
        0, 
        lat, # latitude, If zero, the vehicle will loiter at the current latitude.
        lon, # longitude, If zero, the vehicle will loiter at the current longitude.
        alt # altitude, If zero, the vehicle will loiter at the current altitude.
        ))

# Function sends aircraft to taget and circles around target for a designated ammount of time     
def survey_target_time(time, radius,lat,lon,alt):
    master.mav.send(mavutil.mavlink.MAV_CMD_NAV_LOITER_TIME(
          time, # time in secconds
          0, # "Heading Required" minValue="0" maxValue="1" Leave loiter circle only once heading towards the next waypoint (0 = False)
          radius, # Radius around waypoint, in meters. Specify as a positive value to loiter clockwise, negative to move counter-clockwise
          0, 
          lat, # latitude, If zero, the vehicle will loiter at the current latitude.
          lon, # longitude, If zero, the vehicle will loiter at the current longitude.
          alt # altitude, If zero, the vehicle will loiter at the current altitude.
          ))

 
# Deploy payload on a Lat / Lon / Alt position. This includes the navigation to reach the required release position and velocity
def deploy_payload(ground_speed, altitude_clearance, lat, lon, alt):
    master.mav.send(mavutil.mavlink.MAV_CMD_PAYLOAD_PREPARE_DEPLOY(
        1, # Operation Mode: 0: prepare single payload deploy (overwriting previous requests), but do not execute it. 1: execute payload deploy immediately (rejecting further deploy commands during execution, but allowing abort). 2: add payload deploy to existing deployment list.
        -1, # Approach Vector: desired approach vector in compass heading. A negative value indicates the system can define the approach vector at will
        ground_speed, # Desired ground speed at release time. This can be overridden by the airframe in case it needs to meet minimum airspeed. A negative value indicates the system can define the ground speed at will.
        altitude_clearance, # Minimum altitude clearance to the release position. A negative value indicates the system can define the clearance at will.
        lat,
        lon,
        alt
    ))








#   <entry value="30002" name="MAV_CMD_PAYLOAD_CONTROL_DEPLOY" hasLocation="false" isDestination="false">
#         <deprecated since="2021-06" replaced_by=""/>
#         <description>Control the payload deployment.</description>
#         <param index="1" label="Operation Mode" minValue="0" maxValue="101" increment="1">Operation mode. 0: Abort deployment, continue normal mission. 1: switch to payload deployment mode. 100: delete first payload deployment request. 101: delete all payload deployment requests.</param>
#         <param index="2">Reserved</param>
#         <param index="3">Reserved</param>
#         <param index="4">Reserved</param>
#         <param index="5">Reserved</param>
#         <param index="6">Reserved</param>
#         <param index="7">Reserved</param>
#       </entry>




# Assumes aircraft is in the air -> send it to target position
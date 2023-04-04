# Python code for Multiple Color Detection
  
  
import numpy as np
import cv2
  
  
# Capturing video through webcam
webcam = cv2.VideoCapture('1_2023-03-01_17-04-19.avi')
  
# Start a while loop
while(1):
      
    # Reading the video from the
    # webcam in image frames
    _, imageFrame = webcam.read()
  
    # Convert the imageFrame in 
    # BGR(RGB color space) to 
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
  
    # Set range for red color and 
    # define mask
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
  
    # Set range for green color and 
    # define mask
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
  
    # Set range for blue color and
    # define mask
    blue_lower = np.array([80, 79, 132], np.uint8)
    blue_upper = np.array([125, 133, 218], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
      
    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")
    
    # For red color
    #red_mask = cv2.dilate(red_mask, kernal)
    #res_red = cv2.bitwise_and(imageFrame, imageFrame, 
    #                          mask = red_mask)
      
    # For green color
    #green_mask = cv2.dilate(green_mask, kernal)
    #res_green = cv2.bitwise_and(imageFrame, imageFrame,
     #                           mask = green_mask)
      
    # For blue color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                              mask = blue_mask)
   
    # Creating contour to track red color
    #contours, hierarchy = cv2.findContours(red_mask,
    #                                       cv2.RETR_TREE,
    #                                       cv2.CHAIN_APPROX_SIMPLE)
      
    #for pic, contour in enumerate(contours):
    #    area = cv2.contourArea(contour)
    #    if(area > 300):
    #        x, y, w, h = cv2.boundingRect(contour)
    #        imageFrame = cv2.rectangle(imageFrame, (x, y), 
    #                                   (x + w, y + h), 
    #                                  (0, 0, 255), 2)
              
    #        cv2.putText(imageFrame, "Red Colour", (x, y),
    #                    cv2.FONT_HERSHEY_SIMPLEX, 1.0,
    #                    (0, 0, 255))    
  
    # Creating contour to track green color
    #contours, hierarchy = cv2.findContours(green_mask,
    #                                       cv2.RETR_TREE,
    #                                       cv2.CHAIN_APPROX_SIMPLE)
      
    #for pic, contour in enumerate(contours):
    #    area = cv2.contourArea(contour)
    #    if(area > 300):
    #        x, y, w, h = cv2.boundingRect(contour)
    #        imageFrame = cv2.rectangle(imageFrame, (x, y), 
    #                                   (x + w, y + h),
    #                                   (0, 255, 0), 2)
              
    #        cv2.putText(imageFrame, "Green Colour", (x, y),
    #                    cv2.FONT_HERSHEY_SIMPLEX, 
    #                    1.0, (0, 255, 0))
  
    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (255, 0, 0), 2)
              
            cv2.putText(imageFrame, "Blue Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 0, 0))
              
    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

import cv2
import os
import csv
from csv import writer
import time

# Start timer
start = time.time()

# Clear existing screenshots

folder_path = ('target_recognition/screenshots')
folder = os.listdir(folder_path)

for images in folder:
    if images.endswith(".jpg"):
        os.remove(os.path.join(folder_path, images))
        
# Clear existing csv file

folder_path = ('target_recognition')
folder = os.listdir(folder_path)

for csvfile in folder:
    if csvfile.endswith(".csv"):
        os.remove(os.path.join(folder_path, csvfile))
        
# Load the template images in color
template1 = cv2.imread('target_recognition/images/blue-target.png')
template2 = cv2.imread('target_recognition/images/blue-white-target.png')

# Open the video file
cap = cv2.VideoCapture('target_recognition/video/1_2023-03-01_17-04-19.avi')
# cap = cv2.VideoCapture('target_recognition/vid1.mp4')

# Create new csv file for pixel coordinates
with open('target_recognition/pixel_coordinates.csv', 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'identifier', 'top_left x', 'top_left y', 'bottom_right x', 'bottom_right y']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

# Check if the video file was opened successfully
if not cap.isOpened():
    # Get the error message
    error_msg = cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
    # Print the error message
    print("Error opening video file: ", error_msg)

cap.set(cv2.CAP_PROP_POS_MSEC, 310000)

# Define the threshold for matching
threshold = 0.65

# counter for ALL target screenshots
count_all = 0

# counter for critical target screenshots
count_critical = 0

# Loop through each frame of the video
while cap.isOpened():
    # Read a single frame from the video
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        break

    # Perform template matching for template1
    res1 = cv2.matchTemplate(frame, template1, cv2.TM_CCOEFF_NORMED)

    # Find the location of the best match for template1
    loc1 = cv2.minMaxLoc(res1)

    # If the best match for template1 is above the threshold, draw a rectangle around it
    
    if loc1[1] > threshold:
        # print("found")
        w, h, _ = template1.shape
        top_left = loc1[3]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)
        
        # holds screenshot of target
        cv2.imshow('frame', frame)
        # saves screenshot
        cv2.imwrite("target_recognition/screenshots/target%d.jpg" % count_all, frame)
        
        # write target pixel location to csv file, with image label identifier
        with open('target_recognition/pixel_coordinates.csv', 'a', newline='') as csvfile:
            writer_object = csv.writer(csvfile)
            new_entry = [time.perf_counter(), 'target%d' % count_all, top_left[0], top_left[1], bottom_right[0], bottom_right[1]]
            writer_object.writerow(new_entry)
            csvfile.close()
            
        # update count
        count_all = count_all+1

    # Perform template matching for template2
    res2 = cv2.matchTemplate(frame, template2, cv2.TM_CCOEFF_NORMED)

    # Find the location of the best match for template2
    loc2 = cv2.minMaxLoc(res2)

    # If the best match for template2 is above the threshold, draw a rectangle around it
    
    if loc2[1] > threshold:
        # print("found2")
        w, h, _ = template2.shape
        top_left = loc2[3]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        
        # holds screenshot of critical target
        cv2.imshow('frame', frame)
        # saves screenshot
        cv2.imwrite("target_recognition/screenshots/critical%d.jpg" % count_critical, frame)
        
        # write target pixel location to csv file, with image label identifier
        with open('target_recognition/pixel_coordinates.csv', 'a', newline='') as csvfile:
            writer_object = csv.writer(csvfile)
            new_entry = [time.perf_counter(), 'critical%d' % count_critical, top_left[0], top_left[1], bottom_right[0], bottom_right[1]]
            writer_object.writerow(new_entry)
            csvfile.close()
        
        # update count
        count_critical = count_critical+1

    # Display the frame
    cv2.imshow('Frame', frame)

    # Wait for a key press to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video file and close all windows
cap.release()
cv2.destroyAllWindows()

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
import numpy as np
import rasterio 

# Open raster file with rasterio
rst = rasterio.open('ARCAClippedGCS.tif')

# Read raster data into numpy array
data = rst.read(1)

# Define colormap for raster
cmap = LinearSegmentedColormap.from_list('mycmap', [(0, 'black'), (1, 'white')])

# Create figure and axis objects
fig, ax = plt.subplots(figsize=(10, 10))

# Plot raster as image
ax.imshow(data, cmap=cmap, extent=[rst.bounds.left, rst.bounds.right, rst.bounds.bottom, rst.bounds.top])

# set bounds
x_gcs_left = 97.6063196 #the longitude is made positive
y_gcs_top = 30.3267942
length_gcs = 0.0058647 #length of both sides of raster in gcs

x_length = rst.bounds.right-rst.bounds.left #length of raster in x in matplotlib
y_length = rst.bounds.top-rst.bounds.bottom #length of raster in y in matplotlib

# Convert gcs coordinates to matplotlib coordinates
# set coordinates of empty tarps
x_gcs_tarp = [97.602743, 97.60284224192607, 97.60230311795735]
y_gcs_tarp = [30.324161, 30.3236423845285, 30.3236423845285]

#convert from gcs to matplotlib
x_points = [((x_gcs_left - x_gcs_tarp[i])/length_gcs)*x_length for i in range(0, len(x_gcs_tarp))]
y_points = [((y_gcs_top - y_gcs_tarp[i])/length_gcs)*y_length for i in range(0, len(y_gcs_tarp))]   

# Overlay points on top of raster
x = [rst.bounds.left + x_points[i] for i in range(0, len(x_gcs_tarp))]
y = [rst.bounds.top - y_points[i] for i in range(0, len(y_gcs_tarp))]
ax.scatter(x, y, color='blue', marker='s', label = 'Empty Tarp')

# Convert gcs coordinates to matplotlib coordinates
# set coordinates of Non-Critical Targets
x_gcs_non = [97.602394]
y_gcs_non = [30.324453]

#convert from gcs to matplotlib
x_points = [((x_gcs_left - x_gcs_non[i])/length_gcs)*x_length for i in range(0, len(x_gcs_non))]
y_points = [((y_gcs_top - y_gcs_non[i])/length_gcs)*y_length for i in range(0, len(y_gcs_non))]   

# Overlay points on top of raster
x = [rst.bounds.left + x_points[i] for i in range(0, len(x_gcs_non))]
y = [rst.bounds.top - y_points[i] for i in range(0, len(y_gcs_non))]
ax.scatter(x, y, color='Cyan', marker='o', label = 'Non-Critical')

# Convert gcs coordinates to matplotlib coordinates
# set coordinates of Critical Targets
x_gcs_crit = [97.603051]
y_gcs_crit = [30.324997]

#convert from gcs to matplotlib
x_points = [((x_gcs_left - x_gcs_crit[i])/length_gcs)*x_length for i in range(0, len(x_gcs_crit))]
y_points = [((y_gcs_top - y_gcs_crit[i])/length_gcs)*y_length for i in range(0, len(y_gcs_crit))]   

# Overlay points on top of raster
x = [rst.bounds.left + x_points[i] for i in range(0, len(x_gcs_crit))]
y = [rst.bounds.top - y_points[i] for i in range(0, len(y_gcs_crit))]
ax.scatter(x, y, color='Red', marker='x', label = 'Critical')

# Show the plot
plt.legend()
plt.show()

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
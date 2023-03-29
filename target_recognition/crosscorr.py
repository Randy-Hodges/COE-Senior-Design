#!/usr/bin/python3 
#
#
# Desc: Currently reads a video frame by frame and finds targets through template matching
#
# Warnings: This has currently been tested on low-quality footage. Higher quality footage might
#           require some tweaking of the code, especially the threshold. The code is currently
#           set up to read video, not a live stream. The cap.set() function is specific to certain 
#           videos.
#
# TODO:  Set code to loop through live stream.
#


import cv2
import os 
import time

# ---------------------------------------
# Define the threshold correlation score for matching
THRESHOLD = 0.65


# Load the template images in color
template1 = cv2.imread('target_recognition/images/blue-target.png')
template2 = cv2.imread('target_recognition/images/blue-white-target.png')

# Open the video file
cap = cv2.VideoCapture('target_recognition/video/1_2023-03-01_17-04-19.avi')
# Create output file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = os.path.join(os.getcwd(), 'target_recognition/video/output_video.mp4')
out = cv2.VideoWriter(output_file, 0x7634706d, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

# Check if the video file was opened successfully
if not cap.isOpened():
    error_msg = cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
    print("Error opening video file: ", error_msg)

cap.set(cv2.CAP_PROP_POS_MSEC, 313000) # sets the video to a specific time frame

start_time = time.time()

# Loop through each frame of the video
while cap.isOpened():
    if time.time() - start_time > 13:
        break
    ret, frame = cap.read()
    if not ret:
        break

    # Find the location of the best match for template1
    res1 = cv2.matchTemplate(frame, template1, cv2.TM_CCOEFF_NORMED)
    loc1 = cv2.minMaxLoc(res1)

    # If the best match for template1 is above the threshold, draw a rectangle around it
    if loc1[1] > THRESHOLD:
        # print("found")
        w, h, _ = template1.shape
        top_left = loc1[3]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)

    # Find the location of the best match for template2
    res2 = cv2.matchTemplate(frame, template2, cv2.TM_CCOEFF_NORMED)
    loc2 = cv2.minMaxLoc(res2)

    # If the best match for template2 is above the threshold, draw a rectangle around it
    if loc2[1] > THRESHOLD:
        # print("found2")
        w, h, _ = template2.shape
        top_left = loc2[3]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Frame', frame)
    out.write(frame)

    # Wait for a key press to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video file and close all windows
cap.release()
out.release()
cv2.destroyAllWindows()

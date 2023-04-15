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
templates = []
for i in range(8):
    templates.append(cv2.imread(f'target_recognition/images/other_teams_reference/critical/image ({i}).png'))
# template1 = cv2.imread('target_recognition/images/first_reference/blue-target.png')
# template2 = cv2.imread('target_recognition/images/first_reference/blue-white-target.png')

# Open the video file
cap = cv2.VideoCapture('target_recognition/video/source/new_footage.mp4')
# Create output file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = os.path.join(os.getcwd(), 'target_recognition/video/output/other_teams_output.mp4')
out = cv2.VideoWriter(output_file, 0x7634706d, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

# Check if the video file was opened successfully
if not cap.isOpened():
    error_msg = cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
    print("Error opening video file: ", error_msg)

cap.set(cv2.CAP_PROP_POS_MSEC, 145000) # sets the video to a specific time frame

start_time = time.time()


# Define way to find image
def find_image(frame, template):
    # Find the location of the best match for template1
    res1 = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    loc1 = cv2.minMaxLoc(res1)

    # If the best match for template1 is above the threshold, draw a rectangle around it
    if loc1[1] > THRESHOLD:
        # print("found")
        w, h, _ = template.shape
        top_left = loc1[3]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)


# Loop through each frame of the video
while cap.isOpened():
    if time.time() - start_time > 300:
        break
    ret, frame = cap.read()
    if not ret:
        break

    # Find location of best match for images
    for template in templates:
        find_image(frame=frame, template=template)

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

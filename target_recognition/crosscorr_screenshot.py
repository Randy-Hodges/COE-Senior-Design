import cv2
import os 

# Clear existing screenshots

folder_path = ('target_recognition/screenshots')
test = os.listdir(folder_path)

for images in test:
    if images.endswith(".jpg"):
        os.remove(os.path.join(folder_path, images))
        
# Load the template images in color
template1 = cv2.imread('target_recognition/images/blue-target.png')
template2 = cv2.imread('target_recognition/images/blue-white-target.png')

# Open the video file
cap = cv2.VideoCapture('target_recognition/video/1_2023-03-01_17-04-19.avi')
# cap = cv2.VideoCapture('target_recognition/vid1.mp4')

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

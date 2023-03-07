#!/usr/bin/python3 
#
#
# Desc: file for testing various code snippets


import pyautogui
import time
import cv2
import numpy as np
from PIL import Image, ImageDraw

# ---------------------------------------
print("---------------------")



def find_image(given_image: str, maxLoc_thresh = .05):
    '''
    See if given image is on the screen.
    :returns: True if symbol found, false otherwise.
              maxloc of match
    '''
    # with Image.open(given_image) as im:
    #     im.show()

    found = False # found image
    location = [0, 0]

    method = cv2.TM_SQDIFF_NORMED

    # Read images 
    image = pyautogui.screenshot()
    # make image compatible with cv2
    large_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    small_image = cv2.imread(given_image) 

    result = cv2.matchTemplate(small_image, large_image, method)

    # We want the minimum squared difference
    maxLoc, minLoc, comparedLoc, _ = cv2.minMaxLoc(result)
    
    # Location of best match
    MPx,MPy = comparedLoc
    location = [MPx, MPy]

     # Step 2: Get the size of the template. This is the same size as the match.
    trows,tcols = small_image.shape[:2]

    # Step 3: Draw the rectangle on large_image
    cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),3)

    img = cv2.cvtColor(large_image, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    

    if maxLoc < maxLoc_thresh:
        found = True
        #im_pil.show()
        # print(maxLoc, minLoc)
        return found, maxLoc
    else:
        return found, maxLoc




time.sleep(2)
found = pyautogui.locateOnScreen('target_recognition/images/randomimage.png', confidence=.9) # could be optimized by looking at a smaller window
print(found)
found, _ = find_image('target_recognition/images/randomimage.png')
print(found)

# Load the template image
template = cv2.imread('images/blue-target.png', cv2.IMREAD_GRAYSCALE)

# Open the video file
cap = cv2.VideoCapture('video/1_2023-03-01_17-04-19.avi')




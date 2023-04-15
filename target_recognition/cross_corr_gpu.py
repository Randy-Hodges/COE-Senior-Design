import cv2
from cv2 import cuda
import numpy as np

# Read image file as grayscale
input_image = cv2.imread('input_image.jpg', cv2.IMREAD_GRAYSCALE)

# Read image file as color
# Load the template images in color
templates = []
for i in range(8):
    templates.append(cv2.imread(f'target_recognition/images/other_teams_reference/critical/image ({i}).png'))

cap = cv2.VideoCapture('target_recognition/video/source/new_footage.mp4')
cap.set(cv2.CAP_PROP_POS_MSEC, 150000)
ret, frame = cap.read()

# Load input and template images into GPU memory
input_gpu = cv2.cuda_GpuMat()
template_gpu = cv2.cuda_GpuMat()

input_gpu.upload(frame)
# template_image = cv2.imread('template_image.jpg', cv2.IMREAD_COLOR)
template_gpu.upload(templates[0])

# Create instance of TemplateMatching class
tm = cv2.cuda.createTemplateMatching(cv2.CV_8UC1, cv2.TM_CCOEFF_NORMED)

# Perform template matching on GPU
result_gpu = tm.match(template_gpu, input_gpu)

# Download result from GPU memory to CPU memory
result = result_gpu.download()

# Find best match location
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# Draw rectangle around best match location
template_height, template_width = template_image.shape[:2]
top_left = max_loc
bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
cv2.rectangle(input_image, top_left, bottom_right, (0, 0, 255), 2)

# Show input image with template matching result
cv2.imshow("Result", input_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

import torch
import cv2
import os
import numpy as np

# Load the pre-trained model from the .pt file
weights_path = 'our_weights_1.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path)
# Get the class names
class_names = model.names

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define the folder containing the images to be processed
image_folder = 'data/test_yolov5_1'

# Define the target resolution
target_resolution = (640, 640)

objs_per_image = np.zeros(np.size(os.listdir(image_folder)))
counter = 0

# Loop over each image in the folder and perform object detection
for image_file in os.listdir(image_folder):
    # Read the image file
    image_path = os.path.join(image_folder, image_file)
    image = cv2.imread(image_path)

    # Resize the image to the target resolution
    image = cv2.resize(image, target_resolution)
    
    # Perform object detection using the YOLOv5 model
    results = model(image)

    # Extract the coordinates of the bounding boxes of each object detected in the image
    bboxes = results.xyxy[0].cpu().numpy()

    # Loop over each bounding box and print the coordinates
    #print(str(image_file))
    for bbox in bboxes:
        objs_per_image[counter] += 1
        x1, y1, x2, y2, conf, cls = bbox.tolist()
        class_name = class_names[int(cls)]
        print(f"Object detected: {class_name}, confidence {conf:.2f}, BBox: ({x1:.2f}, {y1:.2f}), ({x2:.2f}, {y2:.2f})")
        
    counter+=1
    
print(objs_per_image)
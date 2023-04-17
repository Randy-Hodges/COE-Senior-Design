import os

##weights_file = "our_weights_1.pt"
#image_folder = "data/test_yolov5_1"
#Where the bounding boxes are stored
#csv_file = "output_test.csv"

#print(yolo_query)


def classify_images(weights_file,image_folder , csv_file ):
    yolo_query = "python3 detect_coords.py --weights " +weights_file  + "  --img 640 --conf 0.25 --source "+image_folder+ " --csv_name "+csv_file
    os.system(yolo_query)
    
classify_images("our_weights_1.pt","data/test_yolov5_1", "output_testington.csv")



#os.system("python3 detect.py --weights our_weights_1.pt --img 640 --conf 0.25 --source data/test_yolov5_1")


#os.system("python3 detect_coords.py --weights our_weights_1.pt --img 640 --conf 0.25 --source data/test_yolov5_1 --csv_name output_test.csv")
Navigate to the yolov5 folder and run

```
pip install -qr requirements.txt 
```


To detect objects, run
```
python3 detect.py --weights <weight file> --img 640 --conf 0.25 --source <image folder>
````
This outputs labeled images as described in the terminal output following a succesful run

The example weight file is yolov5s.pt

Our weights file (this will be updated with more training) is our_weights_1.pt

The example image folder is data/images

The image folder of our testing flight images is data/test_yolov5_1
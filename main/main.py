import numpy as np
import cv2

from lanes_process import Lane
from camera import perspective_transform, undistort

import serial
def main_process(directions, locations):
    print(f"directions = {directions}")
    print(f"locations = {locations}")
    
    #serial connection with arduino
    while True:
            try:
                ser = serial.Serial(port="/dev/ttyUSB0",baudrate =115200, timeout = 1.0)
                ser.write("g".encode("utf-8"))
                print("arduino connection success ")
                break
            except:
                print("could not connect to serial")
        
    #Lane object
    lane = Lane()
    #start capturing with camera
    cap = cv2.VideoCapture(0)
    #set buffersize to 1 to get fresh image from buffer
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_180)
            undst_image = undistort(frame)
            #cv2.imshow("undst", undst_image)
            combined_binary = lane.edge_detection(undst_image)
            transform_image = perspective_transform(combined_binary) 
            crop_image = np.copy(transform_image[200:450,210:440])
            error, image = lane.get_error(crop_image)
            #cv2.imshow("framee", image)
            
            steer = error
            # TODO:: change 10 to any other value as per your requirement
            # here 10 represents the threshold value of steer angle 
            if(abs(steer) > 10): 
                if(steer >0):
                    # steer value is positive and greater than 10 so,
                    # send a right turn message to arduino
                    ser.write("d".encode("utf-8"))
                    print("right")
                else:
                    # steer value is negative. so,
                    # send a left turn message to arduino
                    ser.write("a".encode("utf-8"))
                    print("left")
            else:
                #  when steer value is between -10 to 10 send move straight signal to arduino 
                ser.write("w".encode("utf-8"))
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            ser.write("s".encode("utf-8"))
            break
    cap.release()
    cv2.destroyAllWindows()
    


